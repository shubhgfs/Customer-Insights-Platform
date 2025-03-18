import os
import time
import requests
import warnings
from urllib.parse import urlparse
from datetime import datetime, timedelta
from dotenv import load_dotenv
from azure.storage.blob import BlobServiceClient, generate_blob_sas, BlobSasPermissions
import logging
import json

# Suppress warnings
warnings.filterwarnings("ignore")

# Load environment variables
load_dotenv()

# Azure Storage and Speech API Configurations
AZURE_STORAGE_CONNECTION_STRING = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
AZURE_SPEECH_API_ENDPOINT = os.getenv("AZURE_SPEECH_API_ENDPOINT")
AZURE_SPEECH_API_KEY = os.getenv("AZURE_SPEECH_API_KEY")
AZURE_STORAGE_KEY = os.getenv("AZURE_STORAGE_KEY")

# Initialize Blob Service Client
blob_service_client = BlobServiceClient.from_connection_string(AZURE_STORAGE_CONNECTION_STRING, connection_verify=False)
container_client = blob_service_client.get_container_client("call-recordings")

# Speech API Headers and URL
transcription_url = f"{AZURE_SPEECH_API_ENDPOINT}/speechtotext/v3.2/transcriptions"
headers = {
    "Content-Type": "application/json",
    "Ocp-Apim-Subscription-Key": AZURE_SPEECH_API_KEY,
}

# Set up logging
log_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "process_log.txt")
logging.basicConfig(level=logging.INFO, filename=log_file, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger()

# Log an initial message
logger.info("Pipeline started.")

def get_wav_files(container_client, path="", blob_urls=None):
    """Retrieve all WAV file URLs from the Azure Blob Storage container."""
    if blob_urls is None:
        blob_urls = []

    blobs = container_client.walk_blobs(name_starts_with=path)
    for blob in blobs:
        if "/" in blob.name[len(path):]:
            get_wav_files(container_client, path=blob.name, blob_urls=blob_urls)
        else:
            blob_url = f"https://{container_client.account_name}.blob.core.windows.net/{container_client.container_name}/{blob.name}"
            blob_urls.append(blob_url)
            logger.info(f"Found audio file: {blob_url}")

    return blob_urls


def generate_sas_url(blob_url, sas_expiration=datetime.utcnow() + timedelta(hours=1)):
    """Generate a SAS token for accessing a blob."""
    parsed_url = urlparse(blob_url)
    account_name = parsed_url.netloc.split(".")[0]
    container_name = parsed_url.path.split("/")[1]
    blob_name = "/".join(parsed_url.path.split("/")[2:])

    if not AZURE_STORAGE_KEY:
        raise ValueError("AZURE_STORAGE_KEY is not set in environment variables")

    sas_token = generate_blob_sas(
        account_name=account_name,
        container_name=container_name,
        blob_name=blob_name,
        account_key=AZURE_STORAGE_KEY,
        permission=BlobSasPermissions(read=True),
        expiry=sas_expiration,
    )

    sas_url = f"https://{account_name}.blob.core.windows.net/{container_name}/{blob_name}?{sas_token}"
    logger.info(f"Generated SAS URL: {sas_url}")
    return sas_url


def start_transcription(sas_urls):
    """Start a transcription job using the Speech-to-Text API."""
    data = {
        "contentUrls": sas_urls,
        "locale": "en-AU",
        "displayName": "Batch Audio Transcription",
    }

    response = requests.post(transcription_url, headers=headers, json=data, verify=False)
    logger.info(f"Started transcription request: {response.status_code} - {response.text}")

    response_json = response.json()

    if "self" in response_json:
        transcription_id = response_json["self"].split("/")[-1]
        logger.info(f"Transcription job started with ID: {transcription_id}")
        return transcription_id
    else:
        logger.error("Error: Unable to start transcription. Please check the API key and endpoint.")
        return None


def monitor_transcription(transcription_id):
    """Monitor the transcription job until completion."""
    status_url = f"{transcription_url}/{transcription_id}"

    while True:
        try:
            response = requests.get(status_url, headers=headers, verify=False, timeout=30)
            response.raise_for_status()
            status = response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Error occurred while checking status: {e}")
            logger.info("Retrying in 10 seconds...")
            time.sleep(10)
            continue

        job_status = status.get("status", "")
        logger.info(f"Current status: {job_status}")

        if job_status == "Succeeded":
            logger.info("Transcription job succeeded!")
            return status
        elif job_status == "Failed":
            logger.error("Transcription job failed. Please check the error details.")
            return status
        else:
            logger.info("Transcription job in progress... Checking again in 10 seconds.")
            time.sleep(10)


def fetch_and_upload_transcripts(content_json):
    """Fetch the transcription results and upload them to Azure Blob Storage."""
    transcripts_url = content_json["links"]["files"]
    headers = {"Ocp-Apim-Subscription-Key": os.getenv("AZURE_SPEECH_API_KEY")}

    all_transcription_files = []

    # Fetch the first batch of transcription files
    response = requests.get(transcripts_url, headers=headers, verify=False)
    if response.status_code != 200:
        logger.error(f"Failed to fetch transcripts: {response.text}")
        return

    files_data = response.json()
    all_transcription_files.extend([file for file in files_data["values"] if file["kind"] == "Transcription"])

    # Pagination loop to fetch all files
    batch_num = 1
    while "@nextLink" in files_data:
        next_url = files_data["@nextLink"]
        logger.info(f"Fetching next batch {batch_num}: {next_url}")

        response = requests.get(next_url, headers=headers, verify=False)
        if response.status_code != 200:
            logger.error(f"Failed to fetch next batch: {response.text}")
            break

        files_data = response.json()
        all_transcription_files.extend([file for file in files_data["values"] if file["kind"] == "Transcription"])
        batch_num += 1

    # Upload transcriptions to Azure Storage
    for file in all_transcription_files:
        file_url = file["links"]["contentUrl"]
        file_response = requests.get(file_url, verify=False).json()
        source_url = file_response["source"]

        parsed_source_url = urlparse(source_url)
        blob_name = "/".join(parsed_source_url.path.split("/")[2:])
        blob_path = f"{blob_name} raw transcripts.json"

        # Convert dict to JSON string and upload
        blob_client = blob_service_client.get_blob_client(container="call-recording-transcriptions", blob=blob_path)
        blob_client.upload_blob(json.dumps(file_response), overwrite=True, encoding='utf-8')

        logger.info(f"Uploaded transcription to Azure Blob Storage: {blob_path}")


def main():
    """Main execution pipeline for processing audio files and transcribing them."""
    logger.info("Fetching audio files...")
    audio_files = get_wav_files(container_client)

    if not audio_files:
        logger.warning("No audio files found. Exiting pipeline.")
        return

    logger.info("Generating SAS URLs...")
    sas_urls = [generate_sas_url(file) for file in audio_files]
    logger.info(f"Total audio files found: {len(sas_urls)}")

    logger.info("Starting transcription job...")
    transcription_id = start_transcription(sas_urls)

    if not transcription_id:
        logger.error("Failed to start transcription job. Exiting pipeline.")
        return

    logger.info(f"Monitoring transcription job: {transcription_id}")
    content_json = monitor_transcription(transcription_id)

    if not content_json or content_json.get("status") != "Succeeded":
        logger.error("Transcription job failed or did not complete successfully. Exiting pipeline.")
        return

    logger.info("Fetching and uploading transcripts...")
    fetch_and_upload_transcripts(content_json)

    logger.info("Pipeline execution completed.")


if __name__ == "__main__":
    main()

import os
import re
import json
import time
import warnings
import requests
import isodate
import pandas as pd
from tqdm import tqdm
from urllib.parse import urlparse
from datetime import datetime, timedelta
from dotenv import load_dotenv
from azure.storage.blob import BlobServiceClient, generate_blob_sas, BlobSasPermissions
from concurrent.futures import ThreadPoolExecutor

warnings.filterwarnings("ignore")
load_dotenv()

AZURE_STORAGE_CONNECTION_STRING = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
AZURE_SPEECH_API_ENDPOINT = os.getenv("AZURE_SPEECH_API_ENDPOINT")
AZURE_SPEECH_API_KEY = os.getenv("AZURE_SPEECH_API_KEY")
AZURE_STORAGE_KEY = os.getenv("AZURE_STORAGE_KEY")

blob_service_client = BlobServiceClient.from_connection_string(AZURE_STORAGE_CONNECTION_STRING, connection_verify=False)
container_client = blob_service_client.get_container_client("call-recording-transcriptions")


def get_raw_transcripts(container_client, path="", blob_urls=None):
    if blob_urls is None:
        blob_urls = []

    for blob in container_client.walk_blobs(name_starts_with=path):
        if "/" in blob.name[len(path):]:
            get_raw_transcripts(container_client, path=blob.name, blob_urls=blob_urls)
        else:
            blob_url = f"https://{container_client.account_name}.blob.core.windows.net/{container_client.container_name}/{blob.name}"
            blob_urls.append(blob_url)

    return blob_urls


def generate_sas_url(blob_url, sas_expiration=datetime.utcnow() + timedelta(hours=1)):
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

    return f"https://{account_name}.blob.core.windows.net/{container_name}/{blob_name}?{sas_token}"


def format_time(seconds):
    seconds = round(seconds)
    hours, remainder = divmod(seconds, 3600)
    minutes, sec = divmod(remainder, 60)
    
    parts = []
    if hours:
        parts.append(f"{hours} hours")
    if minutes:
        parts.append(f"{minutes} minutes")
    if sec or not parts:
        parts.append(f"{sec} seconds")
    
    return " ".join(parts)


def process_transcripts(transcript_data):
    data = []
    
    for phrase in tqdm(transcript_data.get('recognizedPhrases', []), desc="Processing transcripts"):
        confidence = phrase['nBest'][0]['confidence']
        if confidence >= 0.1:
            phrase_offset = isodate.parse_duration(phrase['offset'])
            phrase_duration = isodate.parse_duration(phrase['duration']).total_seconds()
            spoken_at_seconds = round(phrase_offset.total_seconds(), 5)
            phrase_duration_rounded = round(phrase_duration, 5)
            
            data.append({
                'timestamp': spoken_at_seconds,
                'duration': phrase_duration_rounded,
                'time_when_finished': spoken_at_seconds + phrase_duration_rounded,
                'channel': phrase['channel'],
                'display': phrase['nBest'][0]['display'],
                'confidence': confidence
            })
    
    if not data:
        print("❌ No recognized phrases found in the transcript data.")
        print(transcript_data)
        return ""

    df = pd.DataFrame(data).sort_values(by='time_when_finished')
    df['group'] = (df['channel'] != df['channel'].shift()).cumsum()
    
    df_new = df.groupby('group', as_index=False).agg({
        'timestamp': 'first',
        'duration': 'sum',
        'time_when_finished': 'last',
        'channel': 'first',
        'display': ' '.join,
        'confidence': 'mean'
    })
    
    df_new.drop(columns=['group'], inplace=True)
    df_new['readable time'] = df_new['timestamp'].apply(format_time)
    df_new["person"] = df_new['channel'].apply(lambda x: os.getenv("CONFIG_AUDIO_CHANNEL_0") if x == 0 else os.getenv("CONFIG_AUDIO_CHANNEL_1"))

    transcript_str = "\n".join(
        f"[{row['readable time']}][{row['person']}] : {row['display']}"
        for _, row in df_new.iterrows()
    )

    return transcript_str


def upload_transcripts_to_blob(transcript_str, blob_path):
    blob_client = blob_service_client.get_blob_client(container="call-recording-transcriptions-processed", blob=blob_path)
    blob_client.upload_blob(transcript_str, overwrite=True, encoding='utf-8')


def upload_file(file_url):
    # print(file_url)
    print()
    parsed_file_url = urlparse(file_url)
    blob_name = "/".join(parsed_file_url.path.split("/")[2:])[:-21]
    blob_path = f"{blob_name} processed transcripts.txt"

    response = requests.get(file_url, verify=False)
    if response.status_code == 200:
        transcript_data = response.json()
        transcript_str = process_transcripts(transcript_data)
        try:
            upload_transcripts_to_blob(transcript_str, blob_path)
            print(f"✅ Successfully uploaded: {blob_path}")
        except Exception as e:
            print(f"❌ Failed to upload {blob_path}: {e}")
    else:
        print(f"❌ Failed to fetch transcript: {file_url} - Status Code: {response.status_code}")


def main():
    files = [generate_sas_url(i) for i in get_raw_transcripts(container_client)]
    
    with ThreadPoolExecutor(max_workers=10) as executor:
        list(tqdm(executor.map(upload_file, files), total=len(files)))


if __name__ == "__main__":
    main()

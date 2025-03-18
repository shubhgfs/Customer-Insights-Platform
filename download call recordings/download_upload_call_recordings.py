import os
import sys
import json
import csv
import requests
from dotenv import load_dotenv
from tqdm import tqdm
from azure.storage.blob import BlobServiceClient
from azure.core.pipeline.transport import RequestsTransport

# Load environment variables
sys.path.append(r"C:\Users\shubhm01\Documents\Marketing AI\download call recordings")
load_dotenv()

# Import authentication module
from authorization import SERVER, getAuthHeader

# Azure Blob Storage setup
CONNECTION_STRING = os.getenv('CONNECTION_STRING')
CONTAINER_NAME = 'call-recordings'
BLOB_SERVICE_CLIENT = BlobServiceClient.from_connection_string(CONNECTION_STRING, connection_verify=False)


def download_and_upload_recording(transaction_id, brand_name, product_name, sale_status):
    """
    Downloads a call recording from Verint Cloud and uploads it to Azure Blob Storage.

    Parameters:
    - transaction_id (str): The unique interaction ID.
    - brand_name (str): Brand name associated with the call.
    - product_name (str): Product name related to the call.
    - sale_status (str): Sale status of the customer.
    """
    
    # Construct API URL
    url = f"https://wfo.mt3.verintcloudservices.com/api/recording/locator/v1/export/interactions/{transaction_id}"

    # Get authorization header
    auth_header = getAuthHeader(url.format(SERVER), "POST")
    headers = {
        'Authorization': f'{auth_header}',
        'Content-Type': 'application/json'
    }

    # API request payload
    payload = json.dumps({
        "async_response": False,
        "types": ["Audio"],
        "encrypted": False,
        "audio_format": "PCM",
        "screen_format": "as-recorded",
        "container_format": "wav"
    })

    # Send API request to download the recording
    response = requests.post(url, headers=headers, data=payload)

    if response.status_code == 200:
        # Define blob storage path
        blob_path = f"{brand_name}/{product_name}/{sale_status}/{transaction_id}.wav"
        print(f"Blob Path - {blob_path}")
        blob_client = BLOB_SERVICE_CLIENT.get_blob_client(container=CONTAINER_NAME, blob=blob_path)

        # Upload to Azure Blob Storage
        blob_client.upload_blob(response.content, overwrite=True)
        print(f"✅ Uploaded: {blob_path}")
    else:
        print(f"❌ Failed to download {transaction_id} | Status Code: {response.status_code}")
        print(response.text)


if __name__ == '__main__':
    # Path to CSV containing transaction IDs
    CSV_FILE_PATH = r"G:\Workgroups\Actuarial\Shubh\Marketing AI\Transaction IDs.csv"

    # Read CSV and process recordings
    with open(CSV_FILE_PATH, mode='r') as file:
        csv_reader = csv.DictReader(file)
        
        for row in tqdm(csv_reader, desc="Processing Transactions"):
            transaction_id = row['id']
            brand_name = row['BrandName']
            product_name = row['ProductName']
            sale_status = row['SaleStatus']
            
            print(f"Processing: {transaction_id} | {brand_name} | {product_name} | {sale_status}")
            download_and_upload_recording(transaction_id, brand_name, product_name, sale_status)
            
            # Remove `break` to process all records
            break
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
from fpdf import FPDF
import os

warnings.filterwarnings("ignore")
load_dotenv()

AZURE_STORAGE_CONNECTION_STRING = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
AZURE_STORAGE_KEY = os.getenv("AZURE_STORAGE_KEY")

blob_service_client = BlobServiceClient.from_connection_string(AZURE_STORAGE_CONNECTION_STRING, connection_verify=False)
container_client = blob_service_client.get_container_client("call-recording-transcriptions-processed")


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


def download_blob(blob_url, download_path):
    response = requests.get(blob_url, verify=False)
    with open(download_path, 'wb') as file:
        file.write(response.content)

def convert_txt_to_pdf(txt_file_path):
    if not os.path.isfile(txt_file_path):
        raise FileNotFoundError(f"The file {txt_file_path} does not exist.")

    with open(txt_file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    for line in lines:
        clean_line = line.encode('latin-1', 'ignore').decode('latin-1')
        pdf.multi_cell(0, 10, clean_line)

    base = os.path.splitext(txt_file_path)[0]
    pdf_file_path = f"{base}.pdf"

    pdf.output(pdf_file_path)
    print(f"PDF saved to {pdf_file_path}")


# blob_urls = get_raw_transcripts(container_client)
# print(blob_urls)
# blob_sas_urls = [generate_sas_url(url) for url in blob_urls]

# for url in blob_sas_urls:
#     file_name = url.split('?')[0] 
#     file = file_name.split('/')
#     brand, product, sale, file_name = file[-4], file[-3], file[-2], file[-1]
#     print(file_name)
#     download_path_file = os.path.join(f'{brand}/{product}/{sale}')
#     download_path = os.path.join(r'C:\Users\shubhm01\Documents\Customer Insights Platform\call transcriptions', download_path_file, file_name)
#     os.makedirs(os.path.dirname(download_path), exist_ok=True)
#     print(f"Downloading {file_name} to {download_path}")
#     download_blob(url, download_path)
#     print(f"Downloaded {file_name}")


all_kb = [
    [r'C:/Users/shubhm01/Documents/Customer Insights Platform/call transcriptions/ASIA/Life/No Sale', "asia_life_no_sale"],
    [r'C:/Users/shubhm01/Documents/Customer Insights Platform/call transcriptions/ASIA/Life/Sale', "asia_life_sale"],
    [r'C:/Users/shubhm01/Documents/Customer Insights Platform/call transcriptions/OneChoice/Life/Sale', "onechoice_life_sale"],
    [r'C:/Users/shubhm01/Documents/Customer Insights Platform/call transcriptions/OneChoice/Life/No Sale', "onechoice_life_no_sale"],
    [r'C:/Users/shubhm01/Documents/Customer Insights Platform/call transcriptions/OneChoice/Income Protection/Sale', "onechoice_income_protection_sale"],
    [r'C:/Users/shubhm01/Documents/Customer Insights Platform/call transcriptions/OneChoice/Income Protection/No Sale', "onechoice_income_protection_no_sale"],
    [r'C:/Users/shubhm01/Documents/Customer Insights Platform/call transcriptions/Real/Life/Sale', "real_life_sale"],
    [r'C:/Users/shubhm01/Documents/Customer Insights Platform/call transcriptions/Real/Life/No Sale', "real_life_no_sale"],
    [r'C:/Users/shubhm01/Documents/Customer Insights Platform/call transcriptions/Real/Funeral/Sale', "real_funeral_sale"],
    [r'C:/Users/shubhm01/Documents/Customer Insights Platform/call transcriptions/Real/Funeral/No Sale', "real_funeral_no_sale"],
    [r'C:/Users/shubhm01/Documents/Customer Insights Platform/call transcriptions/Real/Income Protection/Sale', "real_income_protection_sale"],
    [r'C:/Users/shubhm01/Documents/Customer Insights Platform/call transcriptions/Real/Income Protection/No Sale', "real_income_protection_no_sale"],
]

for index in tqdm(all_kb):
    path = index[0]
    for files in tqdm(os.listdir(path)):
        if files.endswith('.txt'):
            convert_txt_to_pdf(os.path.join(path, files))
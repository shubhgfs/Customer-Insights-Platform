import requests
from dotenv import load_dotenv
import os
import warnings
warnings.filterwarnings("ignore")

load_dotenv()

def get_transcription_jobs(api_key, endpoint):
    url = f"{endpoint}/speechtotext/v3.2-preview.2/transcriptions"
    headers = {
        "Ocp-Apim-Subscription-Key": api_key
    }
    response = requests.get(url, verify=False, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        response.raise_for_status()

def get_transcription_ids(transcriptions):
    return [transcription['self'] for transcription in transcriptions['values']]

def get_transcription_files(api_key, endpoint, transcription_id):
    url = f"{endpoint}/speechtotext/v3.2-preview.2/transcriptions/{transcription_id}/files"
    headers = {
        "Ocp-Apim-Subscription-Key": api_key
    }
    total_files = []
    while url:
        response = requests.get(url, verify=False, headers=headers)
        if response.status_code == 200:
            data = response.json()
            total_files.extend(data['values'])
            url = data.get('@nextLink')
        else:
            response.raise_for_status()
    return total_files

# Example usage
if __name__ == "__main__":
    api_key = os.getenv("AZURE_SPEECH_API_KEY")
    endpoint = os.getenv("AZURE_SPEECH_API_ENDPOINT")
    transcriptions = get_transcription_jobs(api_key, endpoint)
    transcription_ids = get_transcription_ids(transcriptions)
    print(transcription_ids)
    print(len(transcription_ids))
    print()
    
    total_file_count = 0
    for transcription_id in transcription_ids:
        print()
        print(transcription_id)
        files = get_transcription_files(api_key, endpoint, transcription_id.split('/')[-1])
        print(f'Number of files for {transcription_id} : {len(files)}')
        total_file_count += len(files)
    print(f"Total number of files: {total_file_count}")



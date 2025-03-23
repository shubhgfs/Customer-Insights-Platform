import requests
import json

# Set the base URL and headers
base_url = "https://gfsai.happyhill-36e531d5.australiaeast.azurecontainerapps.io/api"
gpu_base_url = "http://localhost:3000/api"
headers = {
    "Authorization": "Bearer sk-f3221ccd644446098efb8498f4020050",
    "Cache-Control": "no-cache",
    "User-Agent": "PostmanRuntime/7.39.1",
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive"
}

# 1. GET Request for models
def get_models(use_gpu=False):
    models_url = f"{gpu_base_url if use_gpu else base_url}/models"
    response = requests.get(models_url, headers=headers, verify=False)
    if response.status_code == 200:
        print("Models retrieved successfully:", response.json())
    else:
        print(f"Failed to retrieve models: {response.status_code}, {response.text}")

# 2. POST Request for chat completions
def chat_completion(system_prompt, user_prompt, use_gpu=False):
    chat_url = f"{gpu_base_url if use_gpu else base_url}/chat/completions"
    payload = {
        "model": "qwq:latest",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
    }
    response = requests.post(chat_url, headers=headers, json=payload, verify=False)
    if response.status_code == 200:
        print("Chat response:", response.json())
    else:
        print(f"Failed to get chat completion: {response.status_code}, {response.text}")

# Example usage
if __name__ == "__main__":
    # Fetch models from GPU
    get_models(use_gpu=True)

    # Define system and user prompts
    system_prompt = "You are an AI assistant."
    user_prompt = "Why is the sky blue?"

    # Get chat response from GPU
    chat_completion(system_prompt, user_prompt, use_gpu=True)

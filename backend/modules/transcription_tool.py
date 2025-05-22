import openai
import os
from agno.tools import Toolkit
import json
from backend.modules.constants import *

CONFIG_PATH = "backend/json files/transcription_tool_config.json"

class TranscriptionSearchTool(Toolkit):
    def __init__(self, **kwargs):
        # Load config from JSON
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            self.config = json.load(f)

        super().__init__(name='transcription_search_tool', **kwargs)

        self.client = openai.AzureOpenAI(
            api_key=AZURE_API_KEY_AQMAGENTICOS,
            azure_endpoint=AZURE_ENDPOINT_AQMAGENTICOS,
            api_version=AZURE_OPENAI_API_VERSION_AQMAGENTICOS,
        )
        self.deployment = AZURE_OPENAI_DEPLOYMENT_ID_AQMAGENTICOS
        self.register(self.select_index)
        self.register(self.search_transcriptions)
    
    def select_index(self, query: str) -> str:

        print('Calling select index tool')

        functions = self.config['select_index']['functions']
        system_prompt = self.config['select_index']['system_prompt']

        # LLM call with system context
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Query: {query}"}
        ]

        response = self.client.chat.completions.create(
            model=self.deployment,
            messages=messages,
            functions=functions,
            function_call={"name": "choose_index"},
        )

        # Extract and validate response
        function_args = response.choices[0].message.function_call.arguments

        index_name = json.loads(function_args)["index_name"]

        print('Returned index name:', index_name)

        return index_name

    def search_transcriptions(self, query: str) -> str:

        print('Calling search transcriptions tool')

        selected_index = self.select_index(query)
        
        if not selected_index:
            return "No valid index could be determined for the query. Please try rephrasing or check brand/product/sale intent."

        # System message to tightly control LLM behavior
        system_prompt = self.config['search_transcriptions']['system_prompt']

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": query}
        ]

        response = self.client.chat.completions.create(
            model=self.deployment,
            messages=messages,
            extra_body={
                "data_sources": [{
                    "type": "azure_search",
                    "parameters": {
                        "endpoint": AZURE_AI_SEARCH_ENDPOINT,
                        "index_name": selected_index,
                        "authentication": {
                            "type": "api_key",
                            "key": AZURE_AI_SEARCH_API_KEY,
                        }
                    }
                }],
            }
        )

        # Extract message + transcriptions
        answer = response.choices[0].message.content
        transcriptions = response.choices[0].message.model_extra.get("context", {}).get("citations", [])

        print("Answer:", answer)
        print("Transcriptions:", transcriptions)

        return {
            "answer": answer,
            "transcriptions": transcriptions
        }

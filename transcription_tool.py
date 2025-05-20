import openai
import os
from agno.tools import Toolkit
import json
import uuid

class TranscriptionSearchTool(Toolkit):
    name = "TranscriptionSearchTool"
    description = "Selects the right index and searches transcription data using Azure AI Search."

    def __init__(self, deployment: str, system_prompt: str):
        self.client = openai.AzureOpenAI(
            api_key=os.getenv("AZURE_OPENAI_API_KEY_AQMAGENTICOS"),
            azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT_AQMAGENTICOS"),
            api_version="2024-12-01-preview",
        )
        self.deployment = deployment
        self.system_prompt = system_prompt

    def extract_and_format_citations(self, all_citations):
        citations_formatted = {}
        
        for i, citation in enumerate(all_citations):
            doc_id = f'doc{i+1}_{str(uuid.uuid4().hex)[:16]}'
            date = citation['filepath'][:12]
            year, month, day, time = date[:4], date[4:6], date[6:8], date[8:10] + '.' + date[10:]
            context = citation['content'].replace(citation['title'], '').strip()
            context = context[:context.rfind('.')] if context.rfind('.') != -1 else context
            if context[0] != '[':
                context = context[context.find('['):]
            citations_formatted[doc_id] = {
                'Date': f'{year}-{month}-{day} {time}',
                'Context': context
            }
        
        return citations_formatted
    
    def select_index(self, query: str) -> str:
        """
        Use an LLM to choose the correct index name from a predefined list.
        Returns a strictly valid index name.
        """

        # Valid index choices
        valid_indexes = [
            "asia_life_no_sale",
            "asia_life_sale",
            "onechoice_life_sale",
            "onechoice_life_no_sale",
            "onechoice_income_protection_sale",
            "onechoice_income_protection_no_sale",
            "real_life_sale",
            "real_life_no_sale",
            "real_funeral_sale",
            "real_funeral_no_sale",
            "real_income_protection_sale",
            "real_income_protection_no_sale",
        ]

        # Define function schema
        functions = [
            {
                "name": "choose_index",
                "description": "Return the most relevant Azure Search index name for the given query.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "index_name": {
                            "type": "string",
                            "enum": valid_indexes,
                            "description": "The selected index name from the allowed list."
                        }
                    },
                    "required": ["index_name"]
                }
            }
        ]

        messages = [
            {"role": "system", "content": "You are an expert assistant helping to choose the most relevant Azure Search index."},
            {"role": "user", "content": f"Query: {query}"}
        ]

        response = self.client.chat.completions.create(
            model=self.deployment,
            messages=messages,
            functions=functions,
            function_call={"name": "choose_index"},
            temperature=0,
        )

        # Extract from function_call result
        index_name = response.choices[0].message.function_call.arguments
        index_name = json.loads(index_name)["index_name"]

        return index_name

    def search_transcriptions(self, query: str) -> str:
        """
        Run the user query against Azure AI Search using the selected index.
        """
        selected_index = self.select_index(query)

        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": query}
        ]

        response = self.client.chat.completions.create(
            model=self.deployment,
            messages=messages,
            temperature=0,
            extra_body={
                "data_sources": [{
                    "type": "azure_search",
                    "parameters": {
                        "endpoint": os.environ["AZURE_AI_SEARCH_ENDPOINT"],
                        "index_name": selected_index,
                        "authentication": {
                            "type": "api_key",
                            "key": os.environ["AZURE_AI_SEARCH_API_KEY"],
                        },
                        "role_information": self.system_prompt
                    }
                }],
            }
        )

        citations = response.choices[0].message.model_extra.get("context", {}).get("citations", [])
    
        if citations:
            citations_formatted = self.extract_and_format_citations(citations)
        else:
            citations_formatted = {}

        return (response.choices[0].message.content, citations_formatted)

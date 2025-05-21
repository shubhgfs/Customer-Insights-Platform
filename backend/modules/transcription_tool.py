import openai
import os
from agno.tools import Toolkit
import json
from backend.modules.constants import *

class TranscriptionSearchTool(Toolkit):
    def __init__(self, **kwargs):

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
        """
        Use an LLM to choose the correct index name from a predefined list.
        Returns a strictly valid index name or refuses if not possible.
        """

        valid_indexes = [
            "asia-life-nosale",
            "asia-life-sale",
            "onechoice-incomeprotection-nosale",
            "onechoice-incomeprotection-sale",
            "onechoice-life-nosale",
            "onechoice-life-sale",
            "real-funeral-nosale",
            "real-funeral-sale",
            "real-incomeprotection-nosale",
            "real-incomeprotection-sale",
            "real-life-nosale",
            "real-life-sale",
        ]

        system_prompt = """
    You are an expert assistant tasked with selecting the most appropriate index name from a predefined list.

    Each index name is a combination of:
    1. **Brand**: 'asia', 'onechoice', or 'real'
    2. **Product**: 'life', 'incomeprotection', or 'funeral'
    3. **Sale status**: 'sale' or 'nosale'

    The format is: `<brand>-<product>-<sale_status>`, all lowercase.

    The user query may mention any combination of brand, product, or sale intent. Based on this, select the best matching index name from the provided enum list. Only return a valid match if it exactly maps to one of the 12 allowed index names.

    If no clear match exists, **do not select anything**.

    Examples:
    - "What happened in Real Life Sale calls?" → real-life-sale
    - "Insights from OneChoice income protection where no sale happened" → onechoice-incomeprotection-nosale
    - "Funeral insurance no-sale data for Real brand" → real-funeral-nosale

    **Do not guess.** If the brand or product is missing, ambiguous, or mismatched, return nothing.
    """

        functions = [
            {
                "name": "choose_index",
                "description": "Return the most relevant index name from the 12 allowed options based on the user query.",
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
        return index_name

    def search_transcriptions(self, query: str) -> str:
        """
        This tool searches call transcription data stored in Azure AI Search vector indexes.
        It:
        1. Selects the appropriate index using brand-product-sale classification.
        2. Uses the query to retrieve relevant transcript chunks (citations).
        3. Extracts grounded insights such as customer intent, agent behavior, call outcome, and sentiments.
        4. Returns a factual summary based ONLY on the retrieved citations.
        """

        selected_index = self.select_index(query)
        
        if not selected_index:
            return "No valid index could be determined for the query. Please try rephrasing or check brand/product/sale intent."

        # System message to tightly control LLM behavior
        system_prompt = """
    You are a Transcription Intelligence Agent built to analyze and summarize insights from customer-sales agent call transcriptions stored in vector indexes (Azure AI Search).

    Your task:
    1. Use the user’s query and retrieved transcript citations to determine the purpose and outcome of the call.
    2. Summarize:
    - The customer's **intent or sentiment**
    - The agent's **response or persuasion**
    - The **outcome** (sale/no sale, confusion, objections, interest, etc.)
    3. Cite only factual information that is present in the retrieved transcript snippets.
    4. Do NOT make up or assume anything that is not in the retrieved citations.
    5. If no meaningful insight is found, state that clearly.

    Be concise but insightful. Your summary must reflect what the actual conversation shows.
    """

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

        # Extract message + citations
        answer = response.choices[0].message.content
        citations = response.choices[0].message.model_extra.get("context", {}).get("citations", [])

        print("Answer:", answer)
        print("Citations:", citations)

        return (answer, citations)
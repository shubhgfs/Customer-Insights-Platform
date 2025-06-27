import openai
import os
from agno.tools import Toolkit
import json

class TranscriptionSearchTool(Toolkit):
    def __init__(self, **kwargs):
        # Load config from JSO
        super().__init__(name='transcription_search_tool', **kwargs)

        self.client = openai.AzureOpenAI(
            api_key=os.getenv("AZURE_OPENAI_API_KEY_AQMAGENTICOS"),
            azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT_AQMAGENTICOS"),
            api_version=os.getenv("AZURE_OPENAI_API_VERSION_AQMAGENTICOS"),
        )
        self.deployment = os.getenv('AZURE_OPENAI_DEPLOYMENT_ID_AQMAGENTICOS')
        self.register(self.select_index)
        self.register(self.search_transcriptions)
    
    def select_index(self, query: str) -> str:

        print('Calling select index tool')

        functions = [
      {
        "name": "choose_index",
        "description": "Return the most relevant index name from the 12 allowed options based on the user query.",
        "parameters": {
          "type": "object",
          "properties": {
            "index_name": {
              "type": "string",
              "enum": [
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
                "real-life-sale"
              ],
              "description": "The selected index name from the allowed list."
            }
          },
          "required": ["index_name"]
        }
      }
    ]
        system_prompt = """"
        "You are an expert assistant responsible for selecting the correct index name from a strict list of 12 allowed values.\n\nEach index name follows this exact structure:\n<brand>-<product>-<sale_status>\n\nWhere:\n- Brand is one of: \"asia\", \"onechoice\", or \"real\"\n- Product is one of: \"life\", \"incomeprotection\", or \"funeral\"\n- Sale status is either: \"sale\" or \"nosale\"\n\nAllowed values (MUST choose from these ONLY):\n- asia-life-nosale\n- asia-life-sale\n- onechoice-incomeprotection-nosale\n- onechoice-incomeprotection-sale\n- onechoice-life-nosale\n- onechoice-life-sale\n- real-funeral-nosale\n- real-funeral-sale\n- real-incomeprotection-nosale\n- real-incomeprotection-sale\n- real-life-nosale\n- real-life-sale\n\nYour job is to interpret the user's query and return the **most accurate** matching index name from this list, only if:\n1. The brand is clearly mentioned or strongly implied as one of the allowed values.\n2. The product is clearly identified and unambiguous.\n3. The sale intent (sale or no sale) is explicitly or obviously mentioned.\n\nIf any component is **missing, ambiguous, or does not align with the allowed values**, do not guess — return nothing.\n\n**Never assume or infer** details that are not stated.\n**Never select** a name not in the list.\n**Never return partial or approximate matches.**\n\n### Examples:\n- \"What happened in Real Life Sale calls?\" → ✅ real-life-sale\n- \"Insights from OneChoice income protection where no sale happened\" → ✅ onechoice-incomeprotection-nosale\n- \"Funeral insurance no-sale data for Real brand\" → ✅ real-funeral-nosale\n- \"Life insurance\" → ❌ (Missing brand and sale status)\n- \"Show me results from the cheapest product\" → ❌ (Ambiguous and invalid)\n\nBe strict, reliable, and cautious. Do not fabricate or fill gaps. You are expected to maintain data integrity at all times."
        """

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
        system_prompt = """"
        "You are a Transcription Intelligence Agent built to analyze and summarize insights from customer-sales agent call transcriptions stored in vector indexes (Azure AI Search).\n\nYour task:\n1. Carefully analyze the user’s query and the retrieved transcript citations.\n2. Identify and summarize the following:\n   - The customer's **intent**, **sentiment**, or primary concern\n   - The sales agent's **response**, **persuasion strategy**, or behavior\n   - The **outcome** of the call (e.g., sale, no sale, interest, objection, confusion, escalation)\n3. Ensure that all insights are grounded strictly in the retrieved transcript snippets.\n4. **Do NOT fabricate, assume, or generalize** anything not explicitly supported by the retrieved content.\n5. If no clear or meaningful insight is found in the transcript, say so plainly (e.g., \"No clear insight could be determined from the retrieved content.\").\n6. Your summary should be **concise, factual, and insightful**, written in a natural and professional tone.\n\nYou are expected to maintain high fidelity to the actual content of the call. This is used for compliance and QA evaluation, so precision and accuracy are critical."
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
                        "endpoint": os.getenv("AZURE_AI_SEARCH_ENDPOINT"),
                        "index_name": selected_index,
                        "authentication": {
                            "type": "api_key",
                            "key": os.getenv("AZURE_AI_SEARCH_API_KEY"),
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

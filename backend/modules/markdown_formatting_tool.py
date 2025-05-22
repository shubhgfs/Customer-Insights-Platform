import openai
import json
from agno.tools import Toolkit
from backend.modules.constants import *

CONFIG_PATH = "backend/json files/markdown_formatting_tool_config.json"

class MarkdownFormattingTool(Toolkit):
    def __init__(self, **kwargs):
        # Load config from JSON
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            self.config = json.load(f)

        super().__init__(
            name='markdown_formatting_tool',
            # description=self.config["description"],
            **kwargs
        )

        self.client = openai.AzureOpenAI(
            api_key=AZURE_API_KEY_AQMAGENTICOS,
            azure_endpoint=AZURE_ENDPOINT_AQMAGENTICOS,
            api_version=AZURE_API_VERSION,
        )
        self.deployment = AZURE_DEPLOYMENT_O3

        # self.register(self.list_tools)
        self.register(self.call)

    # def list_tools(self):
    #     tool = self.config["tool"]
    #     return [
    #         ToolCall(
    #             name=tool["name"],
    #             description=tool["description"],
    #             parameters=tool["parameters"]
    #         )
    #     ]

    def call(self, tool_name, arguments):
        if tool_name != self.config["tool"]["name"]:
            raise ValueError("Unknown tool name")

        raw_text = arguments.get("raw_response", "")

        completion = self.client.chat.completions.create(
            model=self.deployment,
            messages=[
                {"role": "system", "content": self.config["system_prompt"]},
                {"role": "user", "content": raw_text}
            ],
            temperature=0.4,
        )

        return completion.choices[0].message.content

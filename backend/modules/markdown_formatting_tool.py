import openai
import json
from agno.tools import Toolkit
from backend.modules.constants import *

CONFIG_PATH = "backend/markdown files/markdown_formatting_tool.md"

class MarkdownFormattingTool(Toolkit):
    def __init__(self, **kwargs):
        # Load config from JSON
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            self.system_prompt = f.read()

        super().__init__(
            name='markdown_formatting_tool',
            # description=self.config["description"],
            **kwargs
        )

        self.client = openai.AzureOpenAI(
            api_key=AZURE_API_KEY_AQMAGENTICOS,
            azure_endpoint=AZURE_ENDPOINT_AQMAGENTICOS,
            api_version=AZURE_OPENAI_API_VERSION_AQMAGENTICOS,
        )
        self.deployment = AZURE_OPENAI_DEPLOYMENT_ID_AQMAGENTICOS

        # self.register(self.list_tools)
        self.register(self.format_markdown)

    # def list_tools(self):
    #     tool = self.config["tool"]
    #     return [
    #         ToolCall(
    #             name=tool["name"],
    #             description=tool["description"],
    #             parameters=tool["parameters"]
    #         )
    #     ]

    def format_markdown(self, arguments):

        print('Calling markdown formatting tool')
        print('System prompt:', self.system_prompt)
        print(f'arguments: {arguments}')

        # If arguments is a dict with 'text', extract it
        if isinstance(arguments, dict) and 'text' in arguments:
            user_content = arguments['text']
        elif isinstance(arguments, dict) and 'content' in arguments:
            user_content = arguments['content']
        else:
            user_content = str(arguments)

        completion = self.client.chat.completions.create(
            model=self.deployment,
            messages=[
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": user_content}
            ]
        )

        return completion.choices[0].message.content

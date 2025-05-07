from agno.agent import Agent
from agno.models.azure import AzureOpenAI
from agno.tools.sql import SQLTools
import os
from dotenv import load_dotenv
from agno.playground import Playground, serve_playground_app

# Load environment variables from a .env file
load_dotenv()

# Set Azure OpenAI credentials
api_key = os.getenv("AZURE_OPENAI_API_KEY_AQMAGENTICOS")
azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT_AQMAGENTICOS")
azure_deployment = "o3-mini"
api_version = "2024-12-01-preview"

print(api_key, azure_endpoint)

# Initialize the Azure OpenAI model
azure_model = AzureOpenAI(
    api_key=api_key,
    azure_endpoint=azure_endpoint,
    azure_deployment=azure_deployment,
    api_version=api_version
)

# Specify the path to your SQLite database file
lifestyle_db = r"sqlite:////home/shubh/Documents/Customer Insights Platform/lifestyle_smoking_cip.db"
underwriting_db = r"sqlite:////home/shubh/Documents/Customer Insights Platform/underwriting_impact_cip.db"

underwriting_tool = SQLTools(db_url=underwriting_db)
lifestyle_tool = SQLTools(db_url=lifestyle_db)

tools = [lifestyle_tool, underwriting_tool]
tool2 = [underwriting_tool, lifestyle_tool]

# Initialize the agent with the Azure model and SQLTools
agent = Agent(
    name="SQL Analyst Agent",
    model=azure_model,
    tools=tools,
)

# Use the agent to interact with the database
agent.print_response(
    "lIST ALL THE TABLES YOU HAVE USING THE LIST TABLE TOOL"
)

# app = Playground(agents = [agent]).get_app()

# if __name__ == "__main__":
#     # Run the app
#     serve_playground_app("agno_test:app", reload=True)
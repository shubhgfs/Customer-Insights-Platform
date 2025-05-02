from agno.agent import Agent
from agno.tools.sql import SQLTools
import os
from dotenv import load_dotenv

load_dotenv()

os.environ["OPENAI_API_KEY"] = os.getenv("AZURE_OPENAI_API_KEY_AQMAGENTICOS")

# Specify the path to your SQLite database file
db_url = r"sqlite:///C:\Users\shubhm01\Documents\Customer Insights Platform\output.sqlite.db"

# Initialize the agent with the SQLTools
agent = Agent(tools=[SQLTools(db_url=db_url)])

# Use the agent to interact with the database
agent.print_response(
    "List the tables in the database. Tell me about contents of one of the tables",
    markdown=True,
)

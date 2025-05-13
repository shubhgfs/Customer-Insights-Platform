from agno.agent import Agent
from agno.models.azure import AzureOpenAI
from agno.tools.sql import SQLTools
import os
from agno.tools.reasoning import ReasoningTools
from dotenv import load_dotenv
from agno.playground import Playground, serve_playground_app
import httpx
from agno.vectordb.search import SearchType
from agno.vectordb.weaviate import Distance, VectorIndex, Weaviate
from agno.knowledge.json import JSONKnowledgeBase
import json
from agno.storage.sqlite import SqliteStorage



storage = SqliteStorage(
    table_name="tblMaster_CIP",
    db_file="tmp_usr.db",
)

# Import and read context from JSON file
with open(r'agent_config.json', 'r') as f:
    file = json.load(f)
    agent_config = file['agent_config']

http = httpx.Client(verify=False)

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
    api_version=api_version,
    # http_client=http
)

vector_db = Weaviate(
    collection="master",
    search_type=SearchType.hybrid,
    distance=Distance.COSINE,
    vector_index=VectorIndex.HNSW,
    local=True,
    )

knowledge_base = JSONKnowledgeBase(
    path = r"knowledge",
    vector_db=vector_db,)


# Specify the path to your SQLite database file
master_db = r"sqlite:////home/shubh/Documents/Customer Insights Platform/tblMaster_CIP.db"
sql_tool = SQLTools(db_url=master_db)

# Initialize the agent with the Azure model and SQLTools
agent = Agent(
    name="SQL Analyst Agent",
    model=azure_model,
    tools=[sql_tool, ReasoningTools(add_instructions=True)],
    system_message_role="system",
    system_message=agent_config.get('system_message', None),
    description=agent_config.get('description', None),
    goal=agent_config.get('goal', None),
    instructions=agent_config.get('instructions', None),
    expected_output=agent_config.get('expected_output', None),
    context=agent_config.get('context', None),
    add_context=True,
    resolve_context=True,
    add_history_to_messages=True,
    num_history_runs=10,
    read_chat_history=True,
    read_tool_call_history=True,
    markdown=True,
    add_name_to_instructions=True,
    add_datetime_to_instructions=True,
    timezone_identifier="Australia/Sydney",
    add_state_in_messages=False,
    monitoring=True,
    search_knowledge=True,
    knowledge=knowledge_base,
    storage=storage,
)


# Use the agent to interact with the database
# agent.print_response(
#     "lIST ALL THE TABLES YOU HAVE USING THE LIST TABLE TOOL"
# )

app = Playground(agents = [agent]).get_app()

if __name__ == "__main__":
    # Run the app
    serve_playground_app("agno_test:app", reload=True)
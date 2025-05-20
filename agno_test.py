import json
import os
from dotenv import load_dotenv
from agno.agent import Agent
from agno.knowledge.json import JSONKnowledgeBase
from agno.models.azure import AzureOpenAI
from agno.playground import Playground, serve_playground_app
from agno.storage.sqlite import SqliteStorage
from agno.tools.knowledge import KnowledgeTools
from agno.tools.reasoning import ReasoningTools
from agno.tools.sql import SQLTools
from agno.tools.thinking import ThinkingTools
from agno.vectordb.search import SearchType
from agno.vectordb.weaviate import Distance, VectorIndex, Weaviate

storage = SqliteStorage(
    table_name="tblMaster_CIP",
    db_file="tmp_usr.db",
)

with open(r'sql_agent_config.json', 'r') as f:
    file = json.load(f)
    sql_agent_config = file['agent_config']

load_dotenv()

api_key = os.getenv("AZURE_OPENAI_API_KEY_AQMAGENTICOS")
azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT_AQMAGENTICOS")
azure_deployment = "o3-mini"
api_version = "2024-12-01-preview"

print(api_key, azure_endpoint)

azure_model = AzureOpenAI(
    api_key=api_key,
    azure_endpoint=azure_endpoint,
    azure_deployment=azure_deployment,
    api_version=api_version,
)

vector_db = Weaviate(
    collection="master",
    search_type=SearchType.hybrid,
    distance=Distance.COSINE,
    vector_index=VectorIndex.HNSW,
    # local=True,
)

knowledge_base = JSONKnowledgeBase(
    path = r"knowledge",
    vector_db=vector_db,)

knowledge_tool = KnowledgeTools(
        knowledge=knowledge_base,
        think=True,
        search=True,
        analyze=True,
        instructions=sql_agent_config.get('instructions', None),
        add_instructions=True,
        add_few_shot=True,
)

thinking_tool = ThinkingTools(
    think=True,
    instructions=sql_agent_config.get('instructions', None),
    add_instructions=True,
)

master_db = r"sqlite:///tblMaster_CIP.db"
sql_tool = SQLTools(db_url=master_db)

agent = Agent(
    name="SQL Analyst Agent",
    model=azure_model,
    tools=[
        sql_tool,
        ReasoningTools(add_instructions=True),
        knowledge_tool,
        thinking_tool,
    ],
    context=sql_agent_config.get('context', None),
    add_context=True,
    resolve_context=True,
    add_history_to_messages=True,
    num_history_runs=10,
    knowledge=knowledge_base,
    search_knowledge=True,
    update_knowledge=True,
    add_references=True,
    storage=storage,
    show_tool_calls=True,
    reasoning=False,
    read_chat_history=True,
    read_tool_call_history=True,
    system_message_role="system",
    system_message=sql_agent_config.get('system_message', None),
    description=sql_agent_config.get('description', None),
    goal=sql_agent_config.get('goal', None),
    instructions=sql_agent_config.get('instructions', None),
    expected_output=sql_agent_config.get('expected_output', None),
    markdown=True,
    add_name_to_instructions=True,
    add_datetime_to_instructions=True,
    timezone_identifier="Australia/Sydney",
    add_state_in_messages=True,
    monitoring=True,
)

app = Playground(agents = [agent]).get_app()


if __name__ == "__main__":
    serve_playground_app("agno_test:app", host="0.0.0.0", port=7777, reload=True)

import json
import os
import openai
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
from agno.knowledge.combined import CombinedKnowledgeBase
from agno.vectordb.weaviate import Distance, VectorIndex, Weaviate
from agno.team.team import Team
from agno.embedder.azure_openai import AzureOpenAIEmbedder
from transcription_tool import TranscriptionSearchTool

load_dotenv()

embedder = AzureOpenAIEmbedder(
    api_key=os.getenv("AZURE_EMBEDDER_OPENAI_API_KEY"),
    api_version="2024-12-01-preview",
    azure_endpoint=os.getenv("AZURE_EMBEDDER_OPENAI_ENDPOINT"),
    azure_deployment="text-embedding-3-large"
)

storage_sql_agent = SqliteStorage(
    table_name="tblMaster_CIP",
    db_file="tmp_sql_agent.db",
)

storage_transcription_agent = SqliteStorage(
    table_name="tblMaster_CIP",
    db_file="tmp_transcription_agent.db",
)

storage_cip_team = SqliteStorage(
    table_name="tblMaster_CIP",
    db_file="tmp_cip_team.db",
)

with open(r'sql_agent_config.json', 'r') as f:
    file = json.load(f)
    sql_agent_config = file['agent_config']

with open(r'transcription_agent_config.json', 'r') as f:
    file = json.load(f)
    transcription_agent_config = file['agent_config']

with open(r'cip_team_config.json', 'r') as f:
    file = json.load(f)
    cip_team_config = file['team_config']

azure_model = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY_AQMAGENTICOS"),
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT_AQMAGENTICOS"),
    azure_deployment="o3-mini",
    api_version="2024-12-01-preview",
)


#######################################################################
####################     SQL AGENT     ################################
#######################################################################

sql_collection = Weaviate(
    collection="sql_collection",
    search_type=SearchType.hybrid,
    distance=Distance.COSINE,
    vector_index=VectorIndex.HNSW,
    local=True,
    embedder=embedder,
    )

sql_knowledge_base = JSONKnowledgeBase(
    path = r"knowledge",
    vector_db=sql_collection
)

sql_knowledge_tool = KnowledgeTools(
        knowledge=sql_knowledge_base,
        think=True,
        search=True,
        analyze=True,
        instructions=sql_agent_config.get('instructions', None),
        add_instructions=True,
        add_few_shot=True,
)

sql_thinking_tool = ThinkingTools(
    think=True,
    instructions=sql_agent_config.get('instructions', None),
    add_instructions=True,
)

sql_agent = Agent(
    name="SQL Analyst Agent",
    model=azure_model,
    tools=[
        SQLTools(db_url= r"sqlite:///tblMaster_CIP.db"),
        ReasoningTools(add_instructions=True),
        sql_knowledge_tool,
        sql_thinking_tool,
    ],
    context=sql_agent_config.get('context', None),
    add_context=True,
    resolve_context=True,
    add_history_to_messages=True,
    num_history_runs=10,
    knowledge=sql_knowledge_base,
    search_knowledge=True,
    update_knowledge=True,
    add_references=True,
    storage=storage_sql_agent,
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


#######################################################################
####################     TRANSCRIPTION AGENT     ######################
#######################################################################

transcription_agent = Agent(
    name="Transcription Agent",
    model=azure_model,
    tools=[
        TranscriptionSearchTool(
            deployment="o3-mini",
            system_prompt=transcription_agent_config.get('system_prompt', None),)],
    context=transcription_agent_config.get('context', None),
    add_context=True,
    resolve_context=True,
    add_history_to_messages=True,
    num_history_runs=10,
    knowledge=sql_knowledge_base,
    search_knowledge=True,
    update_knowledge=True,
    add_references=True,
    storage=storage_sql_agent,
    show_tool_calls=True,
    reasoning=False,
    read_chat_history=True,
    read_tool_call_history=True,
    system_message_role="system",
    system_message=transcription_agent_config.get('system_message', None),
    description=transcription_agent_config.get('description', None),
    goal=transcription_agent_config.get('goal', None),
    instructions=transcription_agent_config.get('instructions', None),
    expected_output=transcription_agent_config.get('expected_output', None),
    markdown=True,
    add_name_to_instructions=True,
    add_datetime_to_instructions=True,
    timezone_identifier="Australia/Sydney",
    add_state_in_messages=True,
    monitoring=True,
)

#######################################################################
###########################     TEAM     ##############################
#######################################################################


# master_collection = Weaviate(
#         collection="master_collection",
#         search_type=SearchType.hybrid,
#         distance=Distance.COSINE,
#         vector_index=VectorIndex.HNSW,
#         embedder=embedder,
#         # local=True,
#     )

# all_knowledge_bases = CombinedKnowledgeBase(
#     sources=[
#         sql_knowledge_base,
#         # transcription_knowledge_bases,
#     ],
#     vector_db=master_collection
# )

customer_insight_team = Team(
    name="Customer Insight Team",
    mode="coordinate",
    model=azure_model, 
    members=[
        # sql_agent,
        transcription_agent,
    ],
    show_tool_calls=True,
    markdown=True,
    description=cip_team_config.get('description', None),
    instructions=cip_team_config.get('instructions', None),
    expected_output=cip_team_config.get('expected_output', None),
    context=cip_team_config.get('context', None),
    success_criteria=cip_team_config.get('success_criteria', None),
    show_members_responses=True,
    add_datetime_to_instructions=True,
    add_member_tools_to_system_message=True,
    add_context=True,
    # knowledge=all_knowledge_bases,
    enable_agentic_context=True,
    share_member_interactions=True,
    get_member_information_tool=True,
    search_knowledge=True,
    read_team_history=True,
    enable_team_history=True,
    num_history_runs=10,
    storage=storage_cip_team,
)

app = Playground(agents=[transcription_agent], teams=[customer_insight_team]).get_app()

if __name__ == "__main__":
    serve_playground_app("agno_test:app", port=7777, reload=True)


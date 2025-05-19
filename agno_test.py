import json
import os
from dotenv import load_dotenv
from agno.agent import Agent
from agno.knowledge.pdf import PDFKnowledgeBase
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
from agno.vectordb.chroma import ChromaDb
from agno.embedder.azure_openai import AzureOpenAIEmbedder

load_dotenv()

os.environ["AZURE_EMBEDDER_OPENAI_API_KEY"] = os.getenv("AZURE_OPENAI_API_KEY_AQMAGENTICOS")
os.environ["AZURE_EMBEDDER_OPENAI_ENDPOINT"] = os.getenv("AZURE_OPENAI_ENDPOINT_AQMAGENTICOS")
os.environ["AZURE_EMBEDDER_DEPLOYMENT"] = "gpt-4o-mini"

embedder = AzureOpenAIEmbedder()

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

sql_knowledge_base = JSONKnowledgeBase(
    path = r"knowledge",
    vector_db=Weaviate(
    collection="master",
    search_type=SearchType.hybrid,
    distance=Distance.COSINE,
    vector_index=VectorIndex.HNSW,
    local=True,
    embedder=embedder,
    )
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


def create_knowledge_base(base_path, collection):
    vector_db = Weaviate(
        collection=collection,
        search_type=SearchType.hybrid,
        distance=Distance.COSINE,
        vector_index=VectorIndex.HNSW,
        embedder=embedder,
    )
    
    knowledge_base = PDFKnowledgeBase(
        name=collection,
        path=base_path,
        vector_db=vector_db,
        num_documents=5
    )
    c=0
    for file in os.listdir(base_path):
        if c>0:
            switch = False
        else:
            switch = True
        c+=1
        if file.endswith(".pdf"):
            folders = base_path.split('/')
            brand, product, sale_status = folders[-3], folders[-2], folders[-1]
            print(f"Loading {file} into {collection} knowledge base with path {base_path}")
            print(f"Brand: {brand}, Product: {product}, Sale Status: {sale_status}")
            knowledge_base.load_document(
                  path = os.path.join(base_path, file),
                  metadata = {
                      "brand": brand,
                      "product": product,
                      "sale_status": sale_status,
                      "year": file[:4],
                      "month": file[4:6],
                      "day": file[6:8],
                  },
                  recreate=switch
                  )

    return knowledge_base

all_kb = [
    [r'call transcriptions/ASIA/Life/No Sale', "asia_life_no_sale"],
    [r'call transcriptions/ASIA/Life/Sale', "asia_life_sale"],
    [r'call transcriptions/OneChoice/Life/Sale', "onechoice_life_sale"],
    [r'call transcriptions/OneChoice/Life/No Sale', "onechoice_life_no_sale"],
    [r'call transcriptions/OneChoice/Income Protection/Sale', "onechoice_income_protection_sale"],
    [r'call transcriptions/OneChoice/Income Protection/No Sale', "onechoice_income_protection_no_sale"],
    [r'call transcriptions/Real/Life/Sale', "real_life_sale"],
    [r'call transcriptions/Real/Life/No Sale', "real_life_no_sale"],
    [r'call transcriptions/Real/Funeral/Sale', "real_funeral_sale"],
    [r'call transcriptions/Real/Funeral/No Sale', "real_funeral_no_sale"],
    [r'call transcriptions/Real/Income Protection/Sale', "real_income_protection_sale"],
    [r'call transcriptions/Real/Income Protection/No Sale', "real_income_protection_no_sale"],
]

transcription_knowledge_bases = CombinedKnowledgeBase(
    sources = [
        create_knowledge_base(path, collection)
        for path, collection in all_kb
    ],
    vector_db=Weaviate(
        collection="transcription master",
        search_type=SearchType.hybrid,
        distance=Distance.COSINE,
        vector_index=VectorIndex.HNSW,
        embedder=embedder,
        # local=True,
    )
)

transcription_knowledge_tool = KnowledgeTools(
    knowledge=transcription_knowledge_bases,
    think=True,
    search=True,
    analyze=True,
    instructions=transcription_agent_config.get('instructions', None),
    add_instructions=True,
    add_few_shot=True,
)

transcript_agent = Agent(
    name="Transcript Reasoning Agent",
    model=azure_model,
    tools=[
        transcription_knowledge_tool,
        ThinkingTools(add_instructions=True),
    ],
    knowledge=transcription_knowledge_bases,
    search_knowledge=True,
    update_knowledge=True,
    add_references=True,
    context=transcription_agent_config.get('context', None),
    add_context=True,
    resolve_context=True,
    add_history_to_messages=True,
    num_history_runs=10,
    storage=storage_transcription_agent,
    show_tool_calls=True,
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


all_knowledge_bases = CombinedKnowledgeBase(
    sources=[
        sql_knowledge_base,
        transcription_knowledge_bases,
    ],
    vector_db=Weaviate(
        collection="combined master",
        search_type=SearchType.hybrid,
        distance=Distance.COSINE,
        vector_index=VectorIndex.HNSW,
        embedder=embedder,
    )
)

customer_insight_team = Team(
    name="Customer Insight Team",
    mode="collaborate",
    model=azure_model, 
    members=[
        sql_agent,
        transcript_agent,
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
    knowledge=all_knowledge_bases,
    enable_agentic_context=True,
    share_member_interactions=True,
    get_member_information_tool=True,
    search_knowledge=True,
    read_team_history=True,
    enable_team_history=True,
    num_history_runs=10,
    storage=storage_cip_team,
)

app = Playground(agents=[sql_agent,transcript_agent], teams=[customer_insight_team]).get_app()


if __name__ == "__main__":
    serve_playground_app("agno_test:app", host="0.0.0.0", port=7777, reload=True)


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

storage = SqliteStorage(
    table_name="tblMaster_CIP",
    db_file="/mnt/chatdata/tmp_usr.db",
)

with open(r'sql_agent_config.json', 'r') as f:
    file = json.load(f)
    sql_agent_config = file['agent_config']

load_dotenv()

api_key = os.getenv("AZURE_OPENAI_API_KEY_AQMAGENTICOS")
azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT_AQMAGENTICOS")
azure_deployment = "o3-mini"
api_version = "2024-12-01-preview"

def create_knowledge_base(path, collection):
    documents = []
    
    for file in os.listdir(path):
        if file.endswith(".pdf"):
            full_path = os.path.join(path, file).replace("\\", "/").replace(" ", "_")
            folders = path.split("/")[-3:]
            metadata = {
                "brand": folders[0],
                "product": folders[1],
                "sale_status": folders[2],
                "year": file[:4],
                "month": file[4:6],
                "day": file[6:8],
            }
            documents.append({
                "path": full_path,
                "metadata": metadata
            })

    vector_db = Weaviate(
        collection=collection,
        search_type=SearchType.hybrid,
        distance=Distance.COSINE,
        vector_index=VectorIndex.HNSW,
        local=True,
    )
    
    knowledge_base = PDFKnowledgeBase(
        name=collection,
        path=path,
        vector_db=vector_db,
    )

    knowledge_base.load(recreate=True)
    return knowledge_base

azure_model = AzureOpenAI(
    api_key=api_key,
    azure_endpoint=azure_endpoint,
    azure_deployment=azure_deployment,
    api_version=api_version,
)

knowledge_base = JSONKnowledgeBase(
    path = r"knowledge",
    vector_db=Weaviate(
    collection="master",
    search_type=SearchType.hybrid,
    distance=Distance.COSINE,
    vector_index=VectorIndex.HNSW,
    local=True,
    )
)

all_kb = [
    [r'C:/Users/shubhm01/Documents/Customer Insights Platform/call transcriptions/ASIA/Life/No Sale', "asia_life_no_sale"],
    [r'C:/Users/shubhm01/Documents/Customer Insights Platform/call transcriptions/ASIA/Life/Sale', "asia_life_sale"],
    [r'C:/Users/shubhm01/Documents/Customer Insights Platform/call transcriptions/OneChoice/Life/Sale', "onechoice_life_sale"],
    [r'C:/Users/shubhm01/Documents/Customer Insights Platform/call transcriptions/OneChoice/Life/No Sale', "onechoice_life_no_sale"],
    [r'C:/Users/shubhm01/Documents/Customer Insights Platform/call transcriptions/OneChoice/Income Protection/Sale', "onechoice_income_protection_sale"],
    [r'C:/Users/shubhm01/Documents/Customer Insights Platform/call transcriptions/OneChoice/Income Protection/No Sale', "onechoice_income_protection_no_sale"],
    [r'C:/Users/shubhm01/Documents/Customer Insights Platform/call transcriptions/Real/Life/Sale', "real_life_sale"],
    [r'C:/Users/shubhm01/Documents/Customer Insights Platform/call transcriptions/Real/Life/No Sale', "real_life_no_sale"],
    [r'C:/Users/shubhm01/Documents/Customer Insights Platform/call transcriptions/Real/Funeral/Sale', "real_funeral_sale"],
    [r'C:/Users/shubhm01/Documents/Customer Insights Platform/call transcriptions/Real/Funeral/No Sale', "real_funeral_no_sale"],
    [r'C:/Users/shubhm01/Documents/Customer Insights Platform/call transcriptions/Real/Income Protection/Sale', "real_income_protection_sale"],
    [r'C:/Users/shubhm01/Documents/Customer Insights Platform/call transcriptions/Real/Income Protection/No Sale', "real_income_protection_no_sale"],
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
        local=True,
    )
)

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

transcription_knowledge_tool = KnowledgeTools(
    knowledge=transcription_knowledge_bases,
    think=True,
    search=True,
    analyze=True,
    instructions="",
    add_instructions=True,
    add_few_shot=True,
)

sql_agent = Agent(
    name="SQL Analyst Agent",
    model=azure_model,
    tools=[
        SQLTools(db_url= r"sqlite:////mnt/chatdata/tblMaster_CIP.db"),
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
    context=None,
    add_context=True,
    resolve_context=True,
    add_history_to_messages=True,
    num_history_runs=10,
    storage=storage,
    show_tool_calls=True,
    reasoning=True,  # This agent should reason through citations
    read_chat_history=True,
    read_tool_call_history=True,
    system_message_role="system",
    system_message="You are an expert in analyzing customer service transcripts and providing explanations based on real conversations.",
    description="Fetches and explains root causes using call transcripts from Weaviate collections.",
    goal="To explain decline reasons and enrich answers using real conversation transcripts.",
    instructions="Identify the correct transcript collection based on brand, product, and outcome. Retrieve top-k chunks relevant to the user's query and summarize key causes and examples mentioned by customers.",
    expected_output="Natural language explanation grounded in actual transcripts, with references.",
    markdown=True,
    add_name_to_instructions=True,
    add_datetime_to_instructions=True,
    timezone_identifier="Australia/Sydney",
    add_state_in_messages=True,
    monitoring=True,
)


customer_insight_team = Team(
    name="Customer Insight Team",
    mode="route",
    model=azure_model, 
    members=[
        sql_agent,
        transcript_agent,
    ],
    show_tool_calls=True,
    markdown=True,
    description="Routes questions to either the SQL Analyst Agent or the Transcript Reasoning Agent.",
    instructions=[
        "If the user's question is about sales, declines, premiums, underwriting stats, locations, trends, or anything structured — route to the **SQL Analyst Agent**.",
        "If the user's question involves call reasons, customer objections, what was said in transcripts, or examples from conversations — route to the **Transcript Reasoning Agent**.",
        "If unsure, prefer the **SQL Analyst Agent** unless the question explicitly mentions 'transcripts', 'customer said', 'conversation', or 'what did the customer say'.",
    ],
    show_members_responses=True,
)

app = Playground(agents = [sql_agent, transcript_agent], teams=[customer_insight_team]).get_app()


if __name__ == "__main__":
    serve_playground_app("agno_test:app", host="0.0.0.0", port=7777, reload=True)


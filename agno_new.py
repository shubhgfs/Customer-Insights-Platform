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
import openai
from agno.tools import tool

load_dotenv()

# embedder = AzureOpenAIEmbedder(
#     api_key=os.getenv("AZURE_EMBEDDER_OPENAI_API_KEY"),
#     api_version="2024-12-01-preview",
#     azure_endpoint=os.getenv("AZURE_EMBEDDER_OPENAI_ENDPOINT"),
#     azure_deployment="text-embedding-3-large"
# )

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

client = openai.AzureOpenAI(
            api_key=os.getenv("AZURE_OPENAI_API_KEY_AQMAGENTICOS"),
            azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT_AQMAGENTICOS"),
            api_version="2024-12-01-preview",
        )

#######################################################################
####################     SQL AGENT     ################################
#######################################################################

# sql_collection = Weaviate(
#     collection="sql_collection",
#     search_type=SearchType.hybrid,
#     distance=Distance.COSINE,
#     vector_index=VectorIndex.HNSW,
#     )

# sql_knowledge_base = JSONKnowledgeBase(
#     path = r"knowledge",
#     vector_db=Weaviate(
#     collection="master",
#     search_type=SearchType.hybrid,
#     distance=Distance.COSINE,
#     vector_index=VectorIndex.HNSW,
#     )
# )

# sql_knowledge_tool = KnowledgeTools(
#         knowledge=sql_knowledge_base,
#         think=True,
#         search=True,
#         analyze=True,
#         instructions=sql_agent_config.get('instructions', None),
#         add_instructions=True,
#         add_few_shot=True,
# )

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
        # sql_knowledge_tool,
        sql_thinking_tool,
    ],
    context=sql_agent_config.get('context', None),
    add_context=True,
    resolve_context=True,
    add_history_to_messages=True,
    num_history_runs=10,
    # knowledge=sql_knowledge_base,
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


def select_index(query: str) -> str:
    """
    Use an LLM to choose the correct index name from a predefined list.
    Returns a strictly valid index name or refuses if not possible.
    """

    # Valid index choices
    valid_indexes = [
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
        "real-life-sale",
    ]

    # System prompt with deep context
    system_prompt = """
You are an expert assistant tasked with selecting the most appropriate index name from a predefined list.

Each index name is a combination of:
1. **Brand**: 'asia', 'onechoice', or 'real'
2. **Product**: 'life', 'incomeprotection', or 'funeral'
3. **Sale status**: 'sale' or 'nosale'

The format is: `<brand>-<product>-<sale_status>`, all lowercase.

The user query may mention any combination of brand, product, or sale intent. Based on this, select the best matching index name from the provided enum list. Only return a valid match if it exactly maps to one of the 12 allowed index names.

If no clear match exists, **do not select anything**.

Examples:
- "What happened in Real Life Sale calls?" → real-life-sale
- "Insights from OneChoice income protection where no sale happened" → onechoice-incomeprotection-nosale
- "Funeral insurance no-sale data for Real brand" → real-funeral-nosale

**Do not guess.** If the brand or product is missing, ambiguous, or mismatched, return nothing.
"""

    # Define function schema with enums
    functions = [
        {
            "name": "choose_index",
            "description": "Return the most relevant index name from the 12 allowed options based on the user query.",
            "parameters": {
                "type": "object",
                "properties": {
                    "index_name": {
                        "type": "string",
                        "enum": valid_indexes,
                        "description": "The selected index name from the allowed list."
                    }
                },
                "required": ["index_name"]
            }
        }
    ]

    # LLM call with system context
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": f"Query: {query}"}
    ]

    response = client.chat.completions.create(
        model=os.environ.get("AZURE_OPENAI_DEPLOYMENT_ID_AQMAGENTICOS"),
        messages=messages,
        functions=functions,
        function_call={"name": "choose_index"},
    )

    # Extract and validate response
    function_args = response.choices[0].message.function_call.arguments

    try:
        index_name = json.loads(function_args)["index_name"]
        if index_name in valid_indexes:
            return index_name
        else:
            return ""  # fallback safety
    except (KeyError, json.JSONDecodeError):
        return ""


@tool(
    name="search_transcriptions",
    description="Run a search query against the transcription data to find factual insights from call recordings. Results are grounded in retrieved citations only.",
    show_result=True,
)
def search_transcriptions(query: str) -> str:
    """
    This tool searches call transcription data stored in Azure AI Search vector indexes.
    It:
    1. Selects the appropriate index using brand-product-sale classification.
    2. Uses the query to retrieve relevant transcript chunks (citations).
    3. Extracts grounded insights such as customer intent, agent behavior, call outcome, and sentiments.
    4. Returns a factual summary based ONLY on the retrieved citations.
    """
    
    selected_index = select_index(query)
    
    if not selected_index:
        return "No valid index could be determined for the query. Please try rephrasing or check brand/product/sale intent."

    # System message to tightly control LLM behavior
    system_prompt = """
You are a Transcription Intelligence Agent built to analyze and summarize insights from customer-sales agent call transcriptions stored in vector indexes (Azure AI Search).

Your task:
1. Use the user’s query and retrieved transcript citations to determine the purpose and outcome of the call.
2. Summarize:
   - The customer's **intent or sentiment**
   - The agent's **response or persuasion**
   - The **outcome** (sale/no sale, confusion, objections, interest, etc.)
3. Cite only factual information that is present in the retrieved transcript snippets.
4. Do NOT make up or assume anything that is not in the retrieved citations.
5. If no meaningful insight is found, state that clearly.

Be concise but insightful. Your summary must reflect what the actual conversation shows.
"""

    print('System Prompt:', system_prompt)
    print('Query:', query)
    print('Selected Index:', selected_index)

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": query}
    ]

    response = client.chat.completions.create(
        model=os.environ.get("AZURE_OPENAI_DEPLOYMENT_ID_AQMAGENTICOS"),
        messages=messages,
        extra_body={
            "data_sources": [{
                "type": "azure_search",
                "parameters": {
                    "endpoint": os.environ["AZURE_AI_SEARCH_ENDPOINT"],
                    "index_name": selected_index,
                    "authentication": {
                        "type": "api_key",
                        "key": os.environ["AZURE_AI_SEARCH_API_KEY"],
                    }
                }
            }],
        }
    )

    # Extract message + citations
    answer = response.choices[0].message.content
    citations = response.choices[0].message.model_extra.get("context", {}).get("citations", [])

    print("Answer:", answer)
    print("Citations:", citations)

    return answer, citations


#######################################################################
####################     TRANSCRIPTION AGENT     ######################
#######################################################################

transcription_agent = Agent(
    name="Transcription Agent",
    model=azure_model,
    tools=[
        search_transcriptions,
    ],
    context=transcription_agent_config.get('context', None),
    add_context=True,
    resolve_context=True,
    add_history_to_messages=True,
    num_history_runs=10,
    # knowledge=sql_knowledge_base,
    search_knowledge=True,
    update_knowledge=True,
    add_references=True,
    storage=storage_transcription_agent,
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
        sql_agent,
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

app = Playground(agents=[sql_agent, transcription_agent], teams=[customer_insight_team]).get_app()

if __name__ == "__main__":
    serve_playground_app("agno_new:app", port=7777, reload=True)


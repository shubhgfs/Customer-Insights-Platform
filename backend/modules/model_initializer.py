from agno.agent import Agent
from agno.models.azure import AzureOpenAI
from agno.tools.sql import SQLTools
from agno.tools.reasoning import ReasoningTools
from agno.tools.thinking import ThinkingTools
from agno.team.team import Team
from backend.modules.transcription_tool import TranscriptionSearchTool
from backend.modules.config_loader import load_config
from backend.modules.constants import *
from agno.vectordb.search import SearchType
from agno.vectordb.weaviate import Distance, VectorIndex, Weaviate
from agno.knowledge.json import JSONKnowledgeBase

def init_model():
    return AzureOpenAI(
        api_key=AZURE_API_KEY_AQMAGENTICOS,
        azure_endpoint=AZURE_ENDPOINT_AQMAGENTICOS,
        azure_deployment=AZURE_DEPLOYMENT_O3,
        api_version=AZURE_API_VERSION,
    )

def init_sql_agent(model):
    vector_db = Weaviate(
        collection="master",
        search_type=SearchType.hybrid,
        distance=Distance.COSINE,
        vector_index=VectorIndex.HNSW,
    )

    knowledge_base = JSONKnowledgeBase(
        path = r"knowledge",
        vector_db=vector_db,
    )

    cfg = load_config(r"backend/sql_agent_config.json")['agent_config']
    return Agent(
        name="SQL Analyst Agent",
        model=model,
        tools=[
            SQLTools(db_url="sqlite:///backend/tblMaster_CIP.db"),
            ReasoningTools(instructions=cfg.get("instructions"), add_instructions=True),
            ThinkingTools(think=True, instructions=cfg.get("instructions"), add_instructions=True)
        ],
        context=cfg.get("context"),
        add_context=True,
        resolve_context=True,
        add_history_to_messages=True,
        num_history_runs=10,
        knowledge=knowledge_base,
        search_knowledge=True,
        update_knowledge=True,
        add_references=True,
        show_tool_calls=True,
        read_chat_history=True,
        read_tool_call_history=True,
        system_message_role="system",
        system_message=cfg.get("system_message"),
        description=cfg.get("description"),
        goal=cfg.get("goal"),
        instructions=cfg.get("instructions"),
        expected_output=cfg.get("expected_output"),
        add_name_to_instructions=True,
        add_state_in_messages=True,
        markdown=True,
        timezone_identifier=TIMEZONE,
        add_datetime_to_instructions=True,
    )


def init_transcription_agent(model):
    cfg = load_config(r"backend/transcription_agent_config.json")['agent_config']
    return Agent(
        name="Transcription Agent",
        model=model,
        tools=[
            TranscriptionSearchTool()
        ],
        context=cfg.get("context"),
        add_context=True,
        resolve_context=True,
        add_history_to_messages=True,
        num_history_runs=10,
        search_knowledge=True,
        update_knowledge=True,
        add_references=True,
        show_tool_calls=True,
        read_chat_history=True,
        read_tool_call_history=True,
        system_message_role="system",
        system_message=cfg.get("system_message"),
        description=cfg.get("description"),
        goal=cfg.get("goal"),
        instructions=cfg.get("instructions"),
        expected_output=cfg.get("expected_output"),
        add_name_to_instructions=True,
        add_state_in_messages=True,
        markdown=True,
        timezone_identifier=TIMEZONE,
        add_datetime_to_instructions=True,
    )


def init_team(sql_agent, transcription_agent, model):
    cfg = load_config(r"backend/cip_team_config.json")['team_config']
    return Team(
        name="Customer Insight Team",
        model=model,
        mode="coordinate",
        members=[sql_agent, transcription_agent],
        context=cfg.get("context"),
        instructions=cfg.get("instructions"),
        description=cfg.get("description"),
        expected_output=cfg.get("expected_output"),
        success_criteria=cfg.get("success_criteria"),
        markdown=True,
        show_tool_calls=True,
        show_members_responses=True,
        add_datetime_to_instructions=True,
        enable_agentic_context=True,
        read_team_history=True,
        enable_team_history=True,
        num_history_runs=10,
        get_member_information_tool=True,
        share_member_interactions=True,
    )

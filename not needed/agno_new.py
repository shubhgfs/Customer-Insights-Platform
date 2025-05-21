import json
import os
import openai
from dotenv import load_dotenv
from agno.agent import Agent
from agno.models.azure import AzureOpenAI
from agno.tools.reasoning import ReasoningTools
from agno.tools.sql import SQLTools
from agno.tools.thinking import ThinkingTools
from agno.team.team import Team
from backend.transcription_tool import TranscriptionSearchTool

load_dotenv()

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
    # storage=storage_sql_agent,
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
            deployment=os.environ.get("AZURE_OPENAI_DEPLOYMENT_ID_AQMAGENTICOS"),
            system_prompt=transcription_agent_config.get('system_message', None),
        )
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
    # storage=storage_transcription_agent,
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
    # storage=storage_cip_team,
)

import asyncio

# Your async handler
async def get_team_response(team, message):
    response = await team.arun(message)
    return response


aaa = asyncio.run(get_team_response(customer_insight_team, "What is the customer sentiment in the asia life sale calls?"))
print(aaa)
print(type(aaa))


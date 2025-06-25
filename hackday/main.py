from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Optional
from hack import RecommendSIToolkit
from agno.agent import Agent
from agno.models.azure import AzureOpenAI
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# -----------------------------------------
# Pydantic input schema
# -----------------------------------------
class RecommendSIInput(BaseModel):
    product_code: str
    benefit_code: str
    gender: int = Field(ge=0, le=2)
    smoker: int = Field(ge=0, le=2)
    age: int = Field(ge=0, le=120)
    premium: float = Field(gt=0)
    cover_type: int

# -----------------------------------------
# Agent Setup
# -----------------------------------------
model = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY_AQMAGENTICOS"),
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT_AQMAGENTICOS"),
    azure_deployment=os.getenv("AZURE_OPENAI_DEPLOYMENT_ID_AQMAGENTICOS"),
    api_version=os.getenv("AZURE_OPENAI_API_VERSION_AQMAGENTICOS"),
)

agent = Agent(
    name="AURA Insurance Pricing Assistant",
    model=model,
    tools=[RecommendSIToolkit()],
    context={},
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
    system_message=(
        "You are AURA, an intelligent insurance pricing assistant working for Greenswan Financials. "
        "Your job is to analyze a customer's profile, assess how much they can afford to pay as a premium, "
        "and recommend the most suitable sum insured (SI) based on statistical data from similar customer profiles. "
        "You should always respond with valid JSON and clearly justify your recommendation using mean, min, and max values."
    ),
    description="AURA helps insurance advisors and customers determine suitable sum insured options based on affordability and data-driven insights.",
    goal="Recommend a fair and optimized sum insured (SI) to customers who cannot afford their original quoted premium.",
    instructions=(
        "You will receive the customer's profile and their budget, along with summary statistics from past matching cases. "
        "Use this to suggest a sum insured they can receive for their budget. Output valid JSON with your recommendation and justification."
    ),
    expected_output=(
        "{ 'recommended_sum_insured': <number>, "
        "'justification': <explanation string> }"
    ),
    add_name_to_instructions=True,
    add_state_in_messages=True,
    markdown=True,
    timezone_identifier='Australia/Sydney',
    add_datetime_to_instructions=True,
)

# -----------------------------------------
# FastAPI App
# -----------------------------------------
app = FastAPI(
    title="Greenswan Insurance Pricing API",
    description="API for recommending sum insured based on customer premium budget",
    version="1.0.0"
)

# -----------------------------------------
# Endpoint
# -----------------------------------------
@app.post("/recommend-si")
async def recommend_sum_insured(payload: RecommendSIInput):
    try:
        input_data = payload.dict()
        result = await agent.run(input_data)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

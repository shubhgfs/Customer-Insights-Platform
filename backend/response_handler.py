import asyncio

async def run_team(team, user_message: str):
    response = await team.arun(user_message)
    return response

def get_team_response(team, user_message: str):
    return asyncio.run(run_team(team, user_message))

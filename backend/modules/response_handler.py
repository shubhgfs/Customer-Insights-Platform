def get_team_response(team, user_message: str):
    print("🔍 Received user message:")
    print(f"👉 {user_message}\n")

    print("🔧 Starting orchestration process...")

    # Log team configuration or state (optional, depends on team object structure)
    if hasattr(team, 'agents'):
        print(f"🧠 Available agents: {[agent.name for agent in team.agents]}")

    # Hook into Agno’s built-in tool invocation tracking if supported
    print("🤖 Running message through team...")
    response = team.run(
        user_message,
        callbacks={
            "on_tool_start": lambda tool_name, *args, **kwargs: print(f"🔨 Tool started: {tool_name}"),
            "on_tool_end": lambda tool_name, output: print(f"✅ Tool completed: {tool_name} → Output: {str(output)[:300]}..."),
            "on_error": lambda e: print(f"❌ Error encountered: {str(e)}"),
            "on_agent_start": lambda agent_name: print(f"📌 Agent selected: {agent_name}"),
            "on_agent_end": lambda agent_name: print(f"📤 Agent completed: {agent_name}"),
        }
    )

    print("\n📦 Final response generated:")
    print(response)
    return response

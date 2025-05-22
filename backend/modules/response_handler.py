def get_team_response(team, user_message: str):
    print("🔍 Received user message:")
    print(f"👉 {user_message}\n")

    print("🔧 Starting orchestration process...")

    # Hook into Agno’s built-in tool invocation tracking if supported
    print("🤖 Running message through team...")
    response = team.run(user_message)

    print("\n📦 Final response generated:")
    print(response)
    return response

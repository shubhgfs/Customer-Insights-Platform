import pandas as pd
from azure.cosmos import exceptions

def get_agents(container_agent):
    try:
        items = list(container_agent.query_items(query="SELECT * FROM c", enable_cross_partition_query=True))

        if not items:
            return pd.DataFrame()

        formatted_data = [
            {'Agent Name': item['agent_name'], 'System': item['system'], 'Temperature': item['temperature']}
            for item in items
        ]

        return pd.DataFrame(formatted_data)

    except exceptions.CosmosHttpResponseError as e:
        print(f"Error fetching agents: {e}")
        return pd.DataFrame()

def select_agent(agent_data, selected_agent):
    if selected_agent in agent_data["Agent Name"].values:
        selected_row = agent_data[agent_data["Agent Name"] == selected_agent].iloc[0]
        return selected_agent, selected_row["System"], selected_row["Temperature"]
    
    return None, None, None

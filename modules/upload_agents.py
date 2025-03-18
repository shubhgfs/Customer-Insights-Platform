from azure.cosmos import exceptions
from dotenv import load_dotenv
import os
import uuid
from datetime import datetime
import json
from modules.cosmos_db_connection import get_cosmos_client

load_dotenv()

container = get_cosmos_client("Marketing AI", "Agents")

with open(r'json files/agents.json') as f:
    agent_data = json.load(f)

for agent_name, details in agent_data.items():
    query = f"SELECT * FROM c WHERE c.agent_name = '{agent_name}'"
    existing_items = list(container.query_items(query=query, enable_cross_partition_query=True))

    document_id = existing_items[0]["id"] if existing_items else str(uuid.uuid4())

    document = {
        "id": document_id,
        "agent_name": agent_name,
        "system": details["system"],
        "temperature": details["temperature"],
        "timestamp": str(datetime.utcnow()),
    }

    try:
        container.upsert_item(document, partition_key=agent_name)
    except exceptions.CosmosHttpResponseError as e:
        print(f"Error occurred: {e.message}")
        print("Document that caused error:", document)

print('All agent details uploaded or updated!')

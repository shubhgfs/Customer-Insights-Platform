from azure.cosmos import CosmosClient
import os
from dotenv import load_dotenv

load_dotenv()

def get_cosmos_client(database_name, container_name):
    connection_string = os.getenv("AZURE_COSMOS_DB_CONNECTION_STRING")
    client = CosmosClient.from_connection_string(connection_string, connection_verify=False)
    return client.get_database_client(database_name).get_container_client(container_name)

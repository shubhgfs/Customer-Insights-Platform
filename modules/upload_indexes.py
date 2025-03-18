from azure.cosmos import exceptions
from dotenv import load_dotenv
import os
import uuid
from datetime import datetime
import json
import pandas as pd
from modules.cosmos_db_connection import get_cosmos_client

load_dotenv()

container = get_cosmos_client("Marketing AI", "Indexes")

with open(r'json files/index.json') as f:
    index_data = json.load(f)

rows = [
    [brand, product, sale_status, index_name]
    for brand, products in index_data.items()
    for product, statuses in products.items()
    for sale_status, index_name in statuses.items()
]

df = pd.DataFrame(rows, columns=["Brand", "Product", "Sale Status", "IndexName"])

for _, row in df.iterrows():
    index_name = row["IndexName"]
    query = f"SELECT * FROM c WHERE c.index_name = '{index_name}'"
    existing_items = list(container.query_items(query=query, enable_cross_partition_query=True))

    document_id = existing_items[0]["id"] if existing_items else str(uuid.uuid4())

    document = {
        "id": document_id,
        "index_name": index_name,
        "Brand": row["Brand"],
        "Product": row["Product"],
        "Sale Status": row["Sale Status"],
        "timestamp": str(datetime.utcnow()),
    }

    try:
        container.upsert_item(document, partition_key=document["index_name"])
    except exceptions.CosmosHttpResponseError as e:
        print(f"Error occurred: {e.message}")
        print("Document that caused error:", document)

print('All indexes uploaded!')

import pandas as pd
from azure.cosmos import exceptions

def get_indexes(container_index):
    try:
        items = list(container_index.query_items(query="SELECT * FROM c", enable_cross_partition_query=True))

        if not items:
            return pd.DataFrame()

        formatted_data = [
            {'Brand': item['Brand'], 'Product': item['Product'], 'Sale Status': item['Sale Status'], 'Index Name': item['index_name']}
            for item in items
        ]

        return pd.DataFrame(formatted_data)

    except exceptions.CosmosHttpResponseError as e:
        print(f"Error fetching indexes: {e}")
        return pd.DataFrame()

def select_index(index_names, selected_index):
    if selected_index in index_names["Index Name"].values:
        selected_row = index_names[index_names["Index Name"] == selected_index].iloc[0]
        return selected_row["Brand"], selected_row["Product"], selected_row["Sale Status"]
    
    return None, None, None

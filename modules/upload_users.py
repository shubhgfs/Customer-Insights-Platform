from azure.cosmos import exceptions
from dotenv import load_dotenv
import json
from cosmos_db_connection import get_cosmos_client

load_dotenv()

container = get_cosmos_client("Customer Insights Platform", "Users")

with open(r"json files/users.json", "r") as f:
    users_data = json.load(f)

for user_id, user_data in users_data['usernames'].items():
    user_data["id"] = user_id
    if "email" not in user_data:
        print(f"Skipping user {user_id}: Missing email field")
        continue 

    try:
        container.upsert_item(user_data)
    except exceptions.CosmosResourceExistsError:
        continue

cookie_data = users_data['cookie']
cookie_data["id"] = "cookie-cip1234567890"
cookie_data['email'] = "cookie-cip@gfs.com.au"

container.upsert_item(cookie_data)

print("Users with hashed passwords uploaded successfully!")

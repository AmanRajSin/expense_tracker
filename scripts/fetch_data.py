from requests_oauthlib import OAuth1Session
import sys
import os
import json
import pandas as pd

# Add the parent directory to the path so Python can find the 'config' module
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config.credentials import (
    CONSUMER_KEY,
    CONSUMER_SECRET,
    ACCESS_TOKEN,
    ACCESS_TOKEN_SECRET
)

# Create the OAuth session
oauth = OAuth1Session(
    CONSUMER_KEY,
    client_secret=CONSUMER_SECRET,
    resource_owner_key=ACCESS_TOKEN,
    resource_owner_secret=ACCESS_TOKEN_SECRET
)

# Fetch expenses
url = "https://secure.splitwise.com/api/v3.0/get_expenses?limit=100"
response = oauth.get(url)

if response.status_code == 200:
    data = response.json()
    print(f"✅ Fetched {len(data['expenses'])} expenses")
else:
    print("❌ Failed to fetch data:", response.status_code)
    print(response.text)

# Create the data directory if it doesn't exist
os.makedirs("data", exist_ok=True)

# Save raw JSON
with open("data/raw_expenses.json", "w") as f:
    json.dump(data, f, indent=2)
print("✅ Saved raw data to data/raw_expenses.json")

# Convert to DataFrame and save as CSV
df = pd.json_normalize(data['expenses'])
df.to_csv("data/processed_expenses.csv", index=False)
print("✅ Saved structured data to data/processed_expenses.csv")




# from requests_oauthlib import OAuth1Session
# from config.credentials import CONSUMER_KEY, CONSUMER_SECRET
# from config.tokens import ACCESS_TOKEN, ACCESS_TOKEN_SECRET

# oauth = OAuth1Session(
#     consumer_key,
#     client_secret=consumer_secret,
#     resource_owner_key=access_token,
#     resource_owner_secret=access_token_secret
# )

# # Fetch expenses
# url = "https://secure.splitwise.com/api/v3.0/get_expenses?limit=100"
# response = oauth.get(url)

# if response.status_code == 200:
#     data = response.json()
#     print("Expenses fetched:", len(data['expenses']))
# else:
#     print("Failed to fetch expenses:", response.status_code, response.text)
# print(data)
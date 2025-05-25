from requests_oauthlib import OAuth1Session

import sys
import os
# Add the parent directory to the path so Python can find the 'config' module
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config.credentials import CONSUMER_KEY, CONSUMER_SECRET

# Use them directly
consumer_key = CONSUMER_KEY
consumer_secret = CONSUMER_SECRET


# 1. Get a request token
request_token_url = 'https://secure.splitwise.com/api/v3.0/get_request_token'
oauth = OAuth1Session(consumer_key, client_secret=consumer_secret)
fetch_response = oauth.fetch_request_token(request_token_url)
resource_owner_key = fetch_response.get('oauth_token')
resource_owner_secret = fetch_response.get('oauth_token_secret')

# 2. Authorize
base_authorization_url = 'https://secure.splitwise.com/authorize'
authorization_url = oauth.authorization_url(base_authorization_url)
print(f'Go to {authorization_url} and authorize access.')

# After authorizing, paste the verifier from the redirected URL
verifier = input('Paste verifier here: ')

# 3. Get the access token
access_token_url = 'https://secure.splitwise.com/api/v3.0/get_access_token'
oauth = OAuth1Session(
    consumer_key,
    client_secret=consumer_secret,
    resource_owner_key=resource_owner_key,
    resource_owner_secret=resource_owner_secret,
    verifier=verifier
)
oauth_tokens = oauth.fetch_access_token(access_token_url)
access_token = oauth_tokens['oauth_token']
access_token_secret = oauth_tokens['oauth_token_secret']
print("******************")
print(access_token)
print(access_token_secret)
print("******************")
#Writing Tken secret in credentials.py
# Save the tokens to credentials.py
credentials_path = "config/credentials.py"

# Read existing credentials to preserve CONSUMER_KEY and CONSUMER_SECRET
with open(credentials_path, "r") as f:
    lines = f.readlines()

# Filter out old access tokens (if any)
new_lines = [line for line in lines if not line.startswith("ACCESS_TOKEN") and not line.startswith("ACCESS_TOKEN_SECRET")]

# Add the new access tokens
new_lines.append(f'ACCESS_TOKEN = "{access_token}"\n')
new_lines.append(f'ACCESS_TOKEN_SECRET = "{access_token_secret}"\n')

# Write back to file
with open(credentials_path, "w") as f:
    f.writelines(new_lines)

print("✅ Access tokens saved to config/credentials.py")

print("Authorization Done")
# Run this ONCE on your computer to get the token.json file
from google_auth_oauthlib.flow import InstalledAppFlow

# Scopes = What permissions the bot has (Read & Write)
SCOPES = ['https://www.googleapis.com/auth/calendar']

flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
creds = flow.run_local_server(port=0)

# Save the token
with open('token.json', 'w') as token:
    token.write(creds.to_json())

print("Success! You now have 'token.json'. Open it and copy the contents!")
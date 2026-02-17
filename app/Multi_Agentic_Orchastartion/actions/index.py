import requests
from requests.auth import HTTPBasicAuth
import json

# Jira Cloud domain
jira_domain = "jiragenie11.atlassian.net"

# Your credentials
email = "jiragenie11@gmail.com"
api_token = "amlyYWdlbmllMTFAZ21haWwuY29tOkFUQVRUM3hGZkdGMDVqSXFKY2RRZGxBUUZ2M1c4Q2lxSVN1LTVoQ0FZYkx2VVEtRGR2SlUxVmtXcC10X0F0MHpKRi1lMlpva05Ka1lFaHpoWWc4NU14aDFvQWE3YTA3Q2JhMVdBMmNWS2UwRTA5Nkp0MFBUenNnNFhnNlhPVmozMTZVYWpIbUZKeUlPMmZxS2Y0MUowVDd2VEtjOGhVMjZpQ1JCNkVyY2hlbFBtTzBvM2FWSTNCRT1ERjM1QUQxMA=="  # Replace with your actual token

# Correct API endpoint
url = f"https://{jira_domain}/rest/api/3/search/jql"

# Query parameters
params = {
    "jql": "project=SCRUM",
    "maxResults": 100,
    "fields": "key,summary,status,assignee"
}

# Headers
headers = {
    "Accept": "application/json"
}

# Make the GET request
response = requests.get(
    url,
    headers=headers,
    params=params,
    auth=HTTPBasicAuth(email, api_token)
)

# Check for errors
if response.status_code == 200:
    data = response.json()
    # Pretty print the JSON response
    print(json.dumps(data, indent=4))
else:
    print(f"Error: {response.status_code} - {response.text}")

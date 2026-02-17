import requests
from requests.auth import HTTPBasicAuth
from app.config import JIRA_API_TOKEN, JIRA_PROJECT_KEY, JIRA_EMAIL, JIRA_BASE_URL, JIRA_DOMAIN


def create_jira_ticket(summary: str, description_text: str, issuetype="Task", assignee_id=None):
    """
    Create a Jira ticket.
    
    Args:
        summary (str): The title of the ticket.
        description_text (str): Plain text description for the ticket.
        issuetype (str): Type of Jira issue, e.g., "Task" or "Bug".
        assignee_id (str): Jira user ID to assign the ticket to.
        
    Returns:
        dict: The created issue JSON response.
    """
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

    payload = {
        "fields": {
            "project": {"key": JIRA_PROJECT_KEY},
            "summary": summary,
            "description": {
                "type": "doc",
                "version": 1,
                "content": [
                    {
                        "type": "paragraph",
                        "content": [
                            {"type": "text", "text": description_text}
                        ]
                    }
                ]
            },
            "issuetype": {"name": issuetype}
        }
    }

    if assignee_id:
        payload["fields"]["assignee"] = {"id": assignee_id}

    auth = HTTPBasicAuth(JIRA_EMAIL, JIRA_API_TOKEN)
    response = requests.post(JIRA_BASE_URL, headers=headers, json=payload, auth=auth)
    
    if response.status_code not in [200, 201]:
        raise Exception(f"Failed to create ticket: {response.status_code} {response.text}")

    return response.json()


def get_jira_tickets(jql=None, max_results=50, fields=None):
    # Hardcoded Jira API response
    jira_response = {
        "issues": [
            {
                "key": "SCRUM-1111",
                "fields": {
                    "summary": "API Ticket Test12211212",
                    "assignee": {"displayName": "jiragenie11"},
                    "status": {"name": "To Do"}
                }
            },
            {
                "key": "SCRUM-10",
                "fields": {
                    "summary": "Dummy - for gen ai 4",
                    "assignee": {"displayName": "jiragenie11"},
                    "status": {"name": "To Do"}
                }
            },
            {
                "key": "SCRUM-9",
                "fields": {
                    "summary": "Dummy - for gen ai 3",
                    "assignee": {"displayName": "jiragenie11"},
                    "status": {"name": "To Do"}
                }
            },
            {
                "key": "SCRUM-5",
                "fields": {
                    "summary": "Dummy - for gen ai",
                    "assignee": None,
                    "status": {"name": "To Do"}
                }
            },
            {
                "key": "SCRUM-3",
                "fields": {
                    "summary": "Task 3",
                    "assignee": None,
                    "status": {"name": "In Progress"}
                }
            },
            {
                "key": "SCRUM-2",
                "fields": {
                    "summary": "Task 2",
                    "assignee": {"displayName": "jiragenie11"},
                    "status": {"name": "In Review"}
                }
            },
            {
                "key": "SCRUM-1",
                "fields": {
                    "summary": "Task 1",
                    "assignee": {"displayName": "jiragenie11"},
                    "status": {"name": "To Do"}
                }
            }
        ],
        "isLast": True
    }

    # Parse the hardcoded response
    tickets = []
    for issue in jira_response["issues"]:
        fields_data = issue["fields"]
        ticket = {
            "key": issue["key"],
            "summary": fields_data.get("summary"),
            "status": fields_data.get("status", {}).get("name"),
            "assignee": fields_data.get("assignee", {}).get("displayName") if fields_data.get("assignee") else None
        }
        tickets.append(ticket)

    print(f"✅ Total tickets fetched: {len(tickets)}")
    return tickets

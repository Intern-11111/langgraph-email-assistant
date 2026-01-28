import os
import pickle
import glob
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

# REQUIRED Gmail scope
SCOPES = ["https://www.googleapis.com/auth/gmail.modify"]

TOKEN_FILE = "token.json"

# Find the client secret JSON file (lazy loading)
def _find_credentials_file():
    # Look in TeamD1 directory (where this file is located)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    matches = glob.glob(os.path.join(script_dir, "client_secret_*.json"))
    if matches:
        return matches[0]
    
    creds_file = os.path.join(script_dir, "credentials.json")
    if os.path.exists(creds_file):
        return creds_file
    
    return None


def get_gmail_service():
    """
    Returns authenticated Gmail API service
    """

    # Find credentials file when needed (lazy loading)
    credentials_file = _find_credentials_file()
    if not credentials_file:
        raise FileNotFoundError("No credentials file (client_secret_*.json or credentials.json) found in TeamD1/")

    creds = None

    # Load saved token
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, "rb") as token:
            creds = pickle.load(token)

    # If no valid token → Login again
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                credentials_file, SCOPES
            )
            creds = flow.run_local_server(port=0)

        # Save token
        with open(TOKEN_FILE, "wb") as token:
            pickle.dump(creds, token)

    # Build Gmail service
    service = build("gmail", "v1", credentials=creds)

    return service

import os
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

SCOPES = [
    # Gmail
    "https://www.googleapis.com/auth/gmail.readonly",
    "https://www.googleapis.com/auth/gmail.modify",
    "https://www.googleapis.com/auth/gmail.send",

    # Calendar
    "https://www.googleapis.com/auth/calendar.readonly",
    "https://www.googleapis.com/auth/calendar.events",
]


TOKEN_PATH = "token.json"
CLIENT_SECRET_PATH = os.getenv(
    "GOOGLE_CLIENT_SECRET_FILE",
    "client_secret.json"
)



def get_google_credentials() -> Credentials:
    creds = None

    if os.path.exists(TOKEN_PATH):
        creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                CLIENT_SECRET_PATH,
                SCOPES,
            )

            creds = flow.run_local_server(
                host="localhost",
                port=0,
                open_browser=True,
                prompt="consent",
                authorization_prompt_message="Please visit this URL to authorize this application: {url}",
                success_message="Authorization complete. You may close this window.",
            )

        with open(TOKEN_PATH, "w") as token:
            token.write(creds.to_json())
        
        print("TOKEN SCOPES:", creds.scopes)

    return creds

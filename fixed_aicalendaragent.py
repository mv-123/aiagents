from openai import OpenAI
from dotenv import load_dotenv
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import os
import json
import datetime

'''
change token.json (expires 6 hours after created):
https://console.cloud.google.com/auth/clients/414710741977-u9m361v32qb0k9420om76oakh557knhg.apps.googleusercontent.com?project=ai-calendar-agent-507114
'''

load_dotenv()
client = OpenAI(
    api_key=os.environ.get("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1",
)

event = input("What event would you like to add to your calendar? ")
prompt = f'''You are an AI Calendar assistant. Your job is to understand a user's calendar request and convert it into a structured json.
User request:{event}
Return a valid json.
Use format: {{"Title": "Event Title",
"Date": "yyyy-mm-dd",
"Start time": "hh:mm",
"Duration": "mm",
"Attendees": ""}} '''

response = client.chat.completions.create(
    model="openai/gpt-oss-120b",
    messages=[
      {
        "role": "user",
        "content": prompt
      }
    ],
    temperature=2,
    max_completion_tokens=2048,
    top_p=1,
    stream=False,
    stop=None
)

SCOPES = [ "https://www.googleapis.com/auth/calendar" ]
result = response.choices[0].message.content
eventdata = json.loads(result)
print(result)

starttime = datetime.datetime.fromisoformat(eventdata["Date"]+"T"+eventdata["Start time"])
endtime = starttime + datetime.timedelta(minutes = int(eventdata["Duration"]))

# FIX 1: Corrected dictionary keys to camelCase ('dateTime', 'timeZone') 
# and changed the end event time from 'starttime' to 'endtime'.
googleevent = {
    "summary": eventdata["Title"],
    "start": {
        "dateTime": starttime.isoformat(),
        "timeZone": "America/Chicago"
    },
    "end": {
        "dateTime": endtime.isoformat(),
        "timeZone": "America/Chicago"
    }
}

# --- FIX 2: REWRITTEN GOOGLE AUTHENTICATION FLOW ---
credentials = None

# Step A: Look for a previously saved user session
if os.path.exists("token.json"):
    try:
        credentials = Credentials.from_authorized_user_file("token.json", SCOPES)
    except Exception:
        credentials = None  # Reset if the file is broken or malformed

# Step B: If no valid token exists, trigger the fallback workflow
if not credentials or not credentials.valid:
    if credentials and credentials.expired and credentials.refresh_token:
        # Refresh the login session if it is simply expired
        credentials.refresh(Request())
    else:
        # Open the web browser using your downloaded application identity file
        flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
        credentials = flow.run_local_server(port=0)
        
    # Step C: Automatically save the valid session token back down to disk
    with open("token.json", "w") as token:
        token.write(credentials.to_json())

# --- SERVICE BUILD & EXECUTION ---
calendar = build("calendar", version="v3", credentials=credentials)
created_event = calendar.events().insert(calendarId = "primary", body = googleevent).execute()
print("Event created successfully")

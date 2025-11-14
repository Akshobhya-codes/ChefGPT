import datetime, streamlit as st
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
import os, pickle

def get_credentials():
    if "token.pkl" in os.listdir():
        with open("token.pkl", "rb") as f:
            creds = pickle.load(f)
    else:
        flow = Flow.from_client_secrets_file(
            "client_secret.json",  # download this from Google when you created the OAuth client
            scopes=["https://www.googleapis.com/auth/calendar"]
        )
        flow.redirect_uri = "http://localhost:8501"
        auth_url, _ = flow.authorization_url(prompt="consent")
        st.write("👉 [Click here to authorize Google Calendar access](", auth_url, ")")
        st.stop()
    return creds

def add_to_calendar(recipe_text, date, time):
    creds = get_credentials()
    service = build("calendar", "v3", credentials=creds)

    # combine chosen date/time
    start_dt = datetime.datetime.combine(date, time)
    end_dt = start_dt + datetime.timedelta(hours=1)

    title = recipe_text.splitlines()[0][:100]
    event = {
        "summary": title,
        "description": recipe_text,
        "start": {"dateTime": start_dt.isoformat(), "timeZone": "UTC"},
        "end": {"dateTime": end_dt.isoformat(), "timeZone": "UTC"},
    }
    event = service.events().insert(calendarId="primary", body=event).execute()
    return event.get("htmlLink")

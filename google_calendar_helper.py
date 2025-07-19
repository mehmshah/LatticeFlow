"""
google_calendar_helper.py
Handles Google OAuth and fetching today's events for LatticeFlow AM routine.
"""
import os
from datetime import datetime, timedelta
from typing import List, Dict
import pickle
import streamlit as st
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request

SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
CREDENTIALS_FILE = 'google_credentials.json'  # User must provide this from Google Cloud Console
TOKEN_FILE = 'token.pickle'


def get_google_calendar_service():
    creds = None
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not os.path.exists(CREDENTIALS_FILE):
                st.warning('Please upload your google_credentials.json file from Google Cloud Console.')
                return None
            flow = Flow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES, redirect_uri='http://localhost:8501/')
            auth_url, _ = flow.authorization_url(prompt='consent')
            st.markdown(f"[Authorize Google Calendar]({auth_url})")
            code = st.text_input('Paste the authorization code here:')
            if code:
                flow.fetch_token(code=code)
                creds = flow.credentials
                with open(TOKEN_FILE, 'wb') as token:
                    pickle.dump(creds, token)
            else:
                return None
    try:
        service = build('calendar', 'v3', credentials=creds)
        return service
    except Exception as e:
        st.error(f'Google Calendar connection failed: {e}')
        return None

def get_todays_events():
    service = get_google_calendar_service()
    if not service:
        return []
    now = datetime.utcnow()
    start = now.replace(hour=0, minute=0, second=0, microsecond=0).isoformat() + 'Z'
    end = (now + timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0).isoformat() + 'Z'
    try:
        events_result = service.events().list(calendarId='primary', timeMin=start, timeMax=end, singleEvents=True,
                                              orderBy='startTime').execute()
        events = events_result.get('items', [])
        return events
    except Exception as e:
        st.error(f'Failed to fetch events: {e}')
        return []

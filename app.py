import streamlit as st
import re, time, datetime, os, pickle
from helpers.llm_client import get_meal_suggestions
from helpers.weaviate_memory import save_memory
from helpers.comet_logger import log_mood
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# ------------------------- PAGE CONFIG -------------------------
st.set_page_config(page_title="ChefGPT", page_icon="🍳", layout="centered")

# --- Custom CSS ---
st.markdown("""
    <style>
    body {
        background-color: #fafafa;
        font-family: 'Poppins', sans-serif;
    }
    .main-title {
        text-align: center;
        font-size: 42px;
        font-weight: 700;
        color: #ff7a59;
        margin-top: -20px;
    }
    .subtitle {
        text-align: center;
        font-size: 18px;
        color: #666;
        margin-bottom: 30px;
    }
    .stTextArea textarea {
        border-radius: 10px !important;
        border: 2px solid #f0f0f0 !important;
        font-size: 16px !important;
    }
    .stTextInput input {
        border-radius: 10px !important;
        border: 2px solid #f0f0f0 !important;
        font-size: 16px !important;
    }
    .stButton>button {
        background: linear-gradient(90deg, #ff7a59, #ff9a76);
        color: white;
        font-weight: 600;
        border: none;
        border-radius: 12px;
        padding: 10px 25px;
        font-size: 17px;
        transition: 0.3s ease;
    }
    .stButton>button:hover {
        background: linear-gradient(90deg, #ff9a76, #ff7a59);
        transform: scale(1.05);
    }
    .recipe-box {
        background-color: #ffffff;
        padding: 25px 30px;
        border-radius: 18px;
        box-shadow: 0px 4px 15px rgba(0,0,0,0.08);
        margin-top: 25px;
    }
    .recipe-title {
        color: #ff7a59;
        font-size: 22px;
        font-weight: 700;
        margin-bottom: 10px;
    }
    .calendar-btn button {
        background-color: #2d8cff !important;
        color: white !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        border: none !important;
    }
    .calendar-btn button:hover {
        background-color: #1a6ee8 !important;
    }
    </style>
""", unsafe_allow_html=True)

# ------------------------- HEADER -------------------------
st.markdown("<h1 class='main-title'>ChefGPT 🍳</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>Your mood-aware AI sous chef — powered by FriendliAI, Weaviate & Comet</p>", unsafe_allow_html=True)

# ------------------------- INPUTS -------------------------
shopping_list = st.text_area(
    "🛒 What's in your fridge?",
    value="eggs, spinach, bread, milk, cheese, pasta"
)
mood = st.text_input("😌 How are you feeling right now?", value="angry at my boss")

# ------------------------- GOOGLE CALENDAR AUTH -------------------------
SCOPES = ["https://www.googleapis.com/auth/calendar"]

def get_calendar_service():
    creds = None
    if os.path.exists("token.pkl"):
        with open("token.pkl", "rb") as token:
            creds = pickle.load(token)
    if not creds:
        flow = InstalledAppFlow.from_client_secrets_file("client_secret.json", SCOPES)
        creds = flow.run_local_server(port=8502)
        with open("token.pkl", "wb") as token:
            pickle.dump(creds, token)
    service = build("calendar", "v3", credentials=creds)
    return service

def add_to_calendar(recipe_text, event_date, event_time):
    service = get_calendar_service()
    start_dt = datetime.datetime.combine(event_date, event_time)
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

# ------------------------- SESSION -------------------------
if "recipes" not in st.session_state:
    st.session_state.recipes = None

# ------------------------- GENERATE BUTTON -------------------------
st.markdown("<br>", unsafe_allow_html=True)
if st.button("🍽️ Suggest Meals"):
    if shopping_list and mood:
        with st.spinner("ChefGPT is whipping up recipes..."):
            start = time.time()
            recipes = get_meal_suggestions(shopping_list, mood)
            elapsed = time.time() - start
        st.session_state.recipes = recipes
        st.success(f"✅ Ready in {elapsed:.2f}s — Bon Appétit!")
        try:
            save_memory(mood, shopping_list, recipes)
            log_mood(mood, recipes)
        except Exception as e:
            st.warning(f"Note: could not log memory — {e}")
    else:
        st.warning("Please tell me your fridge contents and your mood first!")

# ------------------------- DISPLAY RECIPES -------------------------
if st.session_state.recipes:
    recipe_blocks = [r.strip() for r in st.session_state.recipes.split('---') if r.strip()]
    for i, block in enumerate(recipe_blocks, start=1):
        with st.container():
            st.markdown("<div class='recipe-box'>", unsafe_allow_html=True)
            st.markdown(block)
            event_date = st.date_input(f"📅 Date for Recipe {i}", datetime.date.today(), key=f"date_{i}")
            event_time = st.time_input(f"⏰ Start time for Recipe {i}", datetime.time(18, 0), key=f"time_{i}")
            col1, col2, _ = st.columns([1.5, 3, 1])
            with col1:
                if st.button(f"📅 Add Recipe {i}", key=f"btn_{i}", help="Add to Google Calendar", type="primary"):
                    with st.spinner("Adding to Google Calendar..."):
                        try:
                            link = add_to_calendar(block, event_date, event_time)
                            st.success(f"✅ Added — [View Event]({link})")
                        except Exception as e:
                            st.error(f"⚠️ Calendar error: {e}")
            st.markdown("</div>", unsafe_allow_html=True)

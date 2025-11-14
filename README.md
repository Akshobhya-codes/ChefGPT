# ChefGPT

ChefGPT is an AI-powered cooking companion that recommends meals based on your mood and what's already in your fridge. It combines emotional intelligence with generative AI to turn your day's vibe into the perfect dish — and even adds it straight to your Google Calendar for planning.

## Features

- 🎭 **Mood-aware recommendations**: Get meal suggestions based on your current emotional state
- 🛒 **Fridge-based recipes**: Use ingredients you already have at home
- 📅 **Google Calendar integration**: Automatically add meal plans to your calendar
- 🧠 **Memory system**: Powered by Weaviate for persistent memory
- 📊 **Logging**: Integrated with Comet for mood and recipe tracking

## Tech Stack

- **Streamlit**: Web interface
- **FriendliAI/OpenAI**: AI meal recommendations
- **Weaviate**: Vector database for memory
- **Google Calendar API**: Calendar integration
- **Comet**: Logging and tracking

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set up Google Calendar API:
   - Create a project in Google Cloud Console
   - Enable Google Calendar API
   - Download credentials as `client_secret.json`
   - Place it in the project root

3. Configure environment variables:
   - Set up your API keys for OpenAI/FriendliAI
   - Configure Weaviate connection
   - Set up Comet API keys

4. Run the application:
```bash
streamlit run app.py
```

## Usage

1. Enter the ingredients you have in your fridge
2. Describe your current mood
3. Click "Suggest Meals" to get AI-powered recipe recommendations
4. Add recipes to your Google Calendar with date and time

## License

MIT License

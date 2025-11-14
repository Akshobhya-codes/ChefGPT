import os
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Connect to FriendliAI (OpenAI-compatible)
client = OpenAI(
    api_key=os.getenv("FRIENDLI_TOKEN"),
    base_url=os.getenv("FRIENDLI_BASE_URL")
)

# ----------------------------
# Main function used by app.py
# ----------------------------
def get_meal_suggestions(ingredients, mood):
    prompt = f"""
    You are ChefGPT, an AI chef.
    The user has these ingredients: {ingredients}
    They are feeling {mood}.

    Generate exactly 3 complete meal recipes that match their mood and use their available ingredients.
    Each recipe must include:
    - A creative meal name
    - A one-sentence mood-fit explanation
    - A full ingredients list with quantities
    - Step-by-step cooking instructions (5-8 steps)
    - An estimated cooking time

    Format your response like this:
    1. 🍽️ [Meal name] — [short description]
    **Ingredients:**
    - item1
    - item2
    **Steps:**
    1. ...
    2. ...
    3. ...
    **Time:** ...
    ---
    2. 🍽️ ...
    ...
    """

    # Send prompt to FriendliAI
    completion = client.chat.completions.create(
        model="meta-llama-3.1-8b-instruct",  # from Friendli dashboard
        messages=[{"role": "user", "content": prompt}],
        max_tokens=1000,   # long recipes
        temperature=0.9,
    )

    return completion.choices[0].message.content

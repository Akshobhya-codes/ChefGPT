import os
import weaviate
from weaviate.auth import AuthApiKey
from dotenv import load_dotenv

load_dotenv()

client = weaviate.connect_to_weaviate_cloud(
    cluster_url=os.getenv("WEAVIATE_URL"),
    auth_credentials=AuthApiKey(os.getenv("WEAVIATE_API_KEY")),
)

def save_memory(mood, ingredients, recipe):
    try:
        client.collections.create(
            name="ChefMemory",
            vectorizer_config={"vectorizer": "text2vec-openai"},
        )
    except Exception:
        pass

    collection = client.collections.get("ChefMemory")
    collection.data.insert(
        properties={
            "mood": mood,
            "ingredients": ingredients,
            "recipe": recipe,
        }
    )

def search_similar_mood(mood):
    collection = client.collections.get("ChefMemory")
    res = collection.query.near_text(
        query=mood,
        limit=3,
        return_properties=["mood", "recipe"]
    )
    return res

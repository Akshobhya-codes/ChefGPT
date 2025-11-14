from comet_ml import Experiment
import os

experiment = Experiment(
    api_key=os.getenv("COMET_API_KEY"),
    project_name="chefgpt",
    workspace=os.getenv("COMET_WORKSPACE"),
)

def log_mood(mood, recipe_text):
    experiment.log_text(f"Mood: {mood}\nRecipe: {recipe_text}")

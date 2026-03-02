# check_models.py
import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load your API key
load_dotenv()
api_key = os.environ.get("Gemini_Lock")
genai.configure(api_key=api_key)

print("🔍 Fetching available Gemini models...\n")

# Loop through and print all models that support generating text/content
for m in genai.list_models():
    if 'generateContent' in m.supported_generation_methods:
        print(f"Model Name: {m.name}")
        print(f"Description: {m.description}")
        print("-" * 40)
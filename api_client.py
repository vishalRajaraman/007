# api_client.py
import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

# Fetch the API key from your .env file
api_key = os.environ.get("Gemini_Lock")

if not api_key:
    raise ValueError("API Key not found! Please check your .env file.")

# Configure the Gemini SDK
genai.configure(api_key=api_key)

# Initialize the model (1.5 Flash is extremely fast and free-tier friendly)
model = genai.GenerativeModel('gemini-2.5-flash-lite')

def analyze_image(base64_image):
    """
    Sends the base64 image to Google's Gemini vision model and returns the response text.
    """
    try:
        # Gemini expects the inline image data in this specific dictionary format
        image_part = {
            "mime_type": "image/png",
            "data": base64_image
        }
        
        # Your strict instruction prompt
        prompt = "Analyze this screenshot. If it contains a multiple choice question, provide the correct option just give the option alone. if it contains multiple correct answers give all the correct options only remember options only. the answer u provide only must contain the options [A,B,c,D ...]"
        
        # Send both the prompt and the image dictionary to the model
        response = model.generate_content([prompt, image_part])
        
        # Return the clean text response
        return response.text
        
    except Exception as e:
        return f"API Error: {e}"
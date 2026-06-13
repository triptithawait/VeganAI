import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Use the key from env
google_key = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=google_key)

print("--- Checking Available Models ---")
try:
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(f"Model Name: {m.name}")
except Exception as e:
    print(f"Error: {e}")
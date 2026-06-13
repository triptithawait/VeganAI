from google import genai
import sys
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Load key from environment
MY_KEY = os.getenv("GOOGLE_API_KEY")

client = genai.Client(api_key=MY_KEY)

try:
    response = client.models.generate_content(
        model="gemini-1.5-flash", 
        contents="Say 'Hello World'"
    )
    print("SUCCESS! Your key is valid.")
    print("AI Response:", response.text)
except Exception as e:
    print("FAILED! The key is likely invalid or quota exceeded.")
    print("Error Details:", str(e))
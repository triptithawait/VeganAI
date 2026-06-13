from google import genai
import sys

# PASTE YOUR KEY HERE
MY_KEY = "AIzaSyCHi0CVuUgL31PUbomCni5DeTEpNy_uGC0" 

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
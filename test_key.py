import google.generativeai as genai

# PASTE YOUR KEY HERE
MY_KEY = "AIzaSyCHi0CVuUgL31PUbomCni5DeTEpNy_uGC0" 

genai.configure(api_key=MY_KEY)

try:
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content("Say 'Hello World'")
    print("✅ SUCCESS! Your key is valid.")
    print("AI Response:", response.text)
except Exception as e:
    print("❌ FAILED! The key is invalid.")
    print("Error Details:", str(e))
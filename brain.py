import base64
from google import genai
import os

# 1. Ensure your valid API Key is here
API_KEY = "AIzaSyCHi0CVuUgL31PUbomCni5DeTEpNy_uGC0" 

# 2. Initialize the Client
client = genai.Client(api_key=API_KEY)

def get_recipe_from_ai(user_craving, health_context="General"):
    """
    Fetches a vegan recipe. Uses a fallback list to handle quota limits.
    """
    models_to_try = [
        'gemini-2.0-flash', 
        'gemini-1.5-flash',
        'gemini-3-flash',
        'gemini-1.5-flash-8b' # We will use base names now!
    ]

    prompt = f"""
    You are a professional Vegan Dietitian. Provide a specific vegan recipe for someone craving: {user_craving}.
    Consider this health context: {health_context}.
    Include a short 'Nutritional Highlight' at the end.
    Also, add a single line at the start of your response in the format: "MEALNAME: [Name of the specific dish]"
    """

    for model_name in models_to_try:
        try:
            print(f"--- Attempting {model_name} ---")
            
            #
            response = client.models.generate_content(
                model=model_name,
                contents=prompt
            )
            
            if response and response.text:
                return {"ai_recommendation": response.text}
                
        except Exception as e:
            print(f"Model {model_name} failed: {str(e)}")
            continue 

    return {"ai_recommendation": f"⚠️ All AI nodes busy. Please wait 60 seconds."}

def generate_meal_image(meal_description):
    """
    Generates an image of the vegan meal using Nano Banana.
    """
    enhanced_prompt = f"Professional food photography of gourmet vegan {meal_description}, soft natural lighting, high resolution, 4k."

    try:
        print(f"--- Generating image using Nano Banana ---")
        
        # We use the name exactly as shown in your dashboard
        response = client.models.generate_image(
            model='nano-banana', 
            prompt=enhanced_prompt
        )

        image_base64 = base64.b64encode(response.image_bytes).decode('utf-8')
        return {"image_data": f"data:image/png;base64,{image_base64}"}

    except Exception as e:
        print(f"Image generation failed: {str(e)}")
        return {"image_data": ""}
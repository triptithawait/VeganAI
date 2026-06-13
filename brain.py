import base64
from google import genai
from groq import Groq

# API KEYS
GOOGLE_API_KEY = "AIzaSyCHi0CVuUgL31PUbomCni5DeTEpNy_uGC0" 
GROQ_API_KEY = "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" # Replace with your actual Groq key

# Clients
google_client = genai.Client(api_key=GOOGLE_API_KEY)

# Handle Groq Client (Original logic updated to allow key)
try:
    groq_client = Groq(api_key=GROQ_API_KEY)
except Exception:
    groq_client = None

def get_recipe_from_ai(user_input_data):
    user_craving = user_input_data.get("craving", "Vegan Meal")
    health_goal = user_input_data.get("goal", "General")
    health_issue = user_input_data.get("allergies", "None") 
    language = user_input_data.get("language", "English")

    height = user_input_data.get("height", 0)
    weight = user_input_data.get("weight", 0)
    bmi = user_input_data.get("bmi", 0)

    prompt = f"""
    You are an expert AI Vegan Dietitian.
    Create a gourmet vegan recipe for: {user_craving}.
    
    USER PROFILE:
    - Health Focus: {health_issue}
    - Goal: {health_goal}
    - Height: {height} cm, Weight: {weight} kg, BMI: {bmi:.1f}
    - Language: {language}
    
    Instructions: 
    1. STRICT RULE: Your response MUST START with this exact data block. Calculate these numbers REALISTICALLY based on the ingredients in the recipe and the user's focus ({health_issue}):
       DATA_START
       {{"protein_g": [calc], "carbs_g": [calc], "fats_g": [calc], "calories": [calc], "p_percent": [calc], "c_percent": [calc], "f_percent": [calc], "fiber_g": [calc], "sugar_g": [calc], "sodium_mg": [calc]}}
       DATA_END
    2. Then, provide the recipe starting with: "MEALNAME: [Name]"
    3. Include a 'Nutritional Information' section below the instructions that matches the DATA block exactly.
    4. Enclose every ingredient in [Square Brackets].
    5. Ensure the Macros (P/C/F) add up to nearly 100% in the p_percent/c_percent/f_percent fields.
    """

    try:
        if groq_client:
            completion = groq_client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": prompt}]
            )
            return {"ai_recommendation": completion.choices[0].message.content}
        else:
            # Fallback to Google Gemini
            response = google_client.models.generate_content(
                model="gemini-2.0-flash", contents=prompt
            )
            return {"ai_recommendation": response.text}
    except Exception as e:
        # Final fallback to Gemini if Groq fails
        try:
            response = google_client.models.generate_content(
                model="gemini-2.0-flash", contents=prompt
            )
            return {"ai_recommendation": response.text}
        except Exception as e2:
            return {"ai_recommendation": f"Error: AI services unavailable. {str(e2)}"}

# vision analysis using Fallback
def analyze_ingredients_from_image(image_bytes):
    prompt = "Identify all vegan ingredients in this image. Suggest one specific dish I can make. Format: 'DISHTAG: [Name of dish]'"
    
    try:
        if groq_client:
            base64_image = base64.b64encode(image_bytes).decode('utf-8')
            completion = groq_client.chat.completions.create(
                model="llama-3.2-11b-vision-preview",
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": prompt},
                            {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}
                        ]
                    }
                ]
            )
            return completion.choices[0].message.content
        else:
            # Fallback to Gemini Vision
            from google.genai import types
            response = google_client.models.generate_content(
                model="gemini-2.0-flash",
                contents=[prompt, types.Part.from_bytes(data=image_bytes, mime_type="image/jpeg")]
            )
            return response.text
    except Exception as e:
        return f"AI Analysis Failed: {str(e)}"

def generate_meal_image(meal_description):
    try:
        response = google_client.models.generate_image(
            model='imagen-3.0-generate-002', 
            prompt=f"Professional food photography of vegan {meal_description}, high quality food styling, 4k."
        )
        image_base64 = base64.b64encode(response.image_bytes).decode('utf-8')
        return {"image_data": f"data:image/png;base64,{image_base64}"}
    except:
        return {"image_data": ""}

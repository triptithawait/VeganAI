from fastapi import FastAPI, Request, HTTPException, Form, File, UploadFile
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import sqlite3
import brain 
import uvicorn
import os
from datetime import datetime

app = FastAPI()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
app.mount("/static", StaticFiles(directory=os.path.join(BASE_DIR, "static")), name="static")

# --- DATABASE SETUP (SQLite) ---
SQLITE_DB_PATH = os.path.join(BASE_DIR, "dietitian.db")

def get_db():
    """Returns a new SQLite connection (with row factory for dict-like access)."""
    conn = sqlite3.connect(SQLITE_DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Creates the history table if it doesn't exist."""
    conn = get_db()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            craving TEXT,
            result TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

init_db()
print(f"Connected to SQLite database: {SQLITE_DB_PATH}")


class UserInput(BaseModel):
    name: str
    goal: str
    allergies: str
    craving: str
    height: float = 0
    weight: float = 0
    bmi: float = 0
    language: str = "English"

@app.get("/", response_class=FileResponse)
async def read_root():
    return FileResponse(os.path.join(BASE_DIR, "templates", "login.html"))

@app.get("/auth", response_class=FileResponse)
async def read_auth():
    return FileResponse(os.path.join(BASE_DIR, "templates", "auth.html"))

@app.get("/dashboard", response_class=FileResponse)
async def read_dashboard():
    return FileResponse(os.path.join(BASE_DIR, "templates", "index.html"))

@app.post("/generate-recipe/")
async def generate_recipe(user_input: UserInput):
    try:
        # 1. Get the recipe from Gemini via brain.py
        result = brain.get_recipe_from_ai(user_input.dict())
        ai_text = result.get("ai_recommendation", "")

        # 2. SAVE to History Database (SQLite)
        if ai_text and "Error" not in ai_text:
            conn = get_db()
            conn.execute(
                "INSERT INTO history (craving, result, timestamp) VALUES (?, ?, ?)",
                (user_input.craving, ai_text, datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"))
            )
            conn.commit()
            conn.close()
            
        return result
    except Exception as e:
        return {"ai_recommendation": f"Error: {str(e)}"}

# --- HISTORY RETRIEVAL ROUTE ---
@app.get("/get-history/")
async def get_history():
    """Fetches the 5 most recent recipes from the database."""
    try:
        conn = get_db()
        rows = conn.execute(
            "SELECT craving, result, timestamp FROM history ORDER BY timestamp DESC LIMIT 5"
        ).fetchall()
        conn.close()
        
        history_data = [
            {
                "craving": row["craving"], 
                "result": row["result"], 
                "timestamp": row["timestamp"]
            } for row in rows
        ]
        return history_data
    except Exception as e:
        print(f"DATABASE ERROR: {e}")
        raise HTTPException(status_code=500, detail=f"Database Fetch Failed: {str(e)}")

@app.post("/clear-history/")
async def clear_history():
    """Wipes the history table."""
    try:
        conn = get_db()
        conn.execute("DELETE FROM history")
        conn.commit()
        conn.close()
        return {"status": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/generate-image/")
async def get_meal_image(meal_name: str):
    return brain.generate_meal_image(meal_name)

@app.post("/scan-ingredients/")
async def scan_ingredients(file: UploadFile = File(...)):
    try:
        image_bytes = await file.read()
        analysis = brain.analyze_ingredients_from_image(image_bytes)
        return {"analysis": analysis}
    except Exception as e:
        print(f"VISION ERROR: {e}")
        raise HTTPException(status_code=500, detail=f"AI Vision Failed: {str(e)}")

@app.post("/login")
async def login_user(username: str = Form(...), password: str = Form(...)):
    if username == "admin" and password == "1234":
        return {"status": "success"}
    raise HTTPException(status_code=401, detail="Invalid Credentials")

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8005)

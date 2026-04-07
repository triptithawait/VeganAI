import sqlite3
from pydantic import BaseModel
from typing import List, Optional

# --- Pydantic Models (For FastAPI validation) ---
class UserProfile(BaseModel):
    name: str
    health_conditions: List[str]
    is_strict_vegan: bool = True

class RecipeRequest(BaseModel):
    user_id: str
    current_craving: Optional[str] = "Surprise me"

# --- SQLite Database Logic (For permanent storage) ---
def init_db():
    conn = sqlite3.connect('dietitian.db')
    cursor = conn.cursor()
    
    # 1. Create Users Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id TEXT PRIMARY KEY,
            name TEXT,
            health_conditions TEXT,
            diet TEXT
        )
    ''')
    
    # 2. Create History Table to store past advice
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT,
            craving TEXT,
            advice TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # 3. Seed the database with your profile
    cursor.execute("""
        INSERT OR IGNORE INTO users VALUES 
        ('1', 'Tripti', 'Anemia, Low Energy', 'Strict Vegan')
    """)
    
    conn.commit()
    conn.close()

# Initialize the database immediately when this file is imported
init_db()
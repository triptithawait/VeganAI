import sqlite3
from pymongo import MongoClient
import os
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SQLITE_DB_PATH = os.path.join(BASE_DIR, "dietitian.db")
MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017/")
DB_NAME = os.getenv("MONGO_DB_NAME", "veganai_db")
COLLECTION_NAME = os.getenv("MONGO_COLLECTION_NAME", "history")

def migrate():
    # 1. Connect to SQLite
    if not os.path.exists(SQLITE_DB_PATH):
        print(f"Error: SQLite database not found at {SQLITE_DB_PATH}")
        return

    sqlite_conn = sqlite3.connect(SQLITE_DB_PATH)
    sqlite_cursor = sqlite_conn.cursor()

    # 2. Connect to MongoDB
    try:
        mongo_client = MongoClient(MONGO_URL, serverSelectionTimeoutMS=5000)
        db = mongo_client[DB_NAME]
        collection = db[COLLECTION_NAME]
        print("Connected to MongoDB...")
    except Exception as e:
        print(f"Failed to connect to MongoDB: {e}")
        return

    # 3. Fetch data from SQLite
    try:
        sqlite_cursor.execute("SELECT craving, result, timestamp FROM history")
        rows = sqlite_cursor.fetchall()
        print(f"Found {len(rows)} records in SQLite. Starting migration...")
    except sqlite3.OperationalError as e:
        print(f"Error reading SQLite: {e}")
        return

    # 4. Insert into MongoDB
    count = 0
    for row in rows:
        craving, result, timestamp_str = row
        
        # Convert timestamp string to datetime object if possible
        try:
            timestamp = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S")
        except:
            timestamp = datetime.utcnow()

        document = {
            "craving": craving,
            "result": result,
            "timestamp": timestamp,
            "migrated": True
        }
        
        collection.insert_one(document)
        count += 1

    print(f"Successfully migrated {count} records to MongoDB!")
    
    sqlite_conn.close()
    mongo_client.close()

if __name__ == "__main__":
    migrate()

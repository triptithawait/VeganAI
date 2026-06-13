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

def migrate_back():
    # 1. Connect to MongoDB
    try:
        mongo_client = MongoClient(MONGO_URL, serverSelectionTimeoutMS=5000)
        db = mongo_client[DB_NAME]
        collection = db[COLLECTION_NAME]
        print("Connected to MongoDB...")
    except Exception as e:
        print(f"Failed to connect to MongoDB: {e}")
        return

    # 2. Connect to SQLite (and create table if missing)
    sqlite_conn = sqlite3.connect(SQLITE_DB_PATH)
    sqlite_cursor = sqlite_conn.cursor()
    sqlite_cursor.execute('''
        CREATE TABLE IF NOT EXISTS history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            craving TEXT,
            result TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    sqlite_conn.commit()

    # 3. Fetch data from MongoDB
    mongo_data = list(collection.find())
    if not mongo_data:
        print("No data found in MongoDB to migrate.")
        return
        
    print(f"Found {len(mongo_data)} records in MongoDB. Starting migration back to SQLite...")

    # 4. Insert into SQLite
    count = 0
    for doc in mongo_data:
        craving = doc.get("craving", "")
        result = doc.get("result", "")
        timestamp = doc.get("timestamp")
        
        # Format timestamp for SQLite
        if isinstance(timestamp, datetime):
            timestamp_str = timestamp.strftime("%Y-%m-%d %H:%M:%S")
        else:
            timestamp_str = str(timestamp)

        sqlite_cursor.execute(
            "INSERT INTO history (craving, result, timestamp) VALUES (?, ?, ?)",
            (craving, result, timestamp_str)
        )
        count += 1

    sqlite_conn.commit()
    print(f"Successfully migrated {count} records back to SQLite!")
    
    sqlite_conn.close()
    mongo_client.close()

if __name__ == "__main__":
    migrate_back()

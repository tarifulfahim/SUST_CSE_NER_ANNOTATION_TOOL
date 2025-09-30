import json
from pymongo import MongoClient
from typing import List, Dict, Any

def connect_to_mongodb(connection_string: str = "mongodb://localhost:27017/", database_name: str = "your_database_name"):
    """
    Connect to MongoDB database
    """
    try:
        client = MongoClient(connection_string)
        db = client[database_name]
        print(f"Connected to MongoDB database: {database_name}")
        return db
    except Exception as e:
        print(f"Error connecting to MongoDB: {e}")
        return None

def fetch_tag_sentences_from_non_validates(db) -> List[Dict[str, Any]]:
    """
    Fetch all tag_sentence data from the validates collection
    """
    try:
        validates_collection = db.validates
        documents = validates_collection.find({}, {"tag_sentence": 1, "_id": 1})

        tag_sentences_data = []
        for doc in documents:
            tag_sentences_data.append({
                "id": str(doc.get("_id")),
                "tag_sentence": doc.get("tag_sentence", {})
            })

        print(f"Found {len(tag_sentences_data)} documents with tag_sentence data")
        return tag_sentences_data
    except Exception as e:
        print(f"Error fetching tag_sentences: {e}")
        return []

def save_to_json(data: List[Dict[str, Any]], filename: str = "tag_sentences_no_validate.json"):
    """
    Save tag_sentences data to JSON file
    """
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"Tag sentences saved to {filename}")
    except Exception as e:
        print(f"Error saving to JSON: {e}")

def main():
    # Configuration - Update these values according to your MongoDB setup
    CONNECTION_STRING = process.env("MONGO_URI") 
    DATABASE_NAME = process.env("DATABASE_NAME")
    OUTPUT_FILE = "tag_sentences.json"

    # Connect to MongoDB
    db = connect_to_mongodb(CONNECTION_STRING, DATABASE_NAME)
    if db is None:
        return

    # Fetch tag_sentence data from validates collection
    tag_sentences_data = fetch_tag_sentences_from_non_validates(db)
    if not tag_sentences_data:
        print("No tag_sentence data found or error occurred")
        return

    # Save to JSON file
    save_to_json(tag_sentences_data, OUTPUT_FILE)
    print(f"Process completed. {len(tag_sentences_data)} tag_sentences exported to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
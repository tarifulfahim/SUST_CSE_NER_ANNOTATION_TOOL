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

def fetch_sentences_from_validates(db) -> List[Dict[str, Any]]:
    """
    Fetch all sentences from the validates collection
    """
    try:
        validates_collection = db.validates
        documents = validates_collection.find({}, {"sentence": 1, "_id": 1})

        sentences_data = []
        for doc in documents:
            sentences_data.append({
                "id": str(doc.get("_id")),
                "sentence": doc.get("sentence", "")
            })

        print(f"Found {len(sentences_data)} documents with sentences")
        return sentences_data
    except Exception as e:
        print(f"Error fetching sentences: {e}")
        return []

def save_to_json(data: List[Dict[str, Any]], filename: str = "sentences.json"):
    """
    Save sentences data to JSON file
    """
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"Sentences saved to {filename}")
    except Exception as e:
        print(f"Error saving to JSON: {e}")

def main():
    # Configuration - Update these values according to your MongoDB setup
    CONNECTION_STRING = "mongodb://localhost:27017/"
    DATABASE_NAME = "your_database_name"
    OUTPUT_FILE = "sentences.json"

    # Connect to MongoDB
    db = connect_to_mongodb(CONNECTION_STRING, DATABASE_NAME)
    if not db:
        return

    # Fetch sentences from validates collection
    sentences_data = fetch_sentences_from_validates(db)
    if not sentences_data:
        print("No sentences found or error occurred")
        return

    # Save to JSON file
    save_to_json(sentences_data, OUTPUT_FILE)
    print(f"Process completed. {len(sentences_data)} sentences exported to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
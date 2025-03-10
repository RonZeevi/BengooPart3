from bson.objectid import ObjectId
from pprint import pprint
from utilities.db.db_connector import *

def analyze_db():
    """
    Function that prints all collections in the database
    and the values in each of them
    """
    # Connection check
    try:
        cluster.admin.command('ping')
        print("Database connection successful!\n")
    except Exception as e:
        print(f"Error connecting to database: {e}")
        return
    
    # Get list of all collections
    collections = bengoo.list_collection_names()
    print(f"Found {len(collections)} collections in the database:")
    
    # Print all collections and their data
    for collection_name in collections:
        print("\n" + "="*50)
        print(f"Collection: {collection_name}")
        print("="*50)
        
        # Get the collection
        collection = bengoo[collection_name]
        
        # Count documents in the collection
        count = collection.count_documents({})
        print(f"Number of documents: {count}")
        
        # Print all documents in the collection
        if count > 0:
            print("\nDocuments:")
            for doc in collection.find():
                # Convert ObjectId to string for printing
                if '_id' in doc and isinstance(doc['_id'], ObjectId):
                    doc['_id'] = str(doc['_id'])
                
                # Print the document in a formatted way
                pprint(doc)
                print("-"*30)
        else:
            print("\nNo documents in this collection.")

if __name__ == "__main__":
    analyze_db() 
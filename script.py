import pymongo
from faker import Faker
from datetime import datetime
import random
import threading
import time
import uuid
from datetime import datetime, timezone

# MongoDB Atlas connection string
MONGO_URI = "mongodb+srv://jhapiyush2013:5PnvrMPf1iPrRjsz@mongo-pagination-test.ghb1b.mongodb.net/"
DATABASE_NAME = "master"
COLLECTION_NAME = "application_data"

# Initialize Faker for random data generation
fake = Faker()

# Thread-safe unique ID generator
class UniqueIDGenerator:
    def __init__(self):
        self.counter = 3000022
        self.lock = threading.Lock()

    def get_next_id(self):
        with self.lock:
            self.counter += 1
            return self.counter

# Initialize the unique ID generator
id_generator = UniqueIDGenerator()

# Function to generate a single document
def generate_document():
    unique_id = id_generator.get_next_id()
    return {
        # "_id": pymongo.ObjectId(),
        "key": {
            "key": {
                "applicationId": unique_id  # Ensures unique applicationId
            }
        },
        "candidateDetails": {
            "candidateNumber": f"CAN-{unique_id}",  # Ensures unique candidateNumber
            "name": f"{fake.name()}"  # Ensures unique name
        },
        "baseDetails": {
            "status": random.choice(["ACTIVE", "PENDING", "COMPLETED","INACTIVE"]),
            "updatedDate": datetime.now()
        }
    }

# Function to insert documents into MongoDB
def insert_documents(collection, num_documents):
    batch_size = 10  # Number of documents to insert in each batch
    documents = []
    for _ in range(num_documents):
        documents.append(generate_document())
        if len(documents) == batch_size:
            collection.insert_many(documents)
            documents = []
    if documents:
        collection.insert_many(documents)

# Function to run multi-threaded insertion
def multi_threaded_insertion(collection, total_documents, num_threads):
    documents_per_thread = total_documents // num_threads
    threads = []

    for _ in range(num_threads):
        thread = threading.Thread(target=insert_documents, args=(collection, documents_per_thread))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

# Main function
def main():
    # Connect to MongoDB Atlas
    client = pymongo.MongoClient(MONGO_URI)
    db = client[DATABASE_NAME]
    collection = db[COLLECTION_NAME]

    # Configuration
    total_documents = 1_00_000 # Total number of documents to insert (10 million)
    num_threads = 5  # Number of threads to use for insertion

    # Start timer
    start_time = time.time()

    # Perform multi-threaded insertion
    print(f"Inserting {total_documents} documents using {num_threads} threads...")
    multi_threaded_insertion(collection, total_documents, num_threads)

    # End timer
    end_time = time.time()
    print(f"Insertion completed in {end_time - start_time:.2f} seconds.")

    # Close the MongoDB connection
    client.close()

if __name__ == "__main__":
    main()
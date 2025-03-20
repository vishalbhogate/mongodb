import pymongo
from pymongo.errors import PyMongoError

def simulate_validation_error():
    try:
        # Connect to MongoDB
        client = pymongo.MongoClient("mongodb://localhost:27017/")
        db = client["sj_release"]
        
        # Create a collection with schema validation
        db.create_collection("audit_log", validator={
            '$jsonSchema': {
                'bsonType': 'object',
                'properties': {
                    'msg': { 'bsonType': 'string' },
                    'time': { 'bsonType': 'date' }
                }
            }
        })
        
        # Insert a document that violates the schema
        db.audit_log.insert_one({"msg": "Test message", "time": "invalid_time"})

    except PyMongoError as e:
        print(f"Simulated PyMongoError: {e}")

# Run the function to simulate the error
simulate_validation_error()

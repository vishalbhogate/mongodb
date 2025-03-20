import argparse
import pymongo
import datetime
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get MongoDB credentials from env variables
MONGODB_USERNAME = os.getenv("MONGODB_USERNAME", "sj_user")
MONGODB_PASSWORD = os.getenv("MONGODB_PASSWORD", "securepassword")

# Connection URI for MongoDB
mongo_uri = f"mongodb://{MONGODB_USERNAME}:{MONGODB_PASSWORD}@localhost:27017/sj_release"

def insert_audit_log(user, service_name, release_tag):
    """Insert an audit log entry into MongoDB."""
    try:
        # Connect to MongoDB
        client = pymongo.MongoClient(mongo_uri)
        db = client["sj_release"]
        collection = db["audit_log"]

        # Create log document
        log_entry = {
            "msg": f"{user} deployed service {service_name}:{release_tag}",
            "time": datetime.datetime.utcnow()
        }

        # Insert into collection
        collection.insert_one(log_entry)
        print("Log entry inserted successfully!")

    except pymongo.errors.ConnectionError:
        print("Failed to connect to MongoDB. Ensure it's running and accessible.")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        client.close()

def show_entries():
    """Fetch and print all entries from the `audit_log` collection in MongoDB."""
    try:
        # Connect to MongoDB
        client = pymongo.MongoClient(mongo_uri)
        db = client["sj_release"]
        collection = db["audit_log"]
        
        # Fetch all documents from the collection
        entries = collection.find()
        
        # Print each document in a formatted way
        for entry in entries:
            print(entry)
    
    except pymongo.errors.ConnectionError:
        print("Failed to connect to MongoDB. Ensure it's running and accessible.")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        client.close()

# Parse command-line arguments
parser = argparse.ArgumentParser(description="Insert or view deployment logs in MongoDB.")
parser.add_argument("--user", required=False, help="Username of the person deploying.")
parser.add_argument("--service_name", required=False, help="Name of the service deployed.")
parser.add_argument("--release_tag", required=False, help="Release tag of the deployment.")
parser.add_argument("--view", action='store_true', help="Flag to view existing log entries")

args = parser.parse_args()

# If the --view flag is set, show entries from the MongoDB collection
if args.view:
    show_entries()
elif args.user and args.service_name and args.release_tag:
    # Otherwise, insert a new log entry
    insert_audit_log(args.user, args.service_name, args.release_tag)
else:
    print("Invalid arguments. Use --view to view entries or provide --user, --service_name, and --release_tag to insert a log.")

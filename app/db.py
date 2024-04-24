from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import os
from dotenv import load_dotenv

def init_db():
    # Loading from .env
    load_dotenv()
    uri = os.getenv('MONGODB_CONNECTION_STRING')
    print(uri)
    # Create a new client and connect to the server
    client = MongoClient(uri, server_api=ServerApi('1'))

    # Send a ping to confirm a successful connection
    try:
        client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
    except Exception as e:
        print(f"Encountered MongoDB error:\n{e}")
        exit(1)

    return client.get_database('demo')

DATABASE = init_db()
    
from pymongo import MongoClient
import os

_client = None
_db = None

def init_mongo():
    global _client, _db

    if _client is None:
        _client = MongoClient(
            os.getenv("DB_URI"),
            serverSelectionTimeoutMS=5000,
            connectTimeoutMS=5000,
            socketTimeoutMS=5000,
            retryWrites=True,
            tls=True
        )

        _db = _client["voting_project"]

def get_collection(name="voter_face_data"):
    if _db is None:
        raise RuntimeError("MongoDB not initialized")
    return _db[name]

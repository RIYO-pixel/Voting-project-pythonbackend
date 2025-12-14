from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError
from dotenv import load_dotenv
import os

load_dotenv()  # 🔥 THIS WAS MISSING

MONGO_URI = os.getenv("DB_URI")

if not MONGO_URI:
    raise RuntimeError("❌ MONGODB_URI is not set in environment")

_client = None

def create_connection():
    global _client
    try:
        if _client is None:
            _client = MongoClient(
                MONGO_URI,

                serverSelectionTimeoutMS=30000,
                connectTimeoutMS=30000,
                socketTimeoutMS=30000,

                retryReads=True,
                retryWrites=True,

                directConnection=False,
                tls=True,
                tlsAllowInvalidCertificates=False
            )

            _client.admin.command("ping")  # ✅ forces connection

        return _client

    except ServerSelectionTimeoutError as e:
        print("❌ MongoDB connection failed:", e)
        return None


def get_collection():
    client = create_connection()
    if client:
        return client["voting_project"]["voter_face_data"]
    return None


def close_connection():
    global _client
    if _client:
        _client.close()
        _client = None

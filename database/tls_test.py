from pymongo import MongoClient
import certifi

uri = "mongodb+srv://sanketdeystudent_db_user:Sanket7044@cluster0.ivuzumv.mongodb.net/voting_project?retryWrites=true&w=majority"
    

print("Creating client...")
client = MongoClient(
    uri,
    tls=True,
    tlsCAFile=certifi.where(),
    serverSelectionTimeoutMS=30000
)

print("Pinging MongoDB...")
client.admin.command("ping")
print("✅ BASIC TLS CONNECTION WORKS")

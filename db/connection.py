from pymongo import MongoClient, database
import os
from config import configure
from werkzeug.security import generate_password_hash as genph

configure()
client = MongoClient(os.getenv('MONGODB_SERVER'))

def create_admin_user():
    admin_email = "admin@gmail.com"
    admin_password =  genph("1234")
    client[os.getenv("DB_NAME")].admin.insert_one({"email":admin_email, "password":admin_password})

def create_database():
    if os.getenv("DB_NAME") not in client.list_database_names():
        database.Database(client, os.getenv("DB_NAME"))
        create_admin_user()
        print("Database Created")
    
db = client[os.getenv('DB_NAME')]
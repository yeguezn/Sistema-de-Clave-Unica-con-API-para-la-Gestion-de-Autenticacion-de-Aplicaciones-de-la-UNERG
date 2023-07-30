from pymongo import MongoClient
import os
from config import configure

configure()
client = MongoClient(os.getenv('MONGODB_SERVER'))
db = client["users"]
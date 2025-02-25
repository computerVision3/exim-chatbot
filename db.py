from pymongo import MongoClient
from config import settings

# MongoDB Connection
client = MongoClient(settings.MONGODB_URL)

# Database & Collection
db = client[settings.DB_NAME]
collection = db[settings.COL_NAME]
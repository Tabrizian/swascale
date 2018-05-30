from pymongo import MongoClient
from config import cfg

client = MongoClient(cfg['mongo']['MONGO_URI'])
db = client[cfg['mongo']['MONGO_DB']]

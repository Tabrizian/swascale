import pymongo
from config import cfg

client = MongoClient(cfg['MONGO']['MONGO_URI'])
db = client[cfg['MONGO']['MONGO_DB']]
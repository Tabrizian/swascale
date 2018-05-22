from pymodm import connect
from config import cfg

connect(cfg['mongo']['MONGO_URI'])

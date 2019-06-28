from .env import Env as TradingEnv
from pymongo import MongoClient
import gridfs
from rltrader.util import introspect


def do_train():
    client = MongoClient("mongodb://rltrainingdb")

    db = client['training']
    fs = gridfs.GridFS(db)

    sessions = list(db['sessions'].find({}))

    for session in sessions:
        pass


if __name__ == '__main__':
    do_train()

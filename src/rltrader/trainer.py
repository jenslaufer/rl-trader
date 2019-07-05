from .env import Env as TradingEnv
from pymongo import MongoClient
import gridfs
from di.factory import get_objects
import pandas as pd


def split_train_test(num):
    df = pd.read_csv('./data/btc.csv')
    df = df.sort_values('Timestamp')
    df = df.dropna().reset_index()[
        ['Open', 'High', 'Low', 'Close', 'Volume_(BTC)']]
    slice_point = int(len(df) - num)

    train_data = './data/train.csv'
    test_data = './data/test.csv'
    df[:slice_point].to_csv(train_data, index=False)
    df[slice_point:].to_csv(test_data, index=False)

    return train_data, test_data


def do_train():
    client = MongoClient("mongodb://rltrainingdb")

    db = client['training']
    fs = gridfs.GridFS(db)

    sessions = list(db['sessions'].find({}))

    for session in sessions:
        print(session['agent'])
        agent = get_objects(session['agent']['env'])
        print(agent)
        # agent.learn(total_timesteps=session['total_timesteps'])


if __name__ == '__main__':
    do_train()

from .env import Env as TradingEnv
from pymongo import MongoClient
import gridfs
from di.factory import get_objects
import pandas as pd
import io


def split_train_test(num):
    df = pd.read_csv('./data/btc.csv')
    df = df.sort_values('Timestamp')
    df = df.dropna().reset_index()[
        ['Open', 'High', 'Low', 'Close', 'Volume_(BTC)']]
    slice_point = int(len(df) - num)

    train_data = './data/train.csv'
    test_data = './data/test.csv'
    df[:slice_point].to_csv(train_data[:10000], index=False)
    df[slice_point:].to_csv(test_data[:1000], index=False)

    return train_data, test_data


def __do_train_session(session):
    model = get_objects(session['training'])
    model.learn(session['total_timesteps'])
    training_history = model.env.envs[0].states

    test_env = get_objects(session['test_env'])

    obs = test_env.reset()
    done = False
    while not done:
        action, _states = model.predict(obs)
        obs, rewards, done, info = test_env.step(action)

    test_history = test_env.states

    return model, training_history, test_history


def __to_csv(data, id, filename, fs):
    out = io.StringIO()
    pd.DataFrame(data).to_csv(out)

    fs.put(out.getvalue(), filename=filename,
           type='history', session_id=id,
           encoding="utf-8", contentType="text/csv")


def __save_model(model, id, fs):
    out = io.BytesIO()
    model.save(out)
    fs.put(out.getvalue(), filename="model",
           type='history', session_id=id,
           encoding="utf-8", contentType="application/octet-stream")


def do_train():
    client = MongoClient("mongodb://rltrainingdb")

    db = client['training']
    fs = gridfs.GridFS(db)

    sessions = list(db['sessions'].find({}))

    for session in sessions:
        id = session['_id']
        model, training_history, test_history = __do_train_session(session)
        __save_model(model, id, fs)
        __to_csv(training_history, id, "training_history.csv", fs)
        __to_csv(test_history, id, "test_history.csv", fs)


if __name__ == '__main__':
    split_train_test(30000)
    do_train()

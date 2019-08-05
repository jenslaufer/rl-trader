#from .env import Env as TradingEnv
from pymongo import MongoClient
import gridfs
from di.factory import get_objects
import pandas as pd
import io
from stable_baselines.common.policies import MlpPolicy
from stable_baselines.common.vec_env import DummyVecEnv
from stable_baselines import A2C
from .trading_env import TradingEnv

def __do_train_session(session):
    # model = get_objects(session['training'])
    df = pd.read_csv('/rldata/preprocessed/train_ZL000023_reduced.csv')
    env = DummyVecEnv([lambda: TradingEnv(df)])
    model = A2C(MlpPolicy, env, verbose=1)
    model.learn(session['total_timesteps'])
    training_history = model.env.envs[0].states

    test_env = get_objects(session['test_env'])

    obs = test_env.reset()
    done = False
    reward_sum = 0
    while not done:
        action, _states = model.predict(obs)
        obs, reward, done, info = test_env.step(action)
        reward_sum += reward

    test_history = test_env.states

    return model, reward_sum, training_history, test_history


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

    sessions = list(db['sessions'].find({"test_metrics": {'$exists': False}}))

    for session in sessions:
        id = session['_id']
        model, reward_sum, training_history, test_history = __do_train_session(
            session)
        db['sessions'].update_one({'_id': id}, {
            '$set': {
                'test_metrics': {'reward_sum': reward_sum}
            }
        }
        )
        __save_model(model, id, fs)
        __to_csv(training_history, id, "training_history.csv", fs)
        __to_csv(test_history, id, "test_history.csv", fs)


if __name__ == '__main__':
    do_train()

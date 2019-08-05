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
import logging
import logging.config
import yaml


def __do_train_session(session):
    # model = get_objects(session['training'])
    df = pd.read_csv('/rldata/preprocessed/train_ZL000023_reduced.csv')
    env = DummyVecEnv([lambda: TradingEnv(df)])
    model = A2C(MlpPolicy, env, verbose=1)
    logging.info('Starting learning phase...')
    model.learn(session['total_timesteps'])
    logging.info('Learning has been finished.')
    training_history = model.env.envs[0].states

    logging.info('Starting testing phase...')
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

    logging.info('loading training session from db...')
    sessions = list(db['sessions'].find({"test_metrics": {'$exists': False}}))

    for session in sessions:
        id = session['_id']
        logging.info('Starting training on session %(id)...', id)
        model, reward_sum, training_history, test_history = __do_train_session(
            session)
        logging.info('Storing training results...')
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
    logging.config.dictConfig(yaml.load(open('rltrader/logging.yml', 'r')))
    #logger = logging.getLogger(__name__)

    #logger.info('This is a debug message')
    #logging.basicConfig(filename='../application.log', level=logging.INFO)

    logging.info('This is a test message')
    do_train()

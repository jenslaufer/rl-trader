from .env import Env as TradingEnv
from .spaces import DataSpace
from .context import TradingContext
from .rewards import net_value_reward, end_net_value_reward
from stable_baselines.common.policies import MlpPolicy
from stable_baselines.common.vec_env import DummyVecEnv
from stable_baselines import A2C

import pandas as pd

from gym import spaces


def split_train_test(num):
    df = pd.read_csv('./data/btc.csv')
    df = df.sort_values('Timestamp')
    df = df.dropna().reset_index()[
        ['Open', 'High', 'Low', 'Close', 'Volume_(BTC)']]
    slice_point = int(len(df) - num)

    train_df = df[:slice_point]
    test_df = df[slice_point:]

    return train_df, test_df


def do_train():
    nums_testset = 200000
    train_df, test_df = split_train_test(nums_testset)

    env = TradingEnv(space=DataSpace(spaces.Discrete(3), 70, train_df, random_start=True, max_steps=200),
                     context=TradingContext(100000, 0.005, 3),
                     reward=net_value_reward)

    train_env = DummyVecEnv([lambda:env])

    model = A2C(MlpPolicy, train_env, verbose=1,
                tensorboard_log="./tensorboard/")
    model.learn(total_timesteps=200000)
    train_env.close()
    pd.DataFrame(env.states).to_csv("train.csv")

    env = TradingEnv(space=DataSpace(spaces.Discrete(3), 70, test_df),
                     context=TradingContext(100000, 0.005, 3),
                     reward=net_value_reward)

    test_env = DummyVecEnv([lambda:env])

    obs = test_env.reset()
    for i in range(nums_testset):
        action, _states = model.predict(obs)
        obs, rewards, done, info = test_env.step(action)

    test_env.close()
    pd.DataFrame(env.states.to_csv("test.csv")


if __name__ == '__main__':
    do_train()

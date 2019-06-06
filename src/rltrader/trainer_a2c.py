from .env import Env as TradingEnv
from .spaces import LookbackWindowDataSpace
from .context import TradingContext
from .rewards import net_value_reward, end_net_value_reward, net_value_reward_wrong_action_penalty
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
    action_space = spaces.Discrete(3)
    history_lookback = 70
    max_steps = 10080
    initial_fundings = 100000
    trading_loss_pct = 0.005
    price_col_index = 3
    total_timesteps = 201600
    reward_fct = net_value_reward_wrong_action_penalty

    nums_testset = 259200
    train_df, test_df = split_train_test(nums_testset)

    data_space = LookbackWindowDataSpace(action_space=action_space,
                                         history_lookback=history_lookback,
                                         data=train_df,
                                         random_start=True,
                                         max_steps=max_steps)
    trading_context = TradingContext(
        initial_fundings=initial_fundings,
        trading_loss_pct=trading_loss_pct,
        price_col_index=price_col_index)

    env = TradingEnv(space=data_space,
                     context=trading_context,
                     reward=reward_fct)

    train_env = DummyVecEnv([lambda:env])

    model = A2C(MlpPolicy, train_env, verbose=1,
                tensorboard_log="./tensorboard/")
    model.learn(total_timesteps=total_timesteps)
    train_env.close()
    pd.DataFrame(env.states).to_csv("train.csv")
    print("=================================")
    print("Model trained.")

    data_space = LookbackWindowDataSpace(action_space=action_space,
                                         history_lookback=history_lookback,
                                         data=test_df)
    trading_context = TradingContext(initial_fundings=initial_fundings,
                                     trading_loss_pct=trading_loss_pct,
                                     price_col_index=price_col_index)
    env = TradingEnv(space=data_space,
                     context=trading_context,
                     reward=reward_fct,
                     context_reset=False)

    test_env = DummyVecEnv([lambda:env])

    obs = test_env.reset()
    done = False
    while not done:
        action, _states = model.predict(obs)
        obs, rewards, done, info = test_env.step(action)

    pd.DataFrame(env.states).to_csv("test.csv")
    print(trading_context.balance)


if __name__ == '__main__':
    do_train()

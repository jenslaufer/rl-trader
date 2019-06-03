from .env import Env as TradingEnv
from .spaces import DataSpace
from .context import TradingContext
from .rewards import net_value_reward

from collections import deque
import numpy as np

from keras.models import Model, Sequential
from keras.layers import LeakyReLU, Input, Dense, Conv3D, Conv1D, Dense, \
    Flatten, MaxPooling1D, MaxPooling2D, MaxPooling3D, Concatenate, Activation
from keras.optimizers import Adam
import pandas as pd
from datetime import datetime

from rl.agents.dqn import DQNAgent
from rl.policy import LinearAnnealedPolicy, BoltzmannQPolicy, EpsGreedyQPolicy
from rl.memory import SequentialMemory

from gym import spaces

from stable_baselines.common.policies import MlpPolicy
from stable_baselines.common.vec_env import DummyVecEnv
from stable_baselines import A2C


def build_network_for_sparsed(input_shape, optimizer='adam', init_mode='uniform', filters=16,
                              neurons=20, activation='relu'):
    model = Sequential()
    model.add(Flatten(input_shape=input_shape))
    model.add(Dense(16))
    model.add(Activation('relu'))
    model.add(Dense(16))
    model.add(Activation('relu'))
    model.add(Dense(16))
    model.add(Activation('relu'))
    model.add(Dense(2))
    model.add(Activation('linear'))
    model.compile(optimizer=optimizer, loss='mse',
                  metrics=['mae', 'mape', 'mse'])

    model.summary()

    return model


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

    WINDOW_LENGTH = 4

    nums_testset = 20000
    train_df, test_df = split_train_test(nums_testset)

    space = DataSpace(spaces.Discrete(3), 70, train_df)
    context = TradingContext(100000, 0.005, 3)

    env = TradingEnv(space=space, context=context, reward=net_value_reward)

    model = build_network_for_sparsed(
        input_shape=((WINDOW_LENGTH,) + env.observation_space.shape))

    memory = SequentialMemory(limit=1000000, window_length=WINDOW_LENGTH)

    policy = LinearAnnealedPolicy(EpsGreedyQPolicy(), attr='eps', value_max=1., value_min=.1, value_test=.05,
                                  nb_steps=1000000)

    dqn = DQNAgent(model=model, nb_actions=2, memory=memory, nb_steps_warmup=10,
                   target_model_update=1e-2, policy=policy, enable_dueling_network=True, enable_double_dqn=True)

    dqn.compile(Adam(lr=1e-3), metrics=['mae'])

    dqn.fit(env, nb_steps=nums_testset, log_interval=50)

    pd.DataFrame(env.history).to_csv("train.csv")

    space = DataSpace(spaces.Discrete(3), 70, test_df)
    context = TradingContext(100000, 0.005, 3)

    test_env = TradingEnv(space=space, context=context,
                          reward=net_value_reward)
    dqn.test(test_env, nb_episodes=1000, visualize=True)

    pd.DataFrame(test_env.history).to_csv("test.csv")


if __name__ == '__main__':
    do_train()

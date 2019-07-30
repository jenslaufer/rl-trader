from gym import spaces
import random
from sklearn import preprocessing
import pandas as pd


class Space:

    def __init__(self, action_space, observation_space):
        self.action_space = action_space
        self.observation_space = observation_space

    def next_observation(self):
        return None


class LookbackWindowDataSpace(Space):

    __scaler = preprocessing.MinMaxScaler()

    def __init__(self, action_space, history_lookback, data, date_col=None,
                 max_steps=6000, random_start=False, seed=None):
        if seed != None:
            random.seed(seed)

        self.__random_start = random_start
        self.data = data.frame
        self.history_lookback = history_lookback
        self.max_steps = max_steps
        self.date_col = date_col

        ncols = len(self.data.columns)
        if date_col != None:
            ncols -=1

        observation_space = spaces.Box(
            low=0, high=1, shape=(history_lookback + 1, ncols))
        super(LookbackWindowDataSpace, self).__init__(
            action_space, observation_space)
        self.reset()

    def reset(self):
        if self.__random_start:
            self.current_index = random.randint(
                self.history_lookback, len(self.data))
        else:
            self.current_index = self.history_lookback + 1

        self.end = self.current_index + self.max_steps
        if not self.__random_start or (self.end >= len(self.data)):
            self.end = len(self.data)

        print("===Space reset: start:{} end:{}===".format(
            self.current_index, self.end))

    def next_observation(self):
        done = False
        obs = None
        scaled_obs = None

        if self.date_col != None:
            self.data = self.data[self.data.columns.difference(
                [self.date_col])]

        if self.current_index <= self.end:
            obs = self.data[self.current_index -
                            self.history_lookback - 1: self.current_index]
            scaled_obs = self.__scaler.fit_transform(obs)
            obs = obs.values
        if self.current_index >= self.end:
            done = True

        self.current_index += 1

        return (obs, scaled_obs, done)

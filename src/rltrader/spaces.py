from gym import spaces
import random
from sklearn import preprocessing
import pandas as pd
import numpy as np
import logging


class Space:

    def __init__(self, action_space, observation_space):
        self.action_space = action_space
        self.observation_space = observation_space

        # TODO split action_space from observation_space
        # -> remove space class??
        # -> rename to state

    def next_observation(self):
        return None


class LookbackWindowDataSpace(Space):

    __scaler = preprocessing.MinMaxScaler()

    def __init__(self, history_lookback, data, date_col=None,
                 max_steps=6666, random_start=False, seed=None):
        if seed != None:
            random.seed(seed)

        self.__random_start = random_start
        self.data = data.frame
        self.history_lookback = history_lookback
        self.max_steps = max_steps
        self.date_col = date_col

        ncols = len(self.data.columns)
        if date_col != None:
            ncols -= 1

        # static part of the observation space contains the OHCL values for the last (history_lookback + 1) prices
        observation_space = spaces.Box(
            low=0, high=1, shape=(history_lookback + 1, ncols))

        # actions of the format Buy x%, Sell x%, Hold, etc.
        action_space = spaces.Box(
            low=np.array([0, 0]), high=np.array([3, 1]), dtype=np.float16)

        super(LookbackWindowDataSpace, self).__init__(
            action_space, observation_space)

        # self.reset()

    def reset(self):
        # sets the current starting point within the data frame...
        if self.__random_start:
            self.current_index = random.randint(
                self.history_lookback, len(self.data))
        else:
            self.current_index = self.history_lookback + 1

        # sets end point...
        self.end = self.current_index + self.max_steps
        if not self.__random_start or (self.end >= len(self.data)):
            self.end = len(self.data)

        logging.info("Space resetted to {start: %s, end: %s}.",
                     self.current_index, self.end)

    def next_observation(self):
        done = False
        obs = None
        scaled_obs = None

        # remove data column if exists...
        if self.date_col != None:
            self.data = self.data[self.data.columns.difference(
                [self.date_col])]

        # take observations including history_lookback...
        if self.current_index <= self.end:
            obs = self.data[self.current_index -
                            self.history_lookback - 1: self.current_index]
            scaled_obs = self.__scaler.fit_transform(obs)
            obs = obs.values

        if self.current_index >= self.end:
            done = True

        self.current_index += 1
        self.current_obs = obs
        self.current_scaled_obs = scaled_obs

        return (obs, scaled_obs, done)

    # helper method - delete when we got rid of any dependency to obs in context
    def get_current_obs(self):
        return self.current_obs, self.current_scaled_obs

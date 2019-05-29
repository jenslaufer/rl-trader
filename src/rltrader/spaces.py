from gym import spaces
import random
from sklearn import preprocessing


class Space:

    def __init__(self, action_space, observation_space):
        self.action_space = action_space
        self.observation_space = observation_space

    def next_observation(self):
        return None


class DataSpace(Space):

    __scaler = preprocessing.MinMaxScaler()

    def __init__(self, action_space, history_lookback, data, random_start=False, seed=None):
        if seed != None:
            random.seed(seed)
        self.__random_start = random_start
        self.data = data
        self.history_lookback = history_lookback
        observation_space = spaces.Box(
            low=0, high=1, shape=(len(data.columns), history_lookback+1))
        super().__init__(action_space, observation_space)
        self.__reset()

    def __reset(self):
        if self.__random_start:
            self.current_index = random.randint(
                self.history_lookback, len(self.data))
        else:
            self.current_index = (len(self.data) - self.history_lookback) + 1

    def next_observation(self):
        done = False
        obs = None
        scaled_obs = None

        if self.current_index <= len(self.data):
            obs = self.data[self.current_index -
                            self.history_lookback - 1: self.current_index]
            scaled_obs = self.__scaler.fit_transform(obs)
        if self.current_index >= len(self.data):
            done = True

        self.current_index += 1

        return (obs, scaled_obs, done)

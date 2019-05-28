from gym import spaces


class Space:

    def __init__(self, action_space, observation_space):
        self.action_space = action_space
        self.observation_space = observation_space


class DataSpace(Space):

    def __init__(self, action_space, lookback, data):
        self.data = data
        self.lookback = lookback
        observation_space = spaces.Box(
            low=0, high=1, shape=(len(data.columns), lookback+1))
        super().__init__(action_space, observation_space)

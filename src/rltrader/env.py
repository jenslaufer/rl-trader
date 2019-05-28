from gym import Env as BaseEnv


class Env(BaseEnv):

    def __init__(self, space):
        self.action_space = space.action_space
        self.observation_space = space.observation_space

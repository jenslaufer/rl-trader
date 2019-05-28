from gym import Env as BaseEnv


class Env(BaseEnv):

    def __init__(self, space):
        self.action_space = space.action_space
        self.observation_space = space.observation_space

    def reset(self):
        obs = None
        return obs

    def step(self, action):
        obs = None
        reward = 0
        done = False
        info = {}
        return obs, reward, done, info

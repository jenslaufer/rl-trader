from gym import Env as BaseEnv


class Env(BaseEnv):

    def __init__(self, space):
        self.action_space = space.action_space
        self.observation_space = space.observation_space
        self.space = space

    def reset(self):
        obs, done = self.space.next_observation()
        return obs

    def step(self, action):
        obs, done = self.space.next_observation()
        reward = 0
        info = {}
        return obs, reward, done, info

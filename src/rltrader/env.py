from gym import Env as BaseEnv


class Env(BaseEnv):

    def __init__(self, space, context, reward):
        self.action_space = space.action_space
        self.observation_space = space.observation_space
        self.space = space
        self.context = context
        self.reward = reward
        self.context_data = {}

    def reset(self):
        obs, scaled_obs, done = self.space.next_observation()

        return scaled_obs

    def step(self, action):
        obs, scaled_obs, done = self.space.next_observation()
        old_context = self.context_data
        done_act, context_data = self.context.act(action, obs)
        reward = self.reward(old_context, context_data, obs)
        self.context_data = context_data

        return (scaled_obs, reward, (done | done_act), context_data)

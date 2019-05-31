from gym import Env as BaseEnv


class Env(BaseEnv):

    def __init__(self, space, context):
        self.action_space = space.action_space
        self.observation_space = space.observation_space
        self.space = space
        self.context = context

    def reset(self):
        obs, scaled_obs, done = self.space.next_observation()

        return scaled_obs

    def step(self, action):
        obs, scaled_obs, done = self.space.next_observation()
        context_before_action = self.context
        done_act = self.context.act(action, obs)
        context_after_action = self.context
        reward = 0

        return (scaled_obs, reward, (done | done_act), vars(context_after_action))

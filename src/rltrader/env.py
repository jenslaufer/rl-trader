from gym import Env as BaseEnv


class Env(BaseEnv):

    def __init__(self, space, context, reward):
        self.action_space = space.action_space
        self.observation_space = space.observation_space
        self.space = space
        self.context = context
        self.reward = reward
        self.states = []
        self.states.append(self.context.state)

    def reset(self):
        obs, scaled_obs, done = self.space.next_observation()

        return scaled_obs

    def step(self, action):
        obs, scaled_obs, done = self.space.next_observation()
        old_state = self.context.state
        done_act = self.context.act(action, obs)
        current_state = self.context.state
        reward = self.reward(old_state, current_state, obs)
        self.states.append(self.context.state)

        return (scaled_obs, reward, (done | done_act), current_state)

    def history(self):
        return self.states

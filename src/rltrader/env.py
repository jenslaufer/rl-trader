from gym import Env as BaseEnv


class Env(BaseEnv):

    def __init__(self, space, context, reward):
        self.action_space = space.action_space
        self.observation_space = space.observation_space
        self.space = space
        self.context = context
        self.reward = reward
        self.states = []

    def reset(self):
        obs, scaled_obs, done = self.space.next_observation()

        return scaled_obs

    def step(self, action):
        obs, scaled_obs, done_obs = self.space.next_observation()

        done_act, old_state, current_state, obs = self.context.act(action, obs)

        done = (done_obs | done_act)

        if len(self.states) == 0:
            self.states.append(old_state)

        self.states.append(current_state)

        reward = self.reward(old_state, current_state, action, obs, done)

        if done:
            self.space.reset()
            self.context.reset()

        current_state['reward'] = reward
        current_state['action'] = action

        return (scaled_obs, reward, done, current_state)

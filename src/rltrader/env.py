from gym import Env as BaseEnv
import numpy as np


class Env(BaseEnv):

    def __init__(self, space, context, reward, context_reset=True):
        self.action_space = space.action_space
        self.observation_space = space.observation_space
        self.space = space
        self.context = context
        self.reward = reward
        self.context_reset = context_reset
        self.states = []
        super(Env, self).__init__()

    def reset(self):
        print("\n\n===Env reset===")

        self.space.reset()
        if self.context_reset:
            self.context.reset()

        obs, scaled_obs, done = self.space.next_observation()

        return scaled_obs

    def step(self, action):
        obs, scaled_obs, done_obs = self.space.next_observation()

        done_act, old_state, current_state = self.context.act(
            action, obs, scaled_obs)

        done = (done_obs | done_act)

        if len(self.states) == 0:
            self.states.append(old_state)

        self.states.append(current_state)

        reward = self.reward(old_state, current_state, action, obs, done)

        current_state['reward'] = reward
        current_state['action'] = action
        current_state['done'] = done

        return (scaled_obs, reward, done, current_state)

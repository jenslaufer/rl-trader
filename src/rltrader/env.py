from gym import Env as BaseEnv
import numpy as np
import logging


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
        logging.info("Resetting environment...")

        # resetting observation space
        self.space.reset()

        # resetting account data
        if self.context_reset:
            self.context.reset()

        obs, scaled_obs, done = self.space.next_observation()

        # TODO consider appending additional account data to observations
        # self.balance / MAX_ACCOUNT_BALANCE,
        # self.max_net_worth / MAX_ACCOUNT_BALANCE,
        # self.shares_held / MAX_NUM_SHARES,
        # self.cost_basis / MAX_SHARE_PRICE,
        # self.total_shares_sold / MAX_NUM_SHARES,
        # self.total_sales_value / (MAX_NUM_SHARES * MAX_SHARE_PRICE),

        return obs
        # return scaled_obs

    def step(self, action):
        # TODO consider moving next_observation() call to end??
        obs, scaled_obs, last_timestep_reached = self.space.next_observation()

        net_worth_depleted, old_state, current_state = self.context.act(
            action, obs, scaled_obs)

        done = (last_timestep_reached | net_worth_depleted)

        # TODO consider removing this, in case we moved to next obs at the end
        if len(self.states) == 0:
            self.states.append(old_state)

        self.states.append(current_state)

        reward = self.reward(old_state, current_state, action, obs, done)

        current_state['reward'] = reward
        current_state['action'] = action
        current_state['done'] = done

        return (obs, reward, done, current_state)
        # return (scaled_obs, reward, done, current_state)

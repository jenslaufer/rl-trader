from gym import Env as BaseEnv
import numpy as np
import logging
import math
from math import log


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
        # TODO there should be no dependency to obs / scaled_obs in .act(...)
        obs, scaled_obs = self.space.get_current_obs()
        net_worth_depleted, old_state, current_state = self.context.act(
            action, obs, scaled_obs)
        action_type = self.context.render_action_type(action[0])
        action_amount = action[1]
        logging.debug('Action taken: %s (%s)', action_type, action_amount)

        # TODO consider removing this, in case we moved to next obs at the end
        if len(self.states) == 0:
            self.states.append(old_state)

        self.states.append(current_state)
        logging.debug('Account state: %s', current_state)

        # TODO fix dynamic reward function call
        #reward = self.reward(old_state, current_state, action, obs, done)
        # print(old_state)
        # print(current_state)
        old_net_worth = old_state['net_worth']
        current_net_worth = current_state['net_worth']
        reward = log(current_net_worth) - log(old_net_worth)
        logging.debug('Reward received: %s', reward)

        obs, scaled_obs, last_timestep_reached = self.space.next_observation()
        done = (last_timestep_reached | net_worth_depleted)

        current_state['reward'] = reward
        current_state['action_type'] = action[0]
        current_state['action_amount'] = action[1]
        current_state['done'] = done

        return (obs, reward, done, current_state)
        # return (scaled_obs, reward, done, current_state)

    def render(self, current_state):
        # Render the environment to the screen
        profit = current_state['net_worth'] - current_state['initial_fundings']

        logging.debug('##### Step: %s #####', self.space.current_index)
        logging.debug('Balance: %s', current_state['balance'])
        logging.debug(
            'Assets held: %s (Total sold: %s)', current_state['asset_balance'], current_state['total_assets_sold'])
        # logging.debug(
        #     'Avg cost for held assets: %s (Total sales value: %s)', current_state['cost_basis'], current_state['total_sales_value'])
        logging.debug(
            'Net worth: %s (Max net worth: %s)', current_state['net_worth'], current_state['max_net_worth'])
        logging.debug('Profit: %s', profit)

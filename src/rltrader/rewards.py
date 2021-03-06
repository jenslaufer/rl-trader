import math
from math import log


def net_value_reward(old, current, action, obs, done):
    old_balance = old['balance']
    old_asset_balance = old['asset_balance']
    old_price = old['current_price']

    balance = current['balance']
    asset_balance = current['asset_balance']
    price = current['current_price']

    net_value = (balance + asset_balance * price) - \
        (old_balance + old_asset_balance * old_price)

    return net_value


def end_net_value_reward(old, current, action, obs, done):
    if done:
        old_balance = old['balance']
        old_asset_balance = old['asset_balance']
        old_price = old['current_price']

        balance = current['balance']
        asset_balance = current['asset_balance']
        price = current['current_price']

        return (balance + asset_balance * price) - (old_balance + old_asset_balance * old_price)
    else:
        return 0


def net_value_reward_wrong_action_penalty(old, current, action, obs, done):
    old_balance = old['balance']
    old_asset_balance = old['asset_balance']
    old_price = old['current_price']

    balance = current['balance']
    asset_balance = current['asset_balance']
    price = current['current_price']

    reward = net_value_reward(old, current, action, obs, done)

    if action == 1:
        if balance == old_balance:
            reward = reward-1000000
    elif action == 2:
        if asset_balance == old_asset_balance:
            reward = reward-1000000

    return reward


def portfolio_log(old, current, action, obs, done):
    old_net_worth = old['net_worth']
    current_net_worth = current['net_worth']

    # TODO consider using this
    # delay_factor = (current_step / max_steps)

    reward = log(current_net_worth) - log(old_net_worth)  # + log(delay_factor)

    return reward

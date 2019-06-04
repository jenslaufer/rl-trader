
def net_value_reward(old, current, action, obs, done):
    old_balance = old['balance']
    old_asset_balance = old['asset_balance']
    old_price = old['price']

    balance = current['balance']
    asset_balance = current['asset_balance']
    price = current['price']

    net_value = (balance + asset_balance * price) - \
        (old_balance + old_asset_balance * old_price)

    return net_value


def end_net_value_reward(old, current, action, obs, done):
    if done:
        old_balance = old['balance']
        old_asset_balance = old['asset_balance']
        old_price = old['price']

        balance = current['balance']
        asset_balance = current['asset_balance']
        price = current['price']

        return (balance + asset_balance * price) - (old_balance + old_asset_balance * old_price)
    else:
        return 0


def net_value_reward_wrong_action_penalty(old, current, action, obs, done):
    old_balance = old['balance']
    old_asset_balance = old['asset_balance']
    old_price = old['price']

    balance = current['balance']
    asset_balance = current['asset_balance']
    price = current['price']

    reward = net_value_reward(old, current, action, obs, done)

    if action == 1:
        if old_balance == balance:
            reward = -100000
    elif action == 2:
        if old_asset_balance == asset_balance:
            reward = -100000

    return reward

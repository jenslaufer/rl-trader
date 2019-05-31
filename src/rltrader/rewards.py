
def net_value_reward(old, current, obs):
    old_balance = old['balance']
    old_asset_balance = old['asset_balance']
    old_price = old['price']

    balance = current['balance']
    asset_balance = current['asset_balance']
    price = current['price']

    return (balance + asset_balance * price) - (old_balance + old_asset_balance * old_price)

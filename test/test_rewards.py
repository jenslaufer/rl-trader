import context
from rltrader.rewards import net_value_reward, end_net_value_reward


def test_net_value_reward():
    old_state = {"balance": 5, "asset_balance": 100, "price": 4}
    current_state = {"balance": 13, "asset_balance": 80, "price": 8}
    obs = []

    assert net_value_reward(old_state, current_state, 1, obs, False) == 248


def test_end_net_value_reward():
    old_state = {"balance": 5, "asset_balance": 100, "price": 4}
    current_state = {"balance": 13, "asset_balance": 80, "price": 8}
    obs = []

    assert end_net_value_reward(old_state, current_state, 1, obs, True) == 248

    old_state = {"balance": 5, "asset_balance": 100, "price": 4}
    current_state = {"balance": 13, "asset_balance": 80, "price": 8}
    obs = []

    assert end_net_value_reward(old_state, current_state, 1, obs, False) == 0

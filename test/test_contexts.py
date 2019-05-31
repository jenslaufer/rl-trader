import context
from rltrader import context as rlcontext
import numpy as np


def get_context(fundings, trading_loss_pct, price_col_index):
    return rlcontext.TradingContext(fundings, trading_loss_pct, price_col_index)


def test_init():
    fundings = 100000
    trading_loss_pct = 0.01
    price_col_index = 3
    context = get_context(fundings, trading_loss_pct, price_col_index)

    assert context.trading_loss_pct == trading_loss_pct
    assert context.balance == fundings
    assert context.asset_balance == 0
    assert context.price_col_index == 3


def test_act_buy_sell():
    fundings = 100000
    trading_loss_pct = 0.001
    price_col_index = 0
    context = get_context(fundings, trading_loss_pct, price_col_index)

    action = 1
    obs = np.array([[10, 100], [6, 75], [2, 0]])

    done_act = context.act(action, obs)
    assert not done_act
    assert context.balance == 0
    assert context.asset_balance == 49950.0
    assert context.state == {'fees': 100.0, 'price': 2,
                             'balance': 0, 'asset_balance': 49950.0}
    action = 0
    obs = np.array([[100, 1000], [7, 751], [32, 100]])

    done_act = context.act(action, obs)
    print(context.state)
    assert not done_act
    assert context.balance == 0
    assert context.asset_balance == 49950.0
    assert context.state == {'fees': 0, 'price': 32,
                             'balance': 0, 'asset_balance': 49950.0}

    action = 2
    obs = np.array([[6, 75], [2, 0], [5, 9]])
    done_act = context.act(action, obs)
    print(context.state)
    assert not done_act
    assert context.balance == 249500.25
    assert context.asset_balance == 0
    assert context.state == {'fees': 249.75, 'price': 5, 'balance': 249500.25, 'asset_balance': 0.0}

import context
from rltrader import context as rlcontext


def get_context(fundings, trading_loss_pct):
    return rlcontext.TradingContext(fundings, trading_loss_pct)


def test_init():
    fundings = 100000
    trading_loss_pct = 0.01
    context = get_context(fundings, trading_loss_pct)

    assert context.initial_fundings == fundings
    assert context.trading_loss_pct == trading_loss_pct
    assert context.balance == 0
    assert context.asset_balance == 0

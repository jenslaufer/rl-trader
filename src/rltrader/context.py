class Context:

    def act(self, action, observation):
        return (0, False)


class TradingContext(Context):
    HOLD = 0
    BUY = 1
    SELL = 2

    def __init__(self, initial_fundings, trading_loss_pct, price_col_index):
        self.trading_loss_pct = trading_loss_pct
        self.initial_fundings = initial_fundings
        self.price_col_index = price_col_index
        self.reset()

    def reset(self):
        print("===Context Reset===")
        self.balance = self.initial_fundings
        self.asset_balance = 0
        self.fees = 0
        self.price = 0

    def _get_state(self):
        return {'fees': self.fees,
                'price': self.price,
                'balance': self.balance,
                'asset_balance': self.asset_balance}

    def act(self, action, obs):
        old_state = self._get_state()
        done = False

        self.price = obs[len(obs) - 1][self.price_col_index]
        self.fees = 0

        if action == self.BUY:
            self._buy()
        elif action == self.SELL:
            self._sell()

        current_state = self._get_state()

        return done, old_state, current_state, obs

    def close(self):
        self._sell()

    def _buy(self):
        if self.balance > 0:
            self.fees = self.balance * self.trading_loss_pct
            self.asset_balance = (self.balance - self.fees)/self.price
            self.balance -= self.balance

    def _sell(self):
        if self.asset_balance > 0:
            sold = self.asset_balance * self.price
            self.fees = sold * self.trading_loss_pct
            self.asset_balance -= self.asset_balance
            self.balance = sold - self.fees

class Context:

    def act(self, action, observation):
        return (0, False)


class TradingContext(Context):

    def __init__(self, initial_fundings, trading_loss_pct, price_col_index):
        self.trading_loss_pct = trading_loss_pct
        self.balance = initial_fundings
        self.asset_balance = 0
        self.fees = 0
        self.price = 0
        self.price_col_index = price_col_index

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

        if action == 1:
            if self.balance > 0:
                self.fees = self.balance * self.trading_loss_pct
                self.asset_balance = (self.balance - self.fees)/self.price
                self.balance -= self.balance
        elif action == 2:
            if self.asset_balance > 0:
                sold = self.asset_balance * self.price
                self.fees = sold * self.trading_loss_pct
                self.balance = sold - self.fees
                self.asset_balance -= self.asset_balance

        current_state = self._get_state()

        return done, old_state, current_state, obs

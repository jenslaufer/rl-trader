class Context:

    def act(self, action, observation):
        return (0, False)


class TradingContext(Context):

    def __init__(self, initial_fundings, trading_loss_pct, price_col_index):
        self.trading_loss_pct = trading_loss_pct
        self.balance = initial_fundings
        self.asset_balance = 0
        self.price_col_index = price_col_index

        self.state = {}
        self.state['fees'] = None
        self.state['price'] = None
        self.state['balance'] = self.balance
        self.state['asset_balance'] = self.asset_balance

    def act(self, action, obs):
        done = False
        price = obs[len(obs) - 1][self.price_col_index]
        fees = 0

        if action == 1:
            if self.balance > 0:
                fees = self.balance * self.trading_loss_pct
                self.asset_balance = (self.balance - fees)/price
                self.balance -= self.balance
        elif action == 2:
            sold = self.asset_balance * price
            fees = sold * self.trading_loss_pct
            self.balance = sold - fees
            self.asset_balance -= self.asset_balance

        self.state['fees'] = fees
        self.state['price'] = price
        self.state['balance'] = self.balance
        self.state['asset_balance'] = self.asset_balance

        return done

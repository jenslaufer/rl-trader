class Context:

    def act(self, action, observation):
        return (0, False)


class TradingContext(Context):

    def __init__(self, initial_fundings, trading_loss_pct, price_col_index):
        self.trading_loss_pct = trading_loss_pct
        self.balance = initial_fundings
        self.asset_balance = 0
        self.price_col_index = price_col_index

    def act(self, action, obs):
        done = False
        price = obs[len(obs) - 1][self.price_col_index]
        fees = 0
        old_balance = self.balance
        old_asset_balance = self.asset_balance

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

        context_data = vars(self)
        context_data['fees'] = fees
        context_data['price'] = price
        context_data['old_balance'] = old_balance
        context_data['old_asset_balance'] = old_asset_balance

        return (done, context_data)

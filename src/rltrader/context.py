class Context:

    def act(self, action, observation):
        return (0, False)


class DummyContext(Context):

    def __init__(self):
        self.done = [False, True, False]
        self.current_index = 0

    def act(self, action, observation):
        done = False
        done = self.done[self.current_index]
        self.current_index += 1

        return done


class TradingContext(Context):

    def __init__(self, initial_fundings, trading_loss_pct, price_col_index):
        self.initial_fundings = initial_fundings
        self.trading_loss_pct = trading_loss_pct
        self.balance = initial_fundings
        self.asset_balance = 0
        self.price_col_index = price_col_index

    def act(self, action, obs):
        done = False
        price = obs[len(obs) - 1][self.price_col_index]
        if action == 1:
            if self.balance > 0:
                fees = self.balance * self.trading_loss_pct
                self.asset_balance = (self.balance - fees)/price
                self.balance -= self.balance
        elif action == 2:
            sold = self.asset_balance * price
            self.balance = sold * (1-self.trading_loss_pct)
            self.asset_balance -= self.asset_balance

        return done

class Context:

    def act(self, action, observation):
        return (0, False)


class DummyContext(Context):

    def __init__(self):
        self.rewards = [8, 2, 3]
        self.contexts = [{"b": "blubb"}, {"b": "blabb"}, {"b": "bla"}]
        self.done = [False, True, False]
        self.current_index = 0

    def act(self, action, observation):
        done = False
        context = {}
        reward = self.rewards[self.current_index]
        context = self.contexts[self.current_index]
        done = self.done[self.current_index]
        self.current_index += 1

        return (reward, done, context)


class TradingContext(Context):

    def __init__(self, initial_fundings, trading_loss_pct):
        self.initial_fundings = initial_fundings
        self.trading_loss_pct = trading_loss_pct
        self.balance = 0
        self.asset_balance = 0

import numpy as np
import logging

from sklearn import preprocessing

HOLD = 0
BUY = 1
SELL = 2


class Context:

    def act(self, action, observation):
        return (0, False)


class TradingContext(Context):

    def __init__(self, initial_fundings,
                 trading_loss_pct, price_col_index):
        self.trading_loss_pct = trading_loss_pct
        self.initial_fundings = initial_fundings
        self.price_col_index = price_col_index
        self.reset()

    def reset(self):
        # resets all accout data
        self.balance = self.initial_fundings
        self.net_worth = self.initial_fundings
        self.max_net_worth = self.initial_fundings
        self.asset_balance = 0
        self.total_assets_sold = 0
        self.total_sales_value = 0
        self.fees = 0
        logging.info('Account resetted.')

    def _get_state(self):
        return dict(vars(self))

    def act(self, action, obs, obs_scaled):
        action_type = action[0]
        amount = action[1]

        old_state = self._get_state()
        done = self.net_worth <= 0

        # TODO consider passing attributes instead of global class attributes like current_price
        # TODO remove dependency on price_col_index -> pass current_price as method_param?
        self.current_price = obs[len(obs) - 1][self.price_col_index]
        # TODO calculate current_price by best_bid if action_type == SELL
        # TODO calculate current_price by best_ask if action_type == BUY

        self.fees = 0

        if action_type == BUY:
            self._buy(amount)
        elif action_type == SELL:
            self._sell(amount)

        # realized + unrealized PnL
        self.net_worth = self.balance + self.asset_balance * self.current_price
        if self.net_worth > self.max_net_worth:
            self.max_net_worth = self.net_worth

        if self.asset_balance == 0:
            self.cost_basis = 0

        current_state = self._get_state()

        return done, old_state, current_state

    def _buy(self, amount):
        # Buy amount % of balance in assets
        total_possible_assets = int(self.balance / self.current_price)
        assets_bought = int(total_possible_assets * amount)
        prev_cost = self.cost_basis * self.asset_balance
        additional_cost = assets_bought * self.current_price

        # only buy with sufficient balance
        if self.balance < additional_cost:
            self.balance -= additional_cost
            self.cost_basis = (
                prev_cost + additional_cost) / (self.asset_balance + assets_bought)
            self.asset_balance += assets_bought

        # TODO include fees
        # if self.balance > 0:
        #     self.fees = self.balance * self.trading_loss_pct
        #     self.asset_balance = (self.balance - self.fees)/self.price
        #     self.balance -= self.balance

    def _sell(self, amount):
        # Sell amount % of assets held
        assets_sold = int(self.asset_balance * amount)

        # only sell with sufficient assets
        if self.asset_balance < assets_sold:
            self.balance += assets_sold * self.current_price
            self.asset_balance -= assets_sold
            self.total_assets_sold += assets_sold
            self.total_sales_value += assets_sold * self.current_price

        # TODO include fees
        # if self.asset_balance > 0:
        #     sold = self.asset_balance * self.price
        #     self.fees = sold * self.trading_loss_pct
        #     self.asset_balance -= self.asset_balance
        #     self.balance = sold - self.fees

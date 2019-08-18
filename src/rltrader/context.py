import numpy as np
import logging

from sklearn import preprocessing

BUY = 'BUY'  # action_type in [0,1)
SELL = 'SELL'  # action_type in [1,2)
HOLD = 'HOLD'  # action_type in [2,3)


class Context:

    def act(self, action, observation):
        return (0, False)


class TradingContext(Context):

    def __init__(self, initial_fundings,
                 trading_loss_pct):
        self.trading_loss_pct = trading_loss_pct
        self.initial_fundings = initial_fundings

    def reset(self):
        # resets all accout data
        self.balance = self.initial_fundings
        self.net_worth = self.initial_fundings
        self.max_net_worth = self.initial_fundings
        self.asset_balance = 0
        self.total_assets_sold = 0
        self.total_sales_value = 0
        self.fees = 0

        # TODO implement MAX_OPEN_POSITIONS

        logging.info('Account resetted to %s.', self._get_state())

    def _get_state(self):
        return dict(vars(self))

    # TODO get rid of obs and obs_scaled here, because it is nothing we want to take care with here
    def act(self, action, current_price):
        action_type = action[0]
        amount = action[1]

        old_state = self._get_state()
        done = self.net_worth <= 0

        self.fees = 0

        logging.debug('current price used for next action is: %s', current_price)
        if action_type < 1:
            self._buy(amount, current_price)
        elif action_type < 2:
            self._sell(amount, current_price)

        # realized + unrealized PnL
        self.net_worth = self.balance + self.asset_balance * current_price
        if self.net_worth > self.max_net_worth:
            self.max_net_worth = self.net_worth

        # if self.asset_balance == 0:
        #     self.cost_basis = 0

        current_state = self._get_state()

        return done, old_state, current_state

    def _buy(self, amount, price):
        # Buy amount % of balance in assets
        total_possible_assets = int(self.balance / price)
        assets_bought = int(total_possible_assets * amount)
        #prev_cost = self.cost_basis * self.asset_balance
        additional_cost = assets_bought * price

        # only buy with sufficient balance
        if self.balance >= additional_cost:
            self.balance -= additional_cost
            # self.cost_basis = (
            #    prev_cost + additional_cost) / (self.asset_balance + assets_bought)
            self.asset_balance += assets_bought

        # TODO include fees
        # if self.balance > 0:
        #     self.fees = self.balance * self.trading_loss_pct
        #     self.asset_balance = (self.balance - self.fees)/self.price
        #     self.balance -= self.balance

    def _sell(self, amount, price):
        # Sell amount % of assets held
        assets_sold = int(self.asset_balance * amount)

        # only sell with sufficient assets
        if self.asset_balance >= assets_sold:
            self.balance += assets_sold * price
            self.asset_balance -= assets_sold
            self.total_assets_sold += assets_sold
            self.total_sales_value += assets_sold * price

        # TODO include fees
        # if self.asset_balance > 0:
        #     sold = self.asset_balance * self.price
        #     self.fees = sold * self.trading_loss_pct
        #     self.asset_balance -= self.asset_balance
        #     self.balance = sold - self.fees

    def render_action_type(self, action_type):
        if action_type < 1:
            return BUY
        elif action_type < 2:
            return SELL
        else:
            return HOLD

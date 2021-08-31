from .base import PaperBrokerBase


class PaperBroker(PaperBrokerBase):

    def __init__(self, initial_cash, commission, slippage):
        self._initial_cash = initial_cash
        self._commission = commission
        self._slippage = slippage


import numpy as np
import matplotlib.pyplot as plt
from collections import defaultdict
from .utils.vector import NumPyVector
from .utils.perf_utils import simple_perf


class SimplePaperBroker:

    def __init__(self, initial_cash, fee_rate):
        self._fee_rate = fee_rate
        self._initial_cash = initial_cash
        self._prices = defaultdict(lambda: NumPyVector())
        self._positions = defaultdict(lambda: NumPyVector())

    def hold(self, symbol, price):
        self._prices[symbol].append(price)
        if len(self._positions[symbol]) == 0 or np.isnan(self._positions[symbol][-1]):
            position = np.nan
        else:
            position = self._positions[-1]
        self._positions[symbol].append(position)

    def rebalance(self, symbol, price, position):
        self._prices[symbol].append(price)
        self._positions[symbol].append(position)

    def many_rebalance(self, batch_price, batch_position):
        # 需要计算某一时刻的亏损率，所以需要不同symbol的时间一致
        self._prices[symbol].append(price)
        self._positions[symbol].append(position)

    def buy(self):
        pass

import numpy as np
import matplotlib.pyplot as plt
from collections import defaultdict
from .utils.vector import NumPyVector
from .utils.perf_utils import simple_perf


class Broker_Sm:

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


class Broker:

    def __init__(self, initial_cash, fee_rate):
        self._fee_rate = fee_rate
        self._initial_cash = initial_cash
        self._prices = NumPyVector()
        self._positions = NumPyVector()

    def hold(self, price):
        self._prices.append(price)
        if len(self._positions) == 0 or np.isnan(self._positions[-1]):
            position = np.nan
        else:
            position = self._positions[-1]
        self._positions.append(position)

    def rebalance(self, price, position):
        self._prices.append(price)
        self._positions.append(position)

    def simple_perf(self):
        G, F, Vf, Theta = simple_perf(
            self._prices.values, self._positions, 
            self._initial_cash, self._fee_rate
        )
        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.plot(prices, 'g-', label='prices')
        tx = ax.twinx()
        tx.plot(positions, 'c-', label='positions')
        ax.legend(loc='upper left')

        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.plot(Vf, 'b-', label='Vf')
        tx = ax.twinx()
        tx.plot(F, 'r-', label='Fee')
        tx.plot(G, 'g-', label='Gross Profit')
        ax.legend(loc='upper right')

import os
import arrow
import json
import logging
import numpy as np
import matplotlib.pyplot as plt
from crypto_api.binance.utils import get_future_klines


class DataEngine:
    pass


class DataFeed:

    def forward(self):
        pass


class Profiler:

    def __init__(self, predicate, look_back, look_forward):
        # 因为涉及到分析，所以一次测一个信号
        self._predicate = predicate
        self._buffer = Deque(look_back + look_forward + 1)
        self._events = []

    def on_data(self, data, meta):
        self._buffer[symbol].push(data)
        rv = False
        if self._predicate.is_triggered(data):
            self._events.append(self._buffer[symbol][:])
            rv = True
        return rv

    def run(self, feed):
        self.ensure_data()
        self.init()
        for i, item in enumerate(self._data):
            meta.feed_id
            meta.data_id
            meta.event_type = 'xxx'
            meta.client_dt
            # dt 应该是client时间，回测时用
            data, meta = self.feed.forward()
        self.finalize()


# class Strat_EbnDkvSs_Base
class EbnDkvSs_StrategyBase:
    '''
    EbnDkvSs
    '''
    def __init__(self, symbol, interval, start_dt, end_dt):
        self._symbol = symbol
        self._interval = interval
        self._start_dt = arrow.get(start_dt)
        self._end_dt = arrow.get(end_dt)
        self._cache_file = (f'{symbol}_{interval}_{int(self._start_dt.timestamp())}'
                            f'_{int(self._end_dt.timestamp())}.json')

    def ensure_data(self):
        if not os.path.exists(self._cache_file):
            logging.info('Downloading data ...')
            self._data = self._download_data()
            logging.info(f'Save to cache file `{self._cache_file}`...')
            with open(self._cache_file, 'w') as f:
                json.dump(self._data, f)
        else:
            logging.info(f'Loading from cache file `{self._cache_file}`...')
            with open(self._cache_file) as f:
                self._data = json.load(f)

    def _download_data(self):
        '''
                [
          [
            1499040000000,      // Open time
            "0.01634790",       // Open
            "0.80000000",       // High
            "0.01575800",       // Low
            "0.01577100",       // Close
            "148976.11427815",  // Volume
            1499644799999,      // Close time
            "2434.19055334",    // Quote asset volume
            308,                // Number of trades
            "1756.87402397",    // Taker buy base asset volume
            "28.46694368",      // Taker buy quote asset volume
            "17928899.62484339" // Ignore.
          ]
        ]
        '''
        startTime = self._start_dt.float_timestamp * 1000
        endTime = self._end_dt.float_timestamp * 1000
        chunk_size = 1500
        data = get_future_klines(self._symbol, self._interval, startTime, endTime, 
                                 chunk_size=chunk_size, fetch_interval=0.2)
        if self._interval == '1m':
            assert (endTime - startTime)/1000//60 + 1 == len(data)
        # [1627862400000, '39846.78', '39915.95', '39750.49', '39808.00', '1468.687', 1627862459999, '58498282.26446', 11622, '679.566', '27076194.17723', '0']
        keys = ['open_time', 'open', 'high', 'low', 'close', 'volume',
                'close_time', 'volume_quote', 'num_trades', 
                'volume_base_buy', 'volume_quote_buy', 'ignored']
        data = [dict(zip(keys, item)) for item in data]
        for item in data:
            for key in keys:
                if key in ['open_time', 'close_time']:
                    continue
                item[key] = float(item[key])
        return data

    def entry(self, entry_id, symbol, side, qty, when, group, ):
        current_position_size
        if when:
            self._broker.buy(self.price, qty)

    def run(self):
        self.ensure_data()
        self.init()
        for i, item in enumerate(self._data):
            self.on_data(item)
        self.finalize()

    def init(self):
        pass

    def on_data(self, item):
        raise NotImplementedError()

    def finalize(self):
        pass


class Demo(StrategyBase):

    def init(self):
        pass

    def on_data(self, item):
        # {'open_time': 1627862400000, 'open': 39846.78, 'high': 39915.95, 'low': 39750.49, 'close': 39808.0, 
        # 'volume': 1468.687, 'close_time': 1627862459999, 'volume_quote': 58498282.26446, 'num_trades': 11622.0, 
        # 'volume_base_buy': 679.566, 'volume_quote_buy': 27076194.17723, 'ignored': 0.0}
        print(item)

    def finalize(self):
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


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, format='[%(asctime)s][%(levelname)s]: %(message)s')
    config = {'symbol': 'BTCUSDT', 
              'interval': '1m', 
              'start_dt': '2021-08-01',
              'end_dt': '2021-08-02'
             }
    strat = Demo(**config)
    strat.run()

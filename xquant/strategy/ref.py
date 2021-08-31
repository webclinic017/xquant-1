


class Strategy_MaDpLrSs:

    FEED_TYPE = 'MaDkLrSs'
    def on_data(self, item):
        '''open, high, low, close
        '''
        self.broker.current_position
        self.broker.record(symbol, item['close'])
        self.broker.rebalance(symbol, item['close'])


class Strategy_MaDpLrSs(Strategy_MaDpLrSs):

    FEED_TYPE = 'MaDkLrSs'
    def __init__(self, symbol):
        self._symbol = symbol

    def init(self):
        pass

    def on_data(self, data):
        '''{'btc': {open, high, low, close
        '''
        if self._symbol not data:
            continue

        if_then_else(ShortLong_Ma_CrossUp, then=self.go_long)
        if_then_else(ShortLong_Ma_CrossDown, then=self.go_short)

    def go_long(self):
        pass

    def go_short(self):
        pass
        item = data[self._symbol]
        self.broker.current_position
        self.broker.record(symbol, item['close'])
        self.broker.rebalance(symbol, item['close'])




class BarProfiler:
    '''
    要求固定的时间间隔，含有价格
    如果是Orderbook则不适合

    设计思路: 允许可以测试多个feed
    某个事件在某个symbol上发生后
    该symbol [-look_back, +look_forward] 上的走势表现
    '''

    def __init__(self, predicate, look_back, look_forward):
        # 因为涉及到分析，所以一次测一个信号
        # 要求feed为同一个类型的数据
        # 如果feed的时间间隔不一样呢？　
        # look_back/look_forward不就不在一个时间长度上了吗，比如一个月kline，一个日kline
        self._predicate = predicate
        self._buffer = Deque(look_back + look_forward + 1)
        self._events = []

    def on_data(self, data, meta):
        '''
        '''
        for symbol, item in data.items():
            self._buffer[symbol].push(item)
            rv = False
            if self._predicate.is_triggered(symbol, **item):
                self._events.append(self._buffer[symbol][:])
                rv = True
        return rv

    def run(self, feed):
        self._dispatcher = Dispatcher()
        try:
            feed.ev_data.connect(self.on_data)
            self._dispatcher.add_subject(feed)
            self._dispatcher.run()
        finally:
            feed.ev_data.disconnect(self.on_data)

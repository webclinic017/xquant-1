

class StrategyEngine:

    def __init__(self, feed, broker):
        self._feed = feed
        self._broker = broker
        self.tracedict = {}

    def set_params(self, params):
        self._params = params

    def update_params(self, key, value):
        self._params[key] = value

    def init(self):
        pass

    def on_data(self, data, meta):
        pass

    def finalize(self):
        pass

    def run(self):
        self.ensure_data()
        self.init()
        for i, item in enumerate(self._data):
            self.on_data(item)
        self.finalize()

    def dispatch(self):
        eof, dispatched = True, False
        smallest_dt = None
        for feed in self._feeds:
            if feed.has_next():
                eof = False
                dt = feed.peek_dt()
                if dt is not None:
                    smallest_dt = min(dt, smallest_dt)
        if not eof:
            self._current_dt = smallest_dt
            for feed in self._feeds:
                feed_dt = feed.peek_dt()
                if feed.has_next() and feed_dt in (self._current_dt, None):
                    # 有可能多条消息堵塞，所以应返回一个事件列表
                    # 如果事件列表，不同feed时间如何比较呢
                    # 所以还是单条时间比较好
                    # 框架主要定位还是回测、模拟、性能要求不是那么高的策略
                    # 如果性能要求过高，应单独移植到特定C++程序重新最简框架
                    dt, value = feed.forward()
                    assert feed_dt = dt
                    meta = {'client_dt': dt, 'source': feed.feed_id}
                    self.on_data(value, meta)
                    dispatched = True
        return eof, dispatched

    def run(self):
        self.init()
        try:
            for feed in self._feeds:
                feed.start()
            # 相当于开启了一个线程，此时join回陷入等待
            # for feed in self._feeds:
            #     feed.join()
            # 本质是轮询方式
            while not self.__stop:
                eof, dispatched = self.dispatch()
                if eof: 
                    self.__stop = True
                elif not dispatched:
                    # print('idle ...')
                    pass
        finally:
            self._current_dt = None
            for feed in self._feeds:
                feed.stop()
            for feed in self._feeds:
                feed.join()

        self.finish()

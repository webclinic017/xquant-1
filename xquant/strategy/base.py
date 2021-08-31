from xquant.dispatcher import Dispatcher


class KLineStrategyEngine(StrategyEngine):
    pass


class StrategyEngine(object):

    def __init__(self, feeds, brokers):
        self._feeds = feeds
        self._brokers = brokers
        self._dispatcher = Dispatcher()
        # 接收数据消息
        for feed in self._feeds:
            self._dispatcher.add_subject(feed)
            feed.ev_data.connect(self.on_feed_data)
        # 这样好接收broker的订单消息
        for broker in self._brokers:
            broker.ev_data.connect(self.on_broker_data)
            self._dispatcher.add_subject(broker)

        # self._dispatcher.ev_start.subscribe(self.on_start)
        self._dispatcher.ev_idle.subscribe(self.on_idle)

    def init(self):
        pass

    def on_idle(self):
        pass

    def run(self):
        self.init()
        self._dispatcher.run()
        self.finalize()

    def on_feed_data(self, data, meta):
        pass

    def on_broker_data(self, data, meta):
        pass

    def finalize(self):
        pass

    @property
    def brokers(self):
        return self._brokers

    @property
    def feeds(self):
        return self._feeds

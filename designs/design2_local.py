from xquant import Strategy
from xquant.exchange.huobi import LiveBroker
from xquant.exchange.binance import LiveBroker


# 基于web的，不适合本地
class DemoStrategy(Strategy):

    def on_init(self):
        self.bn_broker = BinanceBroker('xxxx', 'xxxx')
        self.ok_broker = HuobiBroker()
        self.paper_broker = SimpleBroker(matching_engine)

    def on_data(self, meta, data):
        '''
        (source='binance', event_type='feed_data', data_type='kline')
        meta:
            .source
            .event_type
            .data_type
            .client_dt
        '''

    def on_finish(self):
        pass


if __name__ == '__main__':
    feed = binance.KLineFeed()
    broker = PaperBroker(engine=KLineEngine(feed), slippage=Percent)

    from xquant.exchange import astock
    book_feed = astock.replay.BookFeed()
    book_feed = astock.live.BookFeed()

    exchange = astock.live.Exchange(['kline', 'orderbook', 'trades']) # 特定类型的Feed数据
    book_feed.subscribe('xxx:xxx')
    broker = astock.PaperBroker(engine=KLineEngine(exchange['kline']), slippage=Percent)
    broker = astock.TradeBroker('xxx', 'xxx') # 交易帐号

    from xquant.exchange import binance
    broker = binance.PaperBroker(engine=KLineEngine(feed), slippage=Percent)
    broker = binance.TradeBroker('xxxx', 'xxxxx')

    class Demo:

        def init(self):
            from xquant.exchange import binance
            # self.broker = binance.PaperBroker(engine=KLineEngine(feed), slippage=Percent)
            self.broker = binance.PaperBroker(engine_feed=self.feeds[0],
                                              engine=None, slippage=Percent)
            # self.broker = binance.TradeBroker('xxxx', 'xxxxx')

    # engine = StrategyEngine(feeds=[feed1, feed2], broker=broker)
    from xquant.exchange import astock
    from xquant.exchange.broker import SuperBroker
    from xquant.exchange.feed import SuperFeed/Exchange

    book_feed = astock.replay.BookFeed()
    if 0:
        engine = StrategyEngine(feed=[feed1, feed2])
        engine.run()
    if 1:
        engine = StrategyEngine(feed=[feed1, feed2, feed3], strategy=strategy)
        engine.run()

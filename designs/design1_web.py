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
        buy('binance:xxxx', 'btcusdt', 10, sl_price=10232.3)

    def on_finish(self):
        pass


if __name__ == '__main__':
    strat = Strategy('demo')
    strat.auth('token-xxxxxx')
    strat.subscribe('binance:kline:future_btcusdti')
    strat.run()

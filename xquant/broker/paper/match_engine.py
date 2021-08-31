from xquant.observer import Event, Subject


class MatchEngineBase(Subject):
    '''
    撮合成交引擎
    '''
    def __init__(self, feed):
        self._feed = feed
        self._ev_data = Event()
        self._feed.ev_data.connect(self.on_feed)

    def on_feed(self, data, meta):
        pass

    def on_order(self, broker, order):
        pass


class KLineMatchEngine(MatchEngineBase):

    def __init__(self, feed):
        MatchEngineBase.__init__(self, feed)
        self.current_bar = None

    def on_feed(self, data, meta):
        self.current_bar = data

    def on_order(self, broker, order):
        pass

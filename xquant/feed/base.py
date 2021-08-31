from xquant.const import FEED_PRIORITY
from xquant.observer import Event, Subject


class FeedBase(Subject):

    def __init__(self, feed_id, priority=None):
        self._feed_id = feed_id
        self._is_live = None
        self._ev_data = Event()
        if priority is None:
            priority = FEED_PRIORITY
        Subject.__init__(self, priority)

    def start(self):
        raise NotImplementedError()

    def stop(self):
        raise NotImplementedError()

    def join(self):
        raise NotImplementedError()

    def eof(self):
        '''是否还有event待dispatch'''
        raise NotImplementedError()

    def has_event(self):
        '''是否有event待派发
        这和eof不同，has_event表示暂时还没有事件待派发，
        但一会或不久的将来可能会有

        通过一个peek_dt意义模糊
        这样更清晰
        if has_event():
            dt = peek_dt()
        '''
        raise NotImplementedError()

    def peek_dt(self):
        '''待dispatch事件的时间
        如果为实时模式, peek_dt为 None
        '''
        raise NotImplementedError()

    def dispatch(self):
        '''如果为True，最少有一个event被dispatch'''
        raise NotImplementedError()

    @property
    def feed_id(self):
        return self._feed_id

    @property
    def is_live(self):
        return self._is_live

    @property
    def ev_data(self):
        return self._ev_data


class LiveFeedBase(FeedBase):

    def __init__(self, feed_id):
        FeedBase.__init__(self, feed_id)
        self._is_live = True

    def start(self):
        raise NotImplementedError()

    def stop(self):
        raise NotImplementedError()

    def join(self):
        raise NotImplementedError()

    def dispatch(self):
        '''如果为True，最少有一个event被dispatch'''
        raise NotImplementedError()

    def has_event(self):
        '''是否有event待派发
        '''
        raise NotImplementedError()

    def peek_dt(self):
        return None

    def eof(self):
        return False


class ReplayFeedBase(FeedBase):
    def __init__(self, feed_id):
        FeedBase.__init__(self, feed_id)
        self._is_live = False


from enum import Enum
class FeedKind(Enum):
    kinds = {
        's': 'xxx'
    }

class Feed_Ss:

    def __init__(self, symbol):
        pass

    def next(self):
        '''
        [{'price': xxx}]
        '''
        pass


class Feed_Sm:

    def __init__(self, symbol):
        pass

    def next(self):
        '''
        [{'price': xxx}]
        '''
        pass


class Feed_MaDpLrSs:

    def next(self):
        '''
        [{'price': xxx}]
        '''
        pass


class Feed_MaDkLrSs:
    FEED_KEYS = ['open', 'high', 'low', 'close']

    def next(self):
        pass


class PriceFeed:

    def next(self):
        '''
        {'price': xxx}
        '''
        pass

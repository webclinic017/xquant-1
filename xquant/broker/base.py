from xquant.const import BROKER_PRIORITY
from xquant.observer import Event, Subject


class BrokerBase(Subject):

    def __init__(self, broker_id, priority=None):
        self._broker_id = broker_id
        self._is_real = None
        self._ev_data = Event()
        if priority is None:
            priority = BROKER_PRIORITY
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
    def is_real(self):
        return self._is_real

    @property
    def ev_data(self):
        return self._ev_data

    @property
    def broker_id(self):
        return self._broker_id


class LiveBrokerBase(BrokerBase):

    def __init__(self, broker_id):
        BrokerBase.__init__(self, broker_id)
        self._is_real = True

    def start(self):
        raise NotImplementedError()

    def stop(self):
        raise NotImplementedError()

    def join(self):
        raise NotImplementedError()

    def dispatch(self):
        '''如果为True，最少有一个event被dispatch'''
        raise NotImplementedError()

    def peek_dt(self):
        return None

    def eof(self):
        return False


class PaperBrokerBase(BrokerBase):
    def __init__(self, broker_id, match_engine):
        BrokerBase.__init__(self, broker_id)
        self._is_real = False

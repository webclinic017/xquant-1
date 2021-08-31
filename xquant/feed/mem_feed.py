from .base import ReplayFeedBase


class MemFeed(ReplayFeedBase):

    def __init__(self, feed_id, source):
        FeedBase.__init__(self, feed_id)

        self.source = source
        self.is_gen = False
        if inspect.isgeneratorfunction(source):
            self.is_gen = True
        self._reset()
        self._forward()

    def _reset(self):
        if self.is_gen:
            self.generator = self.source()
        else:
            self.generator = iter(source)

        self._eof = False
        self._has_event = True
        self._next_dt = None
        self._next_value = None

    def _forward(self):
        # 实时模式下，不能提前next
        dt, value = self._next_dt, self._next_value
        try:
            rv = next(self.generator)
            try:
                self._next_dt, self._next_value = rv
            except:
                raise Exception('Both `time` and `value` required for Feed')
        except StopIteration:
            # 如果结束以后，next_dt, next_value --> (None, None)
            self._eof = True
            self._has_event = False
            self._next_dt = None
            self._next_value = None
        # meta = {'client_dt': dt, 'source': self.feed_id}
        return dt, value

    def start(self):
        self.reset()

    def stop(self):
        pass

    def join(self):
        pass

    def eof(self):
        return self._eof

    def has_event(self):
        return self._has_event

    def peek_dt(self):
        return self._next_dt

    def dispatch(self):
        dispatched = False
        if self._has_event:
            dt, value = self._forward()
            self._ev_data.emit(dt, value)
            dispatched = True
        return dispatched

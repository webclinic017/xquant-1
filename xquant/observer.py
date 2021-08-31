import abc


class Event:

    def __init__(self):
        self._handlers = []

    def connect(self, handler):
        if handler not in self._handlers:
            self._handlers.append(handler)

    def disconnect(self, handler):
        if handler in self._handlers:
            self._handlers.remove(handler)

    def emit(self, *args, **kwargs)
        for handler in self.__handlers:
            handler(*args, **kwargs)


class Subject(object):

    def __init__(self, priority=None):
        # 越小越优先 None表示最后处理
        self.priority = priority

    def start(self):
        raise NotImplementedError()

    def stop(self):
        raise NotImplementedError()

    def join(self):
        raise NotImplementedError()

    def eof(self):
        '''Subject是否结束（是否还需要监听)'''
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

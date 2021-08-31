from xquant.observer import Event


class Dispatcher(object):
    '''事件调度器
    根据事件的先后顺序依次派发事件
    如果是回测模式: peek_dt非None, 方式是：轮询各事件peek_dt的大小，选择时间最小的事件进行派发
    如果是「实时模式」: for循环轮流对每个subject的最新的事件进行派发
        如果因为Strategy中处理缓慢, 每个subject的事件都越积压越多，则系统永远无法派发最新的事件,
        (实际种可以通过比较最新时间和subject第一次到达的时间来监测这种情况)
        哪怕通过批量忽略一段事件的事件也不行
        理论上为防止: 有可能多条消息堵塞，所以应返回一个事件列表
    
    如果设计成subject返回一个事件列表，则每个subject返回的事件时间可能不同(这个对live模式无关紧要，因为这就是真实世界的情况)
    不同subject只能比较每个subject的最早的事件的时间
                    # 框架主要定位还是回测、模拟、性能要求不是那么高的策略
                    # 如果性能要求过高，应单独移植到特定C++程序重新最简框架
    '''

    def __init__(self):
        self._subjects = []
        self._should_stop = False
        self._current_dt = None
        self._ev_start = Event()
        self._ev_idle = Event()

    def run(self):
        try:
            for subject in self._subjects:
                subject.start()

            self._ev_start.emit()
            # 相当于开启了一个线程，此时join回陷入等待
            # for subject in self._subjects:
            #     subject.join()
            # 本质是轮询方式
            while not self._should_stop:
                eof, dispatched = self.dispatch()
                if eof: 
                    self._should_stop = True
                elif not dispatched:
                    # 虽然没结束，但也没有事件
                    self._ev_idle.emit()
                    # print('idle ...')
        finally:
            # self._current_dt = None 这里似乎没有必要把时间重置
            for subject in self._subjects:
                subject.stop()
            for subject in self._subjects:
                subject.join()

    def dispatch(self):
        smallest_dt = None
        eof, dispatched = True, False

        # 找到最小时间点
        for subject in self._subjects:
            if not subject.eof():
                eof = False
                dt = subject.peek_dt()
                if dt is not None and smallest_dt is not None:
                    smallest_dt = min(dt, smallest_dt)

        if not eof:
            # 更新当前时间
            self._current_dt = smallest_dt
            # 循环派发事件
            for subject in self._subjects:
                subject_dt = subject.peek_dt()
                if (not subject.eof() and subject.has_event() 
                    and subject_dt in (self._current_dt, None)):
                    # 有可能多条消息堵塞，所以应返回一个事件列表
                    # 如果事件列表，不同subject时间如何比较呢
                    # 所以还是单条时间比较好
                    # 框架主要定位还是回测、模拟、性能要求不是那么高的策略
                    # 如果性能要求过高，应单独移植到特定C++程序重新最简框架
                    dispatched = subject.dispatch() is True
        return eof, dispatched

    def add_subject(self, subject):
        if subject in self._subjects:
            return

        # 如果为None: 放在最后
        # 如果不为None
        # 放在原始序列第一个为None的前面，或第一个比subject-priority大的前面
        if subject.priority is None:
            self._subjects.append(subject)
        else:
            pos = 0
            for s in self._subjects:
                if s.priority is None or subject.priority < s.priority:
                    break
                pos += 1
            self._subjects.insert(pos, subject)
        # subject.on_dispatcher_registered(self)

    @property
    def ev_start(self):
        return self._ev_start

    @property
    def ev_idle(self):
        return self._ev_idle

from perf import Strategy, Feed
from pyta.rolling.trend import rEMA
from pyta.utils.deque import NumPyDeque as Deque
from pyta.utils.vector import NumPyVector as Vector
from collections import defaultdict


# closes, opens, highs, lows, volumes
demo = Demo()
demo.set_parameter


class Optimizer:

    def __init__(self, strategy):
        pass

    def set_meshgrid(self, meshgrid):
        self.meshgrid = meshgrid

    def optimize(self):
        list_params = []
        for params in list_params:
            self.strategy.set_params(params)
            self.strategy.run()
            value = self.strategy.object_value()
            object_values.append(value)


class Demo:

    def init(self):
        # XXXL, XXL, XL, L, M, S
        self.Os = Deque(maxlen)
        self.Hs = Deque(maxlen)
        self.Ls = Deque(maxlen)
        self.Cs = Deque(maxlen)
        self.Vs = Deque(maxlen)

        self.DD = defaultdict(lambda: Deque(maxlen))
        self.event_dict = defaultdict(lambda: Vector())
        self._ma_values_L

        self.Fd = {}
        self.Fd[self.XL] = rEMA(self.XL)
        self.Fd[self.L] = rEMA(self.L)

    def check_params(self):
        assert self.p.XL > self.p.L

    def finalize(self):
        pass

    def on_data(self, item):
        my = self
        oo = float(item['open'])
        hh = float(item['high'])
        ll = float(item['low'])
        cc = float(item['close'])
        vv = float(item['volume'])
        my.Os.push(oo)
        my.Hs.push(hh)
        my.Ls.push(ll)
        my.Cs.push(cc)
        my.Vs.push(vv)

        ma_XL = my.F[my.XL].rolling(my.Cs)
        ma_L = my.F[my.XL].rolling(my.Cs)

        # 计算信号
        my.DD['ema_LL'].push(ma_XL)
        my.DD['ema_SS'].push(my.F[my.L].rolling(my.Cs))

        buy = crossup(sma(close, 10), sma(close, 30))
        sell = crossdown(sma(close, 10), sma(close, 30))

        plot_main(buy, 'buy', '^', size, color=color.yellow)
        plot_main(sell, 'sell', '^', size, color=color.yellow)

        # 
        diff_ma_L_XL_2j = my.DD['ema_L'][-2] - my.DD['ema_XL'][-2] 
        diff_ma_L_XL_1j = my.DD['ema_L'][-1] - my.DD['ema_XL'][-1] 

        before_L_lower = diff_ma_L_XL_2j < 0
        after_L_higher  = diff_ma_L_XL_1j > 0
        before_XL_lower = diff_ma_L_XL_2j > 0
        after_XL_higher  = diff_ma_L_XL_1j < 0
        ma_upcross = before_L_lower && after_L_higher
        ma_downcross = before_XL_lower && after_XL_higher

        if_then(ma_upcross, self.go_long)
        if_then(ma_downcross, self.go_short)

        # Trace
        my.TT['ma_XL'].push(ma_XL)
        my.TT['ma_L'].push(ma_XL)

        my.event_dict['ema_upcross'].append(ema_upcross)
        my.event_dict['ema_downcross'].append(ema_downcross)

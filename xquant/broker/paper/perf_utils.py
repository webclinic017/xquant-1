import numpy as np


def simple_single_perf(prices, positions, initial_cash, fee_rate):
    '''全仓模式下
    prices: 价格
    position: 累计绝对持仓量[而非持仓占比]
    initial_cash: 初始资金
    fee_rate: 交易费率
    (leverage: 杠杆率: 暂不考虑，因为涉及到平仓变号)
    (将来可以分别多仓、空仓考虑，模拟阶段不用考虑, 假设现金足够开仓)
    '''
    assert len(prices) == len(positions)
    num = len(prices)
    # -1 时间序列
    S = [0] + list(prices)
    Q = [0] + list(positions)
    # Cash = np.zeros(num+1) # 截止到t_k 现金余额(不包含手续费)
    G = np.zeros(num+1) # 截止到t_k累计盈亏GrossProfit(不包含手续费)
    F = np.zeros(num+1) # 截止到t_k累计手续费
    Vf = np.zeros(num+1) # 截止到t_k累计价值 （现金+市值-手续费)
    Theta = np.zeros(num+1) # 截止到t_k 盈亏率(收益率): 收益/本金
    
    # 使用（J）更新，计算量更小
    for k in range(1, num+1):
        if np.isnan(S[k]) or np.isnan(Q[k-1]):
            Vf[k] = initial_cash
            continue
        g_k = (S[k] - S[k-1]) * Q[k-1]
        fee_k = abs(Q[k] - Q[k-1]) * S[k] * fee_rate
        G[k] = G[k-1] + g_k
        F[k] = F[k-1] + fee_k
        Vf[k] = initial_cash + G[k] - F[k]
        # 亏损率
        # G[k] - F[k] 为净收益
        Theta[k] = (G[k] - F[k])/initial_cash
        # print(G[k], F[k], Vf[k], Theta[k])
    return G[1:], F[1:], Vf[1:], Theta[1:]


if __name__ == '__main__':
    if 0:
        prices = [1, 1.0, 1.0]
        positions = [1, 2, 3]
        initial_cash = 100
        fee_rate = 0.005
        G, F, Vf, Theta = simple_single_perf(prices, positions, initial_cash, fee_rate)
        print('G', G)
        print('Vf', Vf)
        print('F', F)
    if 0:
        prices = [1, 1.1, 1.2]
        positions = [1, 1, 1]
        initial_cash = 100
        fee_rate = 0.000
        G, F, Vf, Theta = simple_single_perf(prices, positions, initial_cash, fee_rate)
        print('G', G)
        print(G[1], type(G[1]))
        print(type(0.1))
        assert G[0] == 0
        assert G[1] == 0.1
        assert G[2] == 0.2
        print('Vf', Vf)
        print('F', F)
    if 1:
        import matplotlib.pyplot as plt
        # prices = [1, 1, 1, 1, 1.0]
        # prices = np.random.rand(5)
        # positions = [0, 0, 0, 0, 0]
        # positions = np.random.rand(5)
        if 0:
            prices = [1, 1.1, 1.2, 1.2, 1.3, 1.3999]
            positions = [0, 0.1, 0.2, 0.3, 0.3, 0.5]
        if 1:
            prices = [1, 1.1, 1.2, 1.2, 1.3, 1.3999, 1.0]
            positions = [1]*len(prices)
        print('position', positions)
        initial_cash = 100
        fee_rate = 0.005
        G, F, Vf, Theta = simple_single_perf(prices, positions, initial_cash, fee_rate)

        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.plot(prices, 'g-', label='prices')
        tx = ax.twinx()
        tx.plot(positions, 'c-', label='positions')
        ax.legend(loc='upper left')

        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.plot(Vf, 'b-', label='Vf')
        tx = ax.twinx()
        tx.plot(F, 'r-', label='Fee')
        tx.plot(G, 'g-', label='Gross Profit')
        ax.legend(loc='upper right')
        plt.show()

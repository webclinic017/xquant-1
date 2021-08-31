# xquant
cross market backtesting/live-trading quant framework （developing)
(定位：处理股票，数字货币交易为主的事件系统)

based on [pyalgotrade](http://gbeced.github.io/pyalgotrade/)

## Design-Objective 设计要求
 - [ ] good-designed interface 接口简单，易于使用
 - [ ] cross-market 支持跨市场获得行情数据，支持跨市场交易
 - [ ] extendable 低耦合性, 可拓展，可以针对特定市场定制
 - [ ] event-backtest 支持事件回测
 - [ ] plot 方便的绘图展示程序
 - [ ] **AI-friendly** strategy paramterized 策略参数化


# 设计
## 对象模型
### 核心对象
	* Feed (单数据类型Stream) LiveFeed/ReplayStream 单个Feed只能发出数据，数据可以被Strategy订阅		(dt, dtype, [{'symbol': '000063.SH', 'open': 15.36}])
	* Stream /LiveStream/ReplayStream 单个Stream可以发出多种数据，数据可以被Strategy订阅 (dt, dtype, [{'symbol': '000063.SH', 'open': 15.36}])
	* Strategy 数据来源于Feed/Stream，策略依赖于数据来源
	* Broker 提供交易接口
	* Analyzer 分析Broker结果
	* Profiler 对单个Feed的指标/因子进行测试

### 辅助对象
	* Dispatcher
	* Sequence

# 思考
	因为需要处理orderbook数据，理论上，对性能要求高，最终xquant可能还是需要用C/Cython写一部分

## Reference
	* pyalgotrade

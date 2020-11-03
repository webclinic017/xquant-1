# 设计

## 辅助库
	* pyta indicator 技术指标库
	* kappa kline pattern recognization 模式识别库

## 对象模型
### 核心对象
	* Feed (单数据类型Stream) LiveFeed/ReplayStream 单个Feed只能发出数据，数据可以被Strategy订阅		(dt, dtype, [{'symbol': '000063.SH', 'open': 15.36}])
	* Stream /LiveStream/ReplayStream 单个Stream可以发出多种数据，数据可以被Strategy订阅 (dt, dtype, [{'symbol': '000063.SH', 'open': 15.36}])
	* Strategy 数据来源于Feed/Stream，策略依赖于数据类型
	* Broker 提供交易接口, PaperBroker, LiveBroker
	* Analyzer 分析Broker结果
	* Profiler 对单个Feed的指标/因子进行测试
	* Flow
### Strategy

```py

Flow(_if = golden_cross, _then = BuyOrder(10), _else = Null).execute()
```
### 辅助对象
	* Dispatcher
	* Sequence

# 思考
	因为需要处理orderbook数据，理论上，对性能要求高，最终xquant可能还是需要用C/Cython写一部分

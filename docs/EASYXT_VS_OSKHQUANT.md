# EasyXT vs OSkhQuant

> 对照本机仓库 `EasyXT` 与 `OSkhQuant`（看海量化 KHQuant **V2.1.4 开源版**）。
> 日期：2026-08-16。评分与结论以本地源码为准，不以宣传文案为准。

## 结论

成熟度不在同一条轴上。

- **OSkhQuant** 更像成品回测软件：统一策略回调、GUI、成本模型和报告更完整。
- **EasyXT** 更像模块化工具箱：实盘、多数据源、因子研究和大 QMT 本地读数更完整。
- 以本机「大 QMT + 实盘」为准，**EasyXT 更可用**。
- 以「开箱即用的可视化回测」为准，**OSkhQuant 更成熟**。

对本机栈的建议：继续以 EasyXT 为主系统。值得从 OSkhQuant 借的是策略回调契约、交易成本模型和回测报告交互，而不是整体迁移。MiniQMT 回测 GUI 会和当前大 QMT / DuckDB 路线冲突。

看海官网另有 VIP 闭源 V3.3（CLI、DuckDB、AI 策略），不在本对照范围内。

---

## 定位

| 维度 | EasyXT | OSkhQuant |
|------|--------|-----------|
| 是什么 | 模块化 QMT 工具集，不是单一框架 | PyQt5 桌面回测产品，可打包 exe |
| 公开版本 | 1.0.0 | 2.1.4（开源） |
| 许可 | MIT | CC BY-NC 4.0（禁止商用） |
| 核心依赖 | 本机已走**大 QMT** `datadir` | **MiniQMT** `userdata_mini` |
| Python 文件 | 约 410 | 约 22 |
| 代码行 | 约 13.7 万 | 约 3.4 万 |
| GitHub stars（2026-08 公开页） | 约 583 | 1,448 |

代码量统计排除 `.git` / `bak` / `Raw_Data` / `__pycache__`。

---

## 分项成熟度（1–10）

| 维度 | EasyXT | OSkhQuant |
|------|--------|-----------|
| 回测产品体验 | 6 | **9** |
| 实盘交易 | **8** | 2 |
| 数据层 | **8** | 6 |
| 策略接口统一 | 5 | **8** |
| 架构可维护性 | 5 | 5 |
| 因子分析 | **8** | 3 |
| 文档与上手 | 6 | **9** |
| 本机大 QMT 契合 | **9** | 2 |

---

## 功能对照

| 能力 | EasyXT | OSkhQuant | 更成熟的一方 |
|------|--------|-----------|--------------|
| 产品形态 | 模块化工具集：API / 回测库 / GUI 插件 / 因子 Web | 单一桌面产品：PyQt5 回测平台 + 打包 exe | 看场景 |
| 策略接口 | 各策略自管生命周期，无统一回调规范 | `init` / `khPreMarket` / `khHandlebar` / `khPostMarket` | OSkhQuant |
| 回测引擎 | 股票增强引擎 + CB/ETF 向量化；佣金滑点有，A 股规则散落 | 事件驱动回放；佣金/印花税/流量费/滑点/T+1 一体 | OSkhQuant |
| 回测报告 | 库级 summary + Streamlit；GUI 不如成品软件 | 净值/回撤/买卖点/交易流水/月度热力图 | OSkhQuant |
| 实盘交易 | `easy_xt` 真下单、撤单、查仓；雪球跟单/网格/条件单 | 官方明确不做实盘；`_place_order_live` 仅 print | EasyXT |
| 行情通道 | 大 QMT 本地 `.DAT` + Tushare/DuckDB/TDX/东财降级 | 只吃 MiniQMT `xtquant`（`download_history_data`） | EasyXT |
| 因子分析 | Alpha101/191、IC/IR、分层回测、Streamlit 平台 | 策略里用 MyTT 指标，无因子研究栈 | EasyXT |
| 数据管理 GUI | Tushare 下载、DuckDB、本地 DAT 管理器 | 数据补充/CSV 下载/清洗/可视化，围绕 MiniQMT | OSkhQuant（产品化） |
| 风控 | 策略内各自实现（跟单有仓位限制） | `khRisk.py` 三个检查全部 `return True` | EasyXT（至少有真实检查） |
| 跨平台 | Windows 原生；Mac/Linux 走 xqshare | 开源版仅 Windows + MiniQMT | EasyXT |
| 测试 | 4 个 `unit_tests`，覆盖很薄 | 无独立测试文件 | 两者都弱 |

OSkhQuant 官方写明当前版本不做实盘。源码里 `_place_order_live` 只 `print`。

---

## 架构对照

### EasyXT：分层工具箱

文档自称三层、单向依赖：应用层 → 核心层 → 基础层。

- 应用：`strategies/`、`gui_app/`、101 因子平台
- 核心：`config`、`data_manager`、`alpha_analysis`、`qmt_local_reader`
- 基础：`easy_xt` 封装 xtquant；DuckDB / Tushare 作数据底座

实际问题：模块边界松、路径插入多、GUI 是学习平台加插件而不是单一工作流。本机已把 miniQMT 路径关掉，行情走大 QMT `datadir`。

### OSkhQuant：单体产品

概念上是 GUI / 框架 / 交易 / 数据分离，策略高内聚。

- GUI：`GUIkhQuant.py` 约 4851 行，主窗口即控制器
- 引擎：`khFrame.py` 事件循环 + Tick / K 线 / 自定义时间触发器
- 交易：`khTrade` 模拟撮合；`khRisk` 仍是空壳

实际问题：几个 3000–4800 行上帝文件；实盘/模拟分支未接通；强绑 MiniQMT `userdata_mini`，和本机大 QMT 栈冲突。

### 策略驱动模型

OSkhQuant 把策略写成「填四个回调、返回信号字典」，框架负责回放、撮合、记账和报告。

EasyXT 把 `easy_xt` 当 SDK：循环、调度和下单由策略自己写。回测是另一套类（`EnhancedBacktestEngine` / `VectorizedBacktestEngine`），和实盘脚本并不共用同一套回调。

因此：写一条 MACD 策略并看报告，OSkhQuant 更省事；把跟单/网格/因子接到银河大 QMT 实盘，EasyXT 已经有通路，OSkhQuant 开源版走不通。

---

## 按用途选

| 你要做的事 | 更合适 | 原因 |
|------------|--------|------|
| 可视化回测、调成本参数、看资金曲线 | OSkhQuant | 成品 GUI、`.kh` 工程文件、报告窗口完整 |
| 本机大 QMT 读 `.DAT` / 补数据 / 真下单 | EasyXT | 已对接银河大 QMT；OSkhQuant 绑 MiniQMT |
| 因子挖掘、IC、分层、DuckDB 研究 | EasyXT | 101 因子平台 + `easyxt_backtest` 因子栈 |
| 雪球跟单、网格、通达信预警、条件单 | EasyXT | `strategies/` 下有可运行实现 |
| 给不会写框架的人一个统一策略模板 | OSkhQuant | 回调契约清晰，文档到第十二章 |

---

## 两边共同的短板

- 自动化测试几乎没有
- 单人维护，社区贡献有限
- 文档与代码有漂移
- 都不是机构级 OMS

文档漂移示例：

- EasyXT 架构/README 仍写「已支持 miniQMT」，本机规则已禁用 miniQMT。
- OSkhQuant 文档写「回测/模拟/实盘无缝切换」，源码里 live 分支是空实现。

---

## 相关路径

- EasyXT：`D:\Git\SideWork\EasyXT`
- OSkhQuant：`D:\Git\SideWork\OSkhQuant`
- EasyXT 架构：[`ARCHITECTURE.md`](ARCHITECTURE.md)
- EasyXT 本机 QMT 约定：仓库根 `.cursor/rules/qmt-easyxt.mdc`

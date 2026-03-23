# 端到端集成实现计划

## 目标
完成 Phase 5 剩余任务：端到端测试 + CLI 接口 + 持久化层

## 当前状态
✅ Phase 0-4 完成（20 tests 全绿）
✅ ReportAssembler + ConsistencyChecker 完成

## 待实现

### 1. 端到端测试（优先级：高）
**目标**：输入公司名 → 完整 8 章节报告

**实现步骤**：
- 创建 `tests/integration/test_e2e.py`
- Mock 所有外部依赖（LLM、API）
- 测试完整 DAG 流程：数据层 → 分析层 → 判断层 → 组装层
- 验证报告结构完整性

### 2. CLI 用户接口（优先级：中）
**目标**：`python -m src.cli research <公司名>`

**实现步骤**：
- 创建 `src/cli.py`
- 参数解析：公司名、输出路径
- 调用 Orchestrator 执行完整流程
- 输出报告到 Markdown 文件

### 3. 持久化层（优先级：低，可选）
**目标**：保存调研历史和公司关系图

**实现步骤**：
- 创建 `src/state/persistence.py`
- 保存 Report 到 JSON
- NetworkX 图序列化（`nx.node_link_data`）
- 失败处理：记录日志，不中断流程

## 验收标准
- [ ] 端到端测试通过
- [ ] CLI 可执行并输出报告
- [ ] 全量测试保持全绿

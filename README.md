# 多Agent协作投资调研系统

基于辩论协议的上市公司调研与投资决策系统。

## 核心特性

- **辩论协议**：多空质疑三方独立论证 + 仲裁合成
- **分层架构**：数据层 → 分析层 → 判断层 → 组装层
- **认知积累**：持仓、偏好、历史判断、公司关系网络

## 快速开始

```bash
# 安装依赖
pip install -r requirements.txt

# 运行调研
python -m src.cli research <股票代码>
```

## 架构

详见设计文档：`~/.gstack/projects/Work/Administrator-unknown-design-20260323-094240.md`

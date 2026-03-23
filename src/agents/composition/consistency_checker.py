from src.agents.base.base_agent import BaseAgent
from src.schemas import Report


class ConsistencyChecker(BaseAgent):
    """一致性校验器"""

    uses_external_data = False

    async def execute(self, input_data: dict) -> list[str]:
        """校验报告一致性，返回警告列表"""
        report: Report = input_data["report"]
        warnings = []

        # 跨轮一致性检查
        if "严重" in report.ch4_risk and "买入" in report.ch7_position:
            if "矛盾" not in report.ch7_position.lower():
                warnings.append("Ch4判定严重风险，但Ch7建议买入，未见显式回应")

        if "不可信" in report.ch6_leader and "买入" in report.ch7_position:
            if "矛盾" not in report.ch7_position.lower():
                warnings.append("Ch6判定不可信，但Ch7建议买入，未见显式回应")

        return warnings

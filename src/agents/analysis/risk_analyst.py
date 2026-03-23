from typing import Any
from ..base.base_agent import BaseAgent
from ...schemas.analysis import RiskAnalysis


class RiskAnalyst(BaseAgent):
    """风险分析 Agent → Ch4"""

    async def execute(self, input_data: dict[str, Any]) -> dict[str, Any]:
        search_output = input_data["search_output"]
        financial_data = input_data["financial_data"]

        analysis = RiskAnalysis(
            risk_matrix="风险清单与评估矩阵（基于财务数据和行业信息）",
        )

        return {"risk_analysis": analysis}

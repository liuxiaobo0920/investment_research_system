from typing import Any
from ..base.base_agent import BaseAgent
from ...schemas.analysis import MoatAnalysis


class MoatAnalyst(BaseAgent):
    """护城河分析 Agent → Ch3"""

    async def execute(self, input_data: dict[str, Any]) -> dict[str, Any]:
        search_output = input_data["search_output"]
        financial_data = input_data["financial_data"]

        analysis = MoatAnalysis(
            core_advantages=f"核心优势分析（ROE均值：{sum(m.value for m in financial_data.roe)/len(financial_data.roe):.2%}）",
            moat_assessment="护城河评估：十年护城河判断",
        )

        return {"moat_analysis": analysis}

from typing import Any
from ..base.base_agent import BaseAgent
from ...schemas.data import WebSearchOutput


class WebSearchAgent(BaseAgent):
    """网页搜索 Agent"""
    uses_external_data = True

    async def execute(self, input_data: dict[str, Any]) -> dict[str, Any]:
        company_name = input_data["company_name"]
        keywords = input_data.get("keywords", [])

        # TODO: 集成 Serper/Tavily 搜索API
        # 一期使用 mock 数据
        search_output = WebSearchOutput(
            company_name=company_name,
            industry_reports=[
                f"{company_name}所在行业2023年度报告摘要",
                f"{company_name}行业竞争格局分析",
            ],
            news_summary=[
                f"{company_name}最新产品发布",
                f"{company_name}Q3财报解读",
            ],
            policy_summary=[
                "行业相关政策支持",
                "监管环境变化",
            ],
        )

        return {"search_output": search_output}

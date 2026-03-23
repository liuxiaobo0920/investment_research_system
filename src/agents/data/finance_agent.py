from typing import Any
from ..base.base_agent import BaseAgent
from ...schemas.data import FinancialData, AnnualMetric


class FinanceAgent(BaseAgent):
    """金融数据采集 Agent"""
    uses_external_data = True

    async def execute(self, input_data: dict[str, Any]) -> dict[str, Any]:
        company_code = input_data["company_code"]
        company_name = input_data.get("company_name", "")

        # TODO: 集成真实金融API (AkShare/Tushare)
        # 一期使用 mock 数据
        financial_data = FinancialData(
            company_code=company_code,
            company_name=company_name,
            revenue=[
                AnnualMetric(year="2023", value=100000.0),
                AnnualMetric(year="2022", value=90000.0),
                AnnualMetric(year="2021", value=80000.0),
            ],
            net_profit=[
                AnnualMetric(year="2023", value=10000.0),
                AnnualMetric(year="2022", value=9000.0),
                AnnualMetric(year="2021", value=8000.0),
            ],
            cash_flow=[
                AnnualMetric(year="2023", value=12000.0),
                AnnualMetric(year="2022", value=11000.0),
                AnnualMetric(year="2021", value=10000.0),
            ],
            roe=[
                AnnualMetric(year="2023", value=0.15),
                AnnualMetric(year="2022", value=0.14),
                AnnualMetric(year="2021", value=0.13),
            ],
            roic=[
                AnnualMetric(year="2023", value=0.12),
                AnnualMetric(year="2022", value=0.11),
                AnnualMetric(year="2021", value=0.10),
            ],
        )

        return {"financial_data": financial_data}

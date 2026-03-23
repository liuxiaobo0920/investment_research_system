from typing import Any
from ..base.base_agent import BaseAgent
from ...schemas.data import LeaderData


class LeaderAgent(BaseAgent):
    """董事长信息采集 Agent"""
    uses_external_data = True

    async def execute(self, input_data: dict[str, Any]) -> dict[str, Any]:
        leader_name = input_data["leader_name"]
        company_name = input_data["company_name"]

        # TODO: 集成搜索API获取董事长信息
        # 一期使用 mock 数据
        leader_data = LeaderData(
            leader_name=leader_name,
            company_name=company_name,
            speeches=[
                f"{leader_name}在年度股东大会的发言",
                f"{leader_name}谈公司战略规划",
            ],
            interviews=[
                f"{leader_name}接受财经媒体专访",
            ],
            career_history=f"{leader_name}职业履历：历任多家企业高管",
            controversies=[],
        )

        return {"leader_data": leader_data}

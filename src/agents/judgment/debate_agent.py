from typing import Any, Literal
from ..base.base_agent import BaseAgent


class DebateAgent(BaseAgent):
    """辩论 Agent - 单类设计，通过 role 参数区分行为"""

    def __init__(self, agent_id: str, role: Literal["bull", "bear", "challenger", "arbitrator"]):
        super().__init__(agent_id)
        self.role = role

    async def execute(self, input_data: dict[str, Any]) -> dict[str, Any]:
        round_id = input_data["round_id"]
        topics = input_data["topics"]
        context = input_data.get("context", {})

        # TODO: 调用 LLM 生成论证
        if self.role == "arbitrator":
            output = f"仲裁结论（Round {round_id}，topics: {topics}）"
        else:
            output = f"{self.role.upper()} 论证（Round {round_id}，topics: {topics}）"

        return {
            "role": self.role,
            "round_id": round_id,
            "output_text": output,
            "paragraph_ids": [f"r{round_id}_{self.role}_1"],
        }

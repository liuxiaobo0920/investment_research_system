from typing import Any
from ..base.base_agent import BaseAgent
from .debate_agent import DebateAgent
from ...schemas.debate import RiskTrustJudgment, InvestmentJudgment


class DebateCoordinator(BaseAgent):
    """协调辩论流程"""

    async def execute(self, input_data: dict[str, Any]) -> dict[str, Any]:
        round_id = input_data["round_id"]
        topics = input_data["topics"]
        context = input_data.get("context", {})

        # Step 1: 并行执行 bull/bear/challenger
        roles = ["bull", "bear", "challenger"]
        arguments = []

        for role in roles:
            agent = DebateAgent(f"{role}_{round_id}", role)
            result = await agent.execute({
                "round_id": round_id,
                "topics": topics,
                "context": context,
            })
            arguments.append(result)

        # Step 2: 仲裁合成
        arbitrator = DebateAgent(f"arbitrator_{round_id}", "arbitrator")
        arbitrator_result = await arbitrator.execute({
            "round_id": round_id,
            "topics": topics,
            "context": {"arguments": arguments},
        })

        if round_id == 1:
            judgment = RiskTrustJudgment(
                risk_verdict="可控",
                risk_reasoning="风险评估推理",
                trust_verdict="值得信任",
                trust_reasoning="信任评估推理",
                evidence_references=[],
            )
            return {"round1_judgment": judgment}
        else:
            judgment = InvestmentJudgment(
                decision="买入",
                confidence=0.8,
                risk_trust_input=context.get("round1_judgment"),
                bull_case="多头论证",
                bear_case="空头论证",
                key_factors=["因素1", "因素2"],
                evidence_references=[],
                position_suggestion="建仓建议",
            )
            return {"round2_judgment": judgment}

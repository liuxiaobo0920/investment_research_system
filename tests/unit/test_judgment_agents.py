import pytest
from src.agents.judgment import DebateAgent, DebateCoordinator
from src.schemas.debate import RiskTrustJudgment, InvestmentJudgment


@pytest.mark.asyncio
async def test_debate_agent_bull():
    agent = DebateAgent("bull_test", "bull")
    result = await agent.execute({
        "round_id": 1,
        "topics": ["risk", "trust"],
        "context": {},
    })

    assert result["role"] == "bull"
    assert result["round_id"] == 1
    assert "output_text" in result


@pytest.mark.asyncio
async def test_debate_agent_arbitrator():
    agent = DebateAgent("arbitrator_test", "arbitrator")
    result = await agent.execute({
        "round_id": 2,
        "topics": ["investment"],
        "context": {},
    })

    assert result["role"] == "arbitrator"
    assert result["round_id"] == 2


@pytest.mark.asyncio
async def test_debate_coordinator_round1():
    coordinator = DebateCoordinator("coordinator_test")
    result = await coordinator.execute({
        "round_id": 1,
        "topics": ["risk", "trust"],
        "context": {},
    })

    assert "round1_judgment" in result
    assert isinstance(result["round1_judgment"], RiskTrustJudgment)


@pytest.mark.asyncio
async def test_debate_coordinator_round2():
    round1_judgment = RiskTrustJudgment(
        risk_verdict="可控",
        risk_reasoning="测试",
        trust_verdict="值得信任",
        trust_reasoning="测试",
        evidence_references=[],
    )

    coordinator = DebateCoordinator("coordinator_test")
    result = await coordinator.execute({
        "round_id": 2,
        "topics": ["investment", "position"],
        "context": {"round1_judgment": round1_judgment},
    })

    assert "round2_judgment" in result
    assert isinstance(result["round2_judgment"], InvestmentJudgment)

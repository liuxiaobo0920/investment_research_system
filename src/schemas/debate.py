from dataclasses import dataclass
from typing import Literal


@dataclass
class EvidenceRef:
    agent_id: str
    round_id: int
    paragraph_id: str
    quote: str


@dataclass
class RiskTrustJudgment:
    """Round 1 产出"""
    risk_verdict: Literal["可控", "需关注", "严重"]
    risk_reasoning: str
    trust_verdict: Literal["值得信任", "有疑虑", "不可信"]
    trust_reasoning: str
    evidence_references: list[EvidenceRef]


@dataclass
class InvestmentJudgment:
    """Round 2 产出"""
    decision: Literal["买入", "观望", "回避"]
    confidence: float
    risk_trust_input: RiskTrustJudgment
    bull_case: str
    bear_case: str
    key_factors: list[str]
    evidence_references: list[EvidenceRef]
    position_suggestion: str


@dataclass
class DebateEvent:
    debate_id: str
    round_id: int
    role: str
    timestamp: str
    input_summary: str
    output_text: str
    paragraph_ids: list[str]
    token_usage: int
    model: str

from dataclasses import dataclass


@dataclass
class IndustryAnalysis:
    policy_environment: str
    industry_cycle: str
    supply_demand: str
    competitive_landscape: str


@dataclass
class MoatAnalysis:
    core_advantages: str
    moat_assessment: str


@dataclass
class RiskAnalysis:
    risk_matrix: str


@dataclass
class FinanceAnalysis:
    revenue_growth: str
    profitability: str
    cash_flow: str


@dataclass
class LeaderAnalysis:
    leadership_profile: str

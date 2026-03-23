from dataclasses import dataclass
from typing import Literal


@dataclass
class AnnualMetric:
    year: str
    value: float


@dataclass
class FinancialData:
    """财务数据结构体"""
    company_code: str
    company_name: str
    revenue: list[AnnualMetric]
    net_profit: list[AnnualMetric]
    cash_flow: list[AnnualMetric]
    roe: list[AnnualMetric]
    roic: list[AnnualMetric]


@dataclass
class WebSearchOutput:
    """网页搜索输出"""
    company_name: str
    industry_reports: list[str]
    news_summary: list[str]
    policy_summary: list[str]


@dataclass
class LeaderData:
    """董事长信息"""
    leader_name: str
    company_name: str
    speeches: list[str]
    interviews: list[str]
    career_history: str
    controversies: list[str]

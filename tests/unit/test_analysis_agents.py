import pytest
from src.agents.analysis import (
    IndustryAnalyst,
    MoatAnalyst,
    RiskAnalyst,
    FinanceAnalyst,
    LeaderAnalyst,
)
from src.schemas.data import FinancialData, WebSearchOutput, LeaderData, AnnualMetric
from src.schemas.analysis import (
    IndustryAnalysis,
    MoatAnalysis,
    RiskAnalysis,
    FinanceAnalysis,
    LeaderAnalysis,
)


@pytest.fixture
def financial_data():
    return FinancialData(
        company_code="600519",
        company_name="贵州茅台",
        revenue=[AnnualMetric(year="2023", value=100000.0)],
        net_profit=[AnnualMetric(year="2023", value=10000.0)],
        cash_flow=[AnnualMetric(year="2023", value=12000.0)],
        roe=[AnnualMetric(year="2023", value=0.15)],
        roic=[AnnualMetric(year="2023", value=0.12)],
    )


@pytest.fixture
def search_output():
    return WebSearchOutput(
        company_name="贵州茅台",
        industry_reports=["行业报告1"],
        news_summary=["新闻1"],
        policy_summary=["政策1"],
    )


@pytest.fixture
def leader_data():
    return LeaderData(
        leader_name="丁雄军",
        company_name="贵州茅台",
        speeches=["演讲1"],
        interviews=["访谈1"],
        career_history="履历",
        controversies=[],
    )


@pytest.mark.asyncio
async def test_industry_analyst(search_output):
    agent = IndustryAnalyst("industry_test")
    result = await agent.execute({"search_output": search_output})

    assert "industry_analysis" in result
    assert isinstance(result["industry_analysis"], IndustryAnalysis)


@pytest.mark.asyncio
async def test_moat_analyst(search_output, financial_data):
    agent = MoatAnalyst("moat_test")
    result = await agent.execute({"search_output": search_output, "financial_data": financial_data})

    assert "moat_analysis" in result
    assert isinstance(result["moat_analysis"], MoatAnalysis)


@pytest.mark.asyncio
async def test_risk_analyst(search_output, financial_data):
    agent = RiskAnalyst("risk_test")
    result = await agent.execute({"search_output": search_output, "financial_data": financial_data})

    assert "risk_analysis" in result
    assert isinstance(result["risk_analysis"], RiskAnalysis)


@pytest.mark.asyncio
async def test_finance_analyst(financial_data):
    agent = FinanceAnalyst("finance_test")
    result = await agent.execute({"financial_data": financial_data})

    assert "finance_analysis" in result
    assert isinstance(result["finance_analysis"], FinanceAnalysis)


@pytest.mark.asyncio
async def test_leader_analyst(leader_data):
    agent = LeaderAnalyst("leader_test")
    result = await agent.execute({"leader_data": leader_data})

    assert "leader_analysis" in result
    assert isinstance(result["leader_analysis"], LeaderAnalysis)

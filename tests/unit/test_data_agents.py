import pytest
from src.agents.data import FinanceAgent, WebSearchAgent, LeaderAgent
from src.schemas.data import FinancialData, WebSearchOutput, LeaderData


@pytest.mark.asyncio
async def test_finance_agent():
    agent = FinanceAgent("finance_test")
    result = await agent.execute({"company_code": "600519", "company_name": "贵州茅台"})

    assert "financial_data" in result
    data = result["financial_data"]
    assert isinstance(data, FinancialData)
    assert data.company_code == "600519"
    assert len(data.revenue) > 0


@pytest.mark.asyncio
async def test_websearch_agent():
    agent = WebSearchAgent("websearch_test")
    result = await agent.execute({"company_name": "贵州茅台"})

    assert "search_output" in result
    output = result["search_output"]
    assert isinstance(output, WebSearchOutput)
    assert output.company_name == "贵州茅台"


@pytest.mark.asyncio
async def test_leader_agent():
    agent = LeaderAgent("leader_test")
    result = await agent.execute({"leader_name": "丁雄军", "company_name": "贵州茅台"})

    assert "leader_data" in result
    data = result["leader_data"]
    assert isinstance(data, LeaderData)
    assert data.leader_name == "丁雄军"

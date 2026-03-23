import pytest
from src.agents.base import BaseAgent, AgentFailure


class MockAgent(BaseAgent):
    def __init__(self, agent_id: str, should_fail: bool = False):
        super().__init__(agent_id)
        self.should_fail = should_fail
        self.call_count = 0

    async def execute(self, input_data: dict) -> dict:
        self.call_count += 1
        if self.should_fail:
            raise ValueError("Mock failure")
        return {"result": "success"}


@pytest.mark.asyncio
async def test_execute_with_retry_success():
    agent = MockAgent("test", should_fail=False)
    result = await agent.execute_with_retry({})
    assert result["result"] == "success"
    assert agent.call_count == 1


@pytest.mark.asyncio
async def test_execute_with_retry_failure():
    agent = MockAgent("test", should_fail=True)
    with pytest.raises(AgentFailure):
        await agent.execute_with_retry({})
    assert agent.call_count == 3

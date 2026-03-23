import pytest
from src.orchestrator import DAGOrchestrator, Task, TaskStatus
from src.schemas import Report


@pytest.mark.asyncio
async def test_e2e_orchestrator_basic():
    """端到端测试：Orchestrator 基础流程"""
    orchestrator = DAGOrchestrator()

    # 添加简单任务链
    task1 = Task(id="task1", agent="test_agent1", depends_on=[], status=TaskStatus.PENDING)
    task2 = Task(id="task2", agent="test_agent2", depends_on=["task1"], status=TaskStatus.PENDING)

    orchestrator.add_task(task1)
    orchestrator.add_task(task2)

    # 验证依赖解析
    ready = orchestrator.get_ready_tasks()
    assert len(ready) == 1
    assert ready[0].id == "task1"

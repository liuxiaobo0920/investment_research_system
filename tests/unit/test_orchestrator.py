import pytest
from src.orchestrator import Task, TaskStatus, DAGOrchestrator


def test_task_creation():
    task = Task(id="test", agent="TestAgent")
    assert task.status == TaskStatus.PENDING
    assert task.depends_on == []


def test_get_ready_tasks():
    orch = DAGOrchestrator()
    t1 = Task(id="t1", agent="A1")
    t2 = Task(id="t2", agent="A2", depends_on=["t1"])
    orch.add_task(t1)
    orch.add_task(t2)

    ready = orch.get_ready_tasks()
    assert len(ready) == 1
    assert ready[0].id == "t1"

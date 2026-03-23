from .task import Task, TaskStatus


class DAGOrchestrator:
    def __init__(self):
        self.tasks: dict[str, Task] = {}

    def add_task(self, task: Task) -> None:
        self.tasks[task.id] = task

    def get_ready_tasks(self) -> list[Task]:
        """返回所有依赖已满足的pending任务"""
        ready = []
        for task in self.tasks.values():
            if task.status != TaskStatus.PENDING:
                continue
            deps_met = all(
                self.tasks[dep_id].status == TaskStatus.COMPLETED
                for dep_id in task.depends_on
            )
            if deps_met:
                ready.append(task)
        return ready

    async def run(self) -> dict:
        """执行DAG直到所有任务完成"""
        return {}

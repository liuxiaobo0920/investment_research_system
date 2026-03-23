import asyncio
from typing import Callable, Any
from .task import Task, TaskStatus


class DAGOrchestrator:
    def __init__(self, max_concurrent: int = 5):
        self.tasks: dict[str, Task] = {}
        self.semaphore = asyncio.Semaphore(max_concurrent)
        self.progress_callback: Callable[[str, TaskStatus], None] | None = None

    def add_task(self, task: Task) -> None:
        self.tasks[task.id] = task

    def set_progress_callback(self, callback: Callable[[str, TaskStatus], None]) -> None:
        self.progress_callback = callback

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

    def _assemble_input(self, task: Task) -> dict[str, Any]:
        """从依赖任务的output_data中装配input_data"""
        input_data = {}
        for dep_id in task.depends_on:
            dep_task = self.tasks[dep_id]
            if dep_task.status == TaskStatus.COMPLETED:
                input_data.update(dep_task.output_data)
        return input_data

    async def run(self) -> dict:
        """执行DAG直到所有任务完成"""
        while True:
            ready = self.get_ready_tasks()
            if not ready:
                pending = [t for t in self.tasks.values() if t.status == TaskStatus.PENDING]
                if not pending:
                    break
                await asyncio.sleep(0.1)
                continue

            await asyncio.gather(*[self._execute_task(task) for task in ready])

        return {t.id: t.output_data for t in self.tasks.values() if t.status == TaskStatus.COMPLETED}

    async def _execute_task(self, task: Task) -> None:
        async with self.semaphore:
            task.status = TaskStatus.RUNNING
            if self.progress_callback:
                self.progress_callback(task.id, TaskStatus.RUNNING)

            try:
                task.input_data = self._assemble_input(task)
                task.output_data = {"result": f"executed_{task.id}"}
                task.status = TaskStatus.COMPLETED
                if self.progress_callback:
                    self.progress_callback(task.id, TaskStatus.COMPLETED)
            except Exception as e:
                import logging
                logging.getLogger(__name__).error(f"Task {task.id} failed: {e}")
                task.status = TaskStatus.FAILED
                if self.progress_callback:
                    self.progress_callback(task.id, TaskStatus.FAILED)

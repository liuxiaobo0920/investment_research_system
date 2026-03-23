from abc import ABC, abstractmethod
from typing import Any
import logging

logger = logging.getLogger(__name__)


class BaseAgent(ABC):
    uses_external_data: bool = False

    def __init__(self, agent_id: str):
        self.agent_id = agent_id

    @abstractmethod
    async def execute(self, input_data: dict[str, Any]) -> dict[str, Any]:
        """执行Agent逻辑"""
        pass

    def sanitize_external_input(self, text: str) -> str:
        """清理外部数据中的潜在注入模式"""
        if not self.uses_external_data:
            return text
        return f"[EXTERNAL_DATA_START]\n{text}\n[EXTERNAL_DATA_END]"

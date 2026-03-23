from abc import ABC, abstractmethod
from typing import Any
import logging
import asyncio

logger = logging.getLogger(__name__)


class AgentFailure(Exception):
    pass


class BaseAgent(ABC):
    uses_external_data: bool = False
    max_retries: int = 3

    def __init__(self, agent_id: str):
        self.agent_id = agent_id

    @abstractmethod
    async def execute(self, input_data: dict[str, Any]) -> dict[str, Any]:
        """执行Agent逻辑"""
        pass

    async def execute_with_retry(self, input_data: dict[str, Any]) -> dict[str, Any]:
        """带重试的执行"""
        for attempt in range(self.max_retries):
            try:
                logger.info(f"Agent {self.agent_id} starting (attempt {attempt + 1})")
                result = await self.execute(input_data)
                logger.info(f"Agent {self.agent_id} completed")
                return result
            except Exception as e:
                logger.warning(f"Agent {self.agent_id} failed (attempt {attempt + 1}): {e}")
                if attempt < self.max_retries - 1:
                    await asyncio.sleep(2 ** attempt)
                else:
                    logger.error(f"Agent {self.agent_id} failed after {self.max_retries} attempts")
                    raise AgentFailure(f"Agent {self.agent_id} failed") from e

    def sanitize_external_input(self, text: str) -> str:
        """清理外部数据中的潜在注入模式"""
        if not self.uses_external_data:
            return text
        return f"[EXTERNAL_DATA_START]\n{text}\n[EXTERNAL_DATA_END]"

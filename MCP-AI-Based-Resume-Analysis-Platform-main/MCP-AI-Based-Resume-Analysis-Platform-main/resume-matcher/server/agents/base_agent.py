"""
Base Agent
----------
Abstract base class for all agents.
Every agent calls existing MCP tools via execute_tool() — no tool logic is duplicated.
"""

import logging
from abc import ABC, abstractmethod
from mcp.registry import execute_tool
from mcp.models import MCPResponse


class BaseAgent(ABC):
    """All agents inherit from this. Provides execute_tool shortcut + logging."""

    def __init__(self):
        self.logger = logging.getLogger(f"agents.{self.__class__.__name__}")

    def run_tool(self, tool_name: str, payload: dict) -> dict:
        """
        Call an existing MCP tool and return its data dict.
        Raises RuntimeError on failure so the supervisor can handle it.
        """
        result: MCPResponse = execute_tool(tool_name, payload)
        if not result.success:
            raise RuntimeError(f"[{tool_name}] {result.error}")
        self.logger.debug("Tool '%s' succeeded.", tool_name)
        return result.data

    @abstractmethod
    def run(self, context: dict) -> dict:
        """
        Execute the agent logic.
        context: shared dict built by the supervisor (resume_data, job_data, etc.)
        Returns a dict that gets merged into the final report.
        """

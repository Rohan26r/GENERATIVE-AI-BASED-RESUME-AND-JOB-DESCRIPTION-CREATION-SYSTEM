"""
MCP Tool Registry
-----------------
Central registry for all MCP tools.
Handles registration, schema validation, execution, and listing.
"""

import logging
from typing import Any, Callable
from pydantic import BaseModel, ValidationError

from mcp.models import MCPResponse

logger = logging.getLogger("mcp.registry")

# Internal store: name -> {func, schema_class}
_registry: dict[str, dict] = {}


def register_tool(name: str, func: Callable, schema: type[BaseModel]) -> None:
    """Register a tool with its handler function and Pydantic input schema."""
    if name in _registry:
        logger.warning("Tool '%s' is already registered — overwriting.", name)
    _registry[name] = {"func": func, "schema": schema}
    logger.info("Registered tool: %s", name)


def list_tools() -> list[dict]:
    """Return metadata for all registered tools."""
    result = []
    for name, entry in _registry.items():
        schema = entry["schema"]
        result.append({
            "name": name,
            "input_schema": schema.model_json_schema(),
        })
    return result


def execute_tool(name: str, payload: dict) -> MCPResponse:
    """
    Validate payload against the tool's schema and execute it.
    Returns a standard MCPResponse envelope.
    """
    if name not in _registry:
        logger.error("Tool not found: %s", name)
        return MCPResponse(success=False, tool=name, error=f"Tool '{name}' not found.")

    entry = _registry[name]
    schema_cls: type[BaseModel] = entry["schema"]
    func: Callable = entry["func"]

    # Validate input
    try:
        validated = schema_cls(**payload)
    except ValidationError as exc:
        logger.error("Validation error for tool '%s': %s", name, exc)
        return MCPResponse(success=False, tool=name, error=str(exc))

    # Execute
    try:
        result = func(validated)
        logger.info("Tool '%s' executed successfully.", name)
        return MCPResponse(success=True, tool=name, data=result)
    except Exception as exc:  # noqa: BLE001
        logger.exception("Execution error in tool '%s'", name)
        return MCPResponse(success=False, tool=name, error=str(exc))

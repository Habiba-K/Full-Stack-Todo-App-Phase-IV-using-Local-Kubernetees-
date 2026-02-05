"""
MCP (Model Context Protocol) Server Module

This module provides the MCP server implementation for hosting task management tools.
The MCP server is embedded in the FastAPI application and provides tools that the
Groq AI agent can discover and invoke.

Architecture:
- MCP server hosts tools using official MCP SDK
- Tools are stateless and wrap existing task_service functions
- All tools require user_id for ownership validation
- Tools return structured responses (task_id, status, data)
"""

from src.mcp.server import mcp_server

__all__ = ["mcp_server"]

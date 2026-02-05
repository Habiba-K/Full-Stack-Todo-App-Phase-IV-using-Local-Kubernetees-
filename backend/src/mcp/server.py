"""
MCP Server Implementation

This module implements the MCP (Model Context Protocol) server using the official MCP SDK.
The server hosts task management tools that can be discovered and invoked by the Groq AI agent.

Architecture:
- Server is embedded in FastAPI application (not a separate process)
- Tools are registered with the MCP SDK
- Server provides tool discovery and invocation capabilities
- All operations are stateless and database-backed
"""

from typing import Dict, Any, List, Optional
import logging

logger = logging.getLogger(__name__)


class MCPServer:
    """
    MCP Server for hosting task management tools.

    This server provides a standardized interface for AI agents to discover
    and invoke task management operations through the Model Context Protocol.

    Attributes:
        name: Server name identifier
        version: Server version string
        tools: Registry of available tools
        _initialized: Server initialization state
    """

    def __init__(self, name: str = "task-management-mcp-server", version: str = "1.0.0"):
        """
        Initialize the MCP server.

        Args:
            name: Server name identifier
            version: Server version string
        """
        self.name = name
        self.version = version
        self.tools: Dict[str, Any] = {}
        self._initialized = False

        logger.info(f"MCP Server initialized: {name} v{version}")

    async def startup(self):
        """
        Start the MCP server and register all tools.

        This method is called during FastAPI application startup.
        It registers all available tools with the MCP runtime.
        """
        if self._initialized:
            logger.warning("MCP Server already initialized")
            return

        try:
            # Import and register tools
            from src.mcp.tools import register_tools
            self.tools = register_tools(self)

            self._initialized = True
            logger.info(f"MCP Server started successfully with {len(self.tools)} tools")

        except Exception as e:
            logger.error(f"Failed to start MCP Server: {e}")
            raise

    async def shutdown(self):
        """
        Shutdown the MCP server and cleanup resources.

        This method is called during FastAPI application shutdown.
        """
        if not self._initialized:
            return

        try:
            # Cleanup resources
            self.tools.clear()
            self._initialized = False
            logger.info("MCP Server shutdown successfully")

        except Exception as e:
            logger.error(f"Error during MCP Server shutdown: {e}")
            raise

    def register_tool(
        self,
        name: str,
        description: str,
        parameters: Dict[str, Any],
        handler: Any
    ):
        """
        Register a tool with the MCP server.

        Args:
            name: Tool name (e.g., "add_task")
            description: Human-readable tool description
            parameters: JSON Schema for tool parameters
            handler: Async function that executes the tool
        """
        if name in self.tools:
            logger.warning(f"Tool '{name}' already registered, overwriting")

        self.tools[name] = {
            "name": name,
            "description": description,
            "parameters": parameters,
            "handler": handler
        }

        logger.debug(f"Registered tool: {name}")

    def get_tool_definitions(self) -> List[Dict[str, Any]]:
        """
        Get all tool definitions in MCP format.

        Returns:
            List of tool definitions with name, description, and parameters
        """
        return [
            {
                "name": tool["name"],
                "description": tool["description"],
                "parameters": tool["parameters"]
            }
            for tool in self.tools.values()
        ]

    async def invoke_tool(
        self,
        tool_name: str,
        arguments: Dict[str, Any],
        user_id: str,
        db: Any
    ) -> Dict[str, Any]:
        """
        Invoke a tool by name with the provided arguments.

        Args:
            tool_name: Name of the tool to invoke
            arguments: Tool arguments as dictionary
            user_id: Authenticated user ID for ownership validation
            db: Database session for tool execution

        Returns:
            Tool execution result as dictionary

        Raises:
            ValueError: If tool not found
        """
        if tool_name not in self.tools:
            raise ValueError(f"Tool not found: {tool_name}")

        tool = self.tools[tool_name]
        handler = tool["handler"]

        try:
            # Invoke the tool handler with user_id and db session
            result = await handler(arguments, user_id, db)
            return result

        except Exception as e:
            logger.error(f"Error invoking tool '{tool_name}': {e}")
            return {
                "status": "error",
                "error": {
                    "type": "execution_error",
                    "message": str(e)
                }
            }

    @property
    def is_initialized(self) -> bool:
        """Check if server is initialized."""
        return self._initialized

    def get_capabilities(self) -> Dict[str, Any]:
        """
        Get server capabilities.

        Returns:
            Dictionary describing server capabilities
        """
        return {
            "name": self.name,
            "version": self.version,
            "tools": len(self.tools),
            "capabilities": {
                "tool_discovery": True,
                "tool_invocation": True,
                "stateless": True,
                "user_scoped": True
            }
        }


# Global MCP server instance
mcp_server = MCPServer(
    name="task-management-mcp-server",
    version="1.0.0"
)

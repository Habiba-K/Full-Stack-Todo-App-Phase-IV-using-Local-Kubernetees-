import logging
from groq import AsyncGroq
from typing import List, Dict, Any, Optional
import json
from src.config import settings
from src.mcp import mcp_server
from sqlalchemy.ext.asyncio import AsyncSession

logger = logging.getLogger(__name__)


# System prompt for the agent
SYSTEM_PROMPT = """You are a helpful task management assistant. You help users manage their todo list through natural language conversation.

Your capabilities:
- Create new tasks when users describe what they need to do
- List and show tasks with filtering options
- Update task details (title, description)
- Mark tasks as complete
- Delete tasks (always ask for confirmation first)
- Maintain conversational context across multiple messages

Guidelines:
- Be friendly and conversational
- Extract task details from natural language (e.g., "buy groceries by Friday" → title: "Buy groceries")
- Format task lists in a readable way with numbers (1, 2, 3...)
- Never expose raw errors - translate them into friendly messages
- When showing tasks, include their status (pending/completed) and any relevant details

CRITICAL - Handling Task References:
When users refer to tasks by number (e.g., "task 2", "the second one", "number 1"):
1. FIRST, check if you recently called list_tasks - look at the previous tool results in this conversation
2. If you have a recent list, map the number to the task_id from that list:
   - "task 1" or "first" = first task in the list
   - "task 2" or "second" = second task in the list
   - etc.
3. Extract the task_id from the list result and use it for update_task, complete_task, or delete_task
4. If you DON'T have a recent list, call list_tasks FIRST to get the current tasks, THEN perform the requested action

Example conversation flow:
User: "Show me all my tasks"
You: Call list_tasks → Get results with task IDs → Show numbered list to user
User: "Change task 2 to 'Call mom'"
You: Look at previous list_tasks result → Find task at position 2 → Extract its task_id → Call update_task with that task_id

Context handling:
- Use previous tool call results to resolve references like "that task" or "the first one"
- When a user says "also" or "and", apply changes to the most recently mentioned task
- Always maintain awareness of the most recent task list shown to the user

Error handling:
- If a task is not found, suggest showing the task list
- If input is unclear, ask for clarifying questions
- Keep error messages user-friendly and actionable"""


def convert_mcp_tools_to_groq_format(mcp_tools: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Convert MCP tool definitions to Groq tool calling format.

    Args:
        mcp_tools: List of MCP tool definitions

    Returns:
        List of tools in Groq format
    """
    groq_tools = []

    for tool in mcp_tools:
        groq_tool = {
            "type": "function",
            "function": {
                "name": tool["name"],
                "description": tool["description"],
                "parameters": tool["parameters"]
            }
        }
        groq_tools.append(groq_tool)

    return groq_tools


async def run_agent(
    user_id: str,
    conversation_messages: List[Dict[str, Any]],
    user_message: str,
    db: AsyncSession
) -> tuple[str, Optional[List[Dict[str, Any]]]]:
    """
    Run the AI agent with Groq API and MCP tool calling.

    Args:
        user_id: Authenticated user ID
        conversation_messages: Previous conversation history
        user_message: New user message
        db: Database session for tool execution

    Returns:
        Tuple of (agent_response_text, tool_calls_metadata)
    """
    # Initialize Groq client
    client = AsyncGroq(api_key=settings.groq_api_key)

    # Get tool definitions from MCP server
    mcp_tool_definitions = mcp_server.get_tool_definitions()
    groq_tools = convert_mcp_tools_to_groq_format(mcp_tool_definitions)

    # Build messages for Groq API
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]

    # Add conversation history
    for msg in conversation_messages:
        messages.append({
            "role": msg["role"],
            "content": msg["content"]
        })

    # Add new user message
    messages.append({"role": "user", "content": user_message})

    # Tool calling loop (max 5 iterations to prevent infinite loops)
    tool_calls_metadata = []
    max_iterations = 5

    for iteration in range(max_iterations):
        try:
            # Call Groq API with tools
            response = await client.chat.completions.create(
                model=settings.groq_model,
                messages=messages,
                tools=groq_tools,
                tool_choice="auto",
                temperature=0.7,
                max_tokens=1024
            )

            assistant_message = response.choices[0].message

            # Check if agent wants to call tools
            if assistant_message.tool_calls:
                # Add assistant message with tool calls to history
                messages.append({
                    "role": "assistant",
                    "content": assistant_message.content or "",
                    "tool_calls": [
                        {
                            "id": tc.id,
                            "type": "function",
                            "function": {
                                "name": tc.function.name,
                                "arguments": tc.function.arguments
                            }
                        }
                        for tc in assistant_message.tool_calls
                    ]
                })

                # Execute each tool call through MCP server
                for tool_call in assistant_message.tool_calls:
                    tool_name = tool_call.function.name
                    tool_args = json.loads(tool_call.function.arguments)

                    # Invoke tool through MCP server
                    tool_result = await mcp_server.invoke_tool(
                        tool_name=tool_name,
                        arguments=tool_args,
                        user_id=user_id,
                        db=db
                    )

                    # Store metadata for response
                    tool_calls_metadata.append({
                        "tool": tool_name,
                        "input": tool_args,
                        "result": tool_result
                    })

                    # Add tool result to messages
                    messages.append({
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": json.dumps(tool_result)
                    })

                # Continue loop to get agent's response after tool execution
                continue

            else:
                # No more tool calls - return final response
                return assistant_message.content or "I'm not sure how to help with that.", tool_calls_metadata if tool_calls_metadata else None

        except Exception as e:
            logger.error(f"Error in agent execution (iteration {iteration}): {e}")
            return f"I encountered an error while processing your request. Please try again.", tool_calls_metadata if tool_calls_metadata else None

    # If we hit max iterations, return what we have
    return "I've completed the requested actions.", tool_calls_metadata if tool_calls_metadata else None

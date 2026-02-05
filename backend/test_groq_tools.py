"""
Simple Test: Check if Groq AI can call MCP tools

This test directly calls the agent with a simple command to see if tools are invoked.
"""
import asyncio
import json
from groq import AsyncGroq
from src.config import settings
from src.mcp.server import mcp_server
from src.database import get_session

async def test_groq_tool_calling():
    print("=" * 70)
    print("TESTING GROQ AI TOOL CALLING")
    print("=" * 70)

    # Initialize Groq client
    client = AsyncGroq(api_key=settings.groq_api_key)

    # Initialize MCP server
    await mcp_server.startup()

    # Get tool definitions
    mcp_tools = mcp_server.get_tool_definitions()
    print(f"\nMCP Tools available: {len(mcp_tools)}")
    for tool in mcp_tools:
        print(f"  - {tool['name']}")

    # Convert to Groq format
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

    print(f"\nGroq tools formatted: {len(groq_tools)}")

    # Test message
    user_message = "Show me all my tasks"

    messages = [
        {
            "role": "system",
            "content": "You are a task management assistant. Use the available tools to help users manage their tasks."
        },
        {
            "role": "user",
            "content": user_message
        }
    ]

    print(f"\nUser message: '{user_message}'")
    print("\nCalling Groq API...")

    try:
        response = await client.chat.completions.create(
            model=settings.groq_model,
            messages=messages,
            tools=groq_tools,
            tool_choice="auto",
            temperature=0.7,
            max_tokens=1024
        )

        assistant_message = response.choices[0].message

        print(f"\nAssistant response:")
        print(f"  Content: {assistant_message.content}")
        print(f"  Tool calls: {assistant_message.tool_calls}")

        if assistant_message.tool_calls:
            print(f"\n✓ SUCCESS! AI called {len(assistant_message.tool_calls)} tool(s):")
            for tc in assistant_message.tool_calls:
                print(f"  - Tool: {tc.function.name}")
                print(f"    Arguments: {tc.function.arguments}")

            # Now actually execute the tool
            print("\nExecuting tool...")
            user_id = "3805678f-bfe2-4698-98c8-0c8a75f71b62"

            async for db in get_session():
                try:
                    tool_call = assistant_message.tool_calls[0]
                    tool_name = tool_call.function.name
                    tool_args = json.loads(tool_call.function.arguments)

                    result = await mcp_server.invoke_tool(
                        tool_name=tool_name,
                        arguments=tool_args,
                        user_id=user_id,
                        db=db
                    )

                    print(f"\nTool execution result:")
                    print(json.dumps(result, indent=2))

                except Exception as e:
                    print(f"\n✗ Tool execution failed: {e}")
                    import traceback
                    traceback.print_exc()
                finally:
                    break
        else:
            print(f"\n✗ FAILED! AI did not call any tools.")
            print("This means the AI doesn't understand when to use tools.")

    except Exception as e:
        print(f"\n✗ Error calling Groq API: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_groq_tool_calling())

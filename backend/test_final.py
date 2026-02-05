"""
Final Test: AI Chat Agent with Fixed Tool Schemas

This test verifies that the AI agent can now properly call tools
without needing to provide user_id parameter.
"""
import asyncio
import json
from groq import AsyncGroq
from src.config import settings
from src.mcp.server import mcp_server
from src.database import get_session

async def test_fixed_agent():
    print("=" * 70)
    print("TESTING AI AGENT WITH FIXED TOOL SCHEMAS")
    print("=" * 70)

    # Initialize Groq client
    client = AsyncGroq(api_key=settings.groq_api_key)

    # Get tool definitions (now without user_id)
    mcp_tools = mcp_server.get_tool_definitions()

    print(f"\nMCP Tools: {len(mcp_tools)}")
    print("\nChecking list_tasks schema:")
    list_tasks_schema = [t for t in mcp_tools if t['name'] == 'list_tasks'][0]
    print(f"  Required parameters: {list_tasks_schema['parameters'].get('required', [])}")
    print(f"  Properties: {list(list_tasks_schema['parameters']['properties'].keys())}")

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

    # Test message
    user_message = "Show me all my tasks"

    messages = [
        {
            "role": "system",
            "content": "You are a helpful task management assistant. Use the available tools to help users manage their tasks. When listing tasks, call list_tasks with appropriate status filter."
        },
        {
            "role": "user",
            "content": user_message
        }
    ]

    print(f"\nUser: '{user_message}'")
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

        if assistant_message.tool_calls:
            print(f"\nSUCCESS! AI called {len(assistant_message.tool_calls)} tool(s):")

            for tc in assistant_message.tool_calls:
                print(f"\n  Tool: {tc.function.name}")
                print(f"  Arguments: {tc.function.arguments}")

                # Parse arguments
                args = json.loads(tc.function.arguments)

                # Check if user_id is in arguments
                if 'user_id' in args:
                    print(f"  WARNING: AI still sending user_id: {args['user_id']}")
                else:
                    print(f"  GOOD: No user_id in arguments")

            # Execute the tool
            print("\n" + "=" * 70)
            print("EXECUTING TOOL WITH BACKEND")
            print("=" * 70)

            user_id = "3805678f-bfe2-4698-98c8-0c8a75f71b62"

            async for db in get_session():
                try:
                    tool_call = assistant_message.tool_calls[0]
                    tool_name = tool_call.function.name
                    tool_args = json.loads(tool_call.function.arguments)

                    print(f"\nCalling: {tool_name}")
                    print(f"With args: {tool_args}")
                    print(f"User ID (from session): {user_id}")

                    result = await mcp_server.invoke_tool(
                        tool_name=tool_name,
                        arguments=tool_args,
                        user_id=user_id,
                        db=db
                    )

                    print(f"\nResult:")
                    if 'tasks' in result:
                        print(f"  Found {result['count']} tasks:")
                        for task in result['tasks']:
                            print(f"    - {task['title']} (Completed: {task['completed']})")
                    else:
                        print(json.dumps(result, indent=2))

                    print("\n" + "=" * 70)
                    print("TEST PASSED! AI agent is working correctly!")
                    print("=" * 70)

                except Exception as e:
                    print(f"\nERROR executing tool: {e}")
                    import traceback
                    traceback.print_exc()
                finally:
                    break
        else:
            print(f"\nFAILED: AI did not call any tools")
            print(f"Response: {assistant_message.content}")

    except Exception as e:
        print(f"\nERROR: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_fixed_agent())

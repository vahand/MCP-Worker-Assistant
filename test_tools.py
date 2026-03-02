#!/usr/bin/env python3
"""Test script to verify MCP tools are working correctly."""

import asyncio
import nest_asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

nest_asyncio.apply()

PATH_MCP_SERVER = "/Users/Vahan/Documents/Development/AI/MCP/apple-daily-planning/server.py"

async def test_tools():
    """Test calling MCP tools directly."""
    params = StdioServerParameters(
        command="python3",
        args=[PATH_MCP_SERVER]
    )

    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as session:
            print("Initializing MCP session...")
            await session.initialize()
            print("Session initialized\n")

            # Test 1: Say Good Morning
            print("=" * 50)
            print("Test 1: say_good_morning")
            print("=" * 50)
            try:
                result = await session.call_tool("say_good_morning", {})
                print(f"Result type: {type(result)}")
                print(f"Has content: {hasattr(result, 'content')}")
                if hasattr(result, 'content'):
                    print(f"Content length: {len(result.content)}")
                    if len(result.content) > 0:
                        content = result.content[0]
                        print(f"Content[0] type: {type(content)}")
                        print(f"Has text: {hasattr(content, 'text')}")
                        if hasattr(content, 'text'):
                            print(f"Text: {content.text}")
                        else:
                            print(f"Content: {content}")
                print()
            except Exception as e:
                print(f"Error: {e}\n")

            # Test 2: Open Tasks
            print("=" * 50)
            print("Test 2: open_for_today_tasks")
            print("=" * 50)
            try:
                result = await session.call_tool("open_for_today_tasks", {})
                print(f"Result type: {type(result)}")
                print(f"Has content: {hasattr(result, 'content')}")
                if hasattr(result, 'content'):
                    print(f"Content length: {len(result.content)}")
                    if len(result.content) > 0:
                        content = result.content[0]
                        print(f"Content[0] type: {type(content)}")
                        print(f"Has text: {hasattr(content, 'text')}")
                        if hasattr(content, 'text'):
                            print(f"Text: {content.text}")
                        else:
                            print(f"Content: {content}")
                print()
            except Exception as e:
                print(f"Error: {e}\n")

            # Test 3: Calendar
            print("=" * 50)
            print("Test 3: calendar_today")
            print("=" * 50)
            try:
                result = await session.call_tool("calendar_today", {
                    "calendar_names": ["Calendrier", "EPITECH", "HFT"]
                })
                print(f"Result type: {type(result)}")
                print(f"Has content: {hasattr(result, 'content')}")
                if hasattr(result, 'content'):
                    print(f"Content length: {len(result.content)}")
                    if len(result.content) > 0:
                        content = result.content[0]
                        print(f"Content[0] type: {type(content)}")
                        print(f"Has text: {hasattr(content, 'text')}")
                        if hasattr(content, 'text'):
                            print(f"Text: {content.text}")
                        else:
                            print(f"Content: {content}")
                print()
            except Exception as e:
                print(f"Error: {e}\n")

if __name__ == "__main__":
    asyncio.run(test_tools())

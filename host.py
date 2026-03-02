import asyncio
import nest_asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from langchain_ollama import ChatOllama

from agents import create_calendar_agent, create_tasks_agent, create_orchestrator

# Apply nest_asyncio to allow nested event loops
nest_asyncio.apply()
from tool_factory import (
    make_calendar_tool,
    make_tasks_tool,
    make_weekend_tasks_tool,
    make_current_work_tool,
    make_good_morning_tool
)


PATH_MCP_SERVER = "/Users/Vahan/Documents/Development/AI/MCP/apple-daily-planning/server.py"

llm = ChatOllama(
    model="qwen2.5:7b",  # Qwen2.5 has excellent tool calling support
    temperature=0.2,  # Lower temperature for more reliable tool usage
    num_predict=512  # Limit response length
)

async def main():
    params = StdioServerParameters(
        command="python3",
        args=[PATH_MCP_SERVER]
    )

    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as session:
            print("Initialising MCP session...")
            await session.initialize()
            print("MCP session initialized")

            print("Creating tools...")
            # Create MCP tools
            calendar_tool = make_calendar_tool(session)
            tasks_tool = make_tasks_tool(session)
            weekend_tasks_tool = make_weekend_tasks_tool(session)
            current_work_tool = make_current_work_tool(session)
            good_morning_tool = make_good_morning_tool(session)
            print("Tools created")

            # Create sub-agents
            print("Creating sub-agents...")
            calendar_agent = create_calendar_agent(calendar_tool, llm)
            tasks_agent = create_tasks_agent(tasks_tool, weekend_tasks_tool, llm)
            print("Sub-agents created")

            # Create orchestrator with sub-agents + utility tools
            print("Creating orchestrator...")
            utility_tools = [good_morning_tool, current_work_tool]
            agent = create_orchestrator(calendar_agent, tasks_agent, utility_tools, llm)
            print("Orchestrator ready")

            print("\n=== AI Assistant Ready ===")
            print("I can help you with your calendar and tasks.")
            print("Type 'exit' or 'quit' to end the conversation.\n")

            # Chat loop
            while True:
                try:
                    user_input = input("You: ").strip()

                    if not user_input:
                        continue

                    if user_input.lower() in ['exit', 'quit', 'bye']:
                        print("\nGoodbye!")
                        break

                    # Invoke the agent asynchronously to use _arun methods
                    print("Processing your request...")
                    print("[DEBUG] Invoking agent...")
                    response = await agent.ainvoke(
                        {"messages": [{"role": "user", "content": user_input}]}
                    )
                    print(f"[DEBUG] Agent response type: {type(response)}")
                    print(f"[DEBUG] Agent response keys: {response.keys() if isinstance(response, dict) else 'N/A'}")

                    # Debug: show message flow
                    if "messages" in response:
                        print(f"[DEBUG] Number of messages: {len(response['messages'])}")
                        for i, msg in enumerate(response['messages']):
                            if hasattr(msg, 'type'):
                                msg_type = msg.type
                                # Check if it's a tool call message
                                if hasattr(msg, 'tool_calls') and msg.tool_calls:
                                    print(f"[DEBUG] Message {i}: type={msg_type}, has tool_calls")
                                else:
                                    print(f"[DEBUG] Message {i}: type={msg_type}")

                    # Extract and display the response
                    if "messages" in response:
                        last_message = response["messages"][-1]
                        if hasattr(last_message, 'content'):
                            print(f"\nAssistant: {last_message.content}\n")
                        else:
                            print(f"\nAssistant: {str(last_message)}\n")
                    else:
                        print(f"\nAssistant: {response}\n")

                except KeyboardInterrupt:
                    print("\n\nGoodbye!")
                    break
                except Exception as e:
                    import traceback
                    print(f"\nError: {e}")
                    print(f"Traceback:\n{traceback.format_exc()}\n")

if __name__ == "__main__":
    asyncio.run(main())
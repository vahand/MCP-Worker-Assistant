import asyncio
import argparse
import nest_asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from langchain_ollama import ChatOllama

from agents.agents import create_calendar_agent, create_tasks_agent, create_orchestrator
from debug.debug import debug_response

# Apply nest_asyncio to allow nested event loops
nest_asyncio.apply()
from tools.calendar_tools import make_calendar_tool, make_calendar_names_tool
from tools.tasks_tools import make_tasks_tool, make_weekend_tasks_tool
from tools.notes_tools import make_current_work_tool
from tools.simple_tools import make_good_morning_tool


from config import DEBUG, PATH_MCP_SERVER

llm = ChatOllama(
    model="qwen2.5:7b",
    temperature=0.2,  # Lower temperature for more reliable tool usage
    num_predict=512  # Limit response length
)


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Worker Assistant - MCP Host",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python host.py          # Launch with CLI (default)
  python host.py --cli    # Launch with CLI explicitly
  python host.py --gui    # Launch with graphical interface
        """
    )
    mode_group = parser.add_mutually_exclusive_group()
    mode_group.add_argument(
        "--cli",
        action="store_true",
        default=True,
        help="Use command line interface (default)"
    )
    mode_group.add_argument(
        "--gui",
        action="store_true",
        help="Use graphical user interface"
    )
    return parser.parse_args()


async def initialize_agent(session):
    """Initialize all tools and create the orchestrator agent."""
    # Create MCP tools
    print("Creating tools...")
    calendar_tool = make_calendar_tool(session)
    calendar_names_tool = make_calendar_names_tool(session)
    tasks_tool = make_tasks_tool(session)
    weekend_tasks_tool = make_weekend_tasks_tool(session)
    current_work_tool = make_current_work_tool(session)
    good_morning_tool = make_good_morning_tool(session)
    print("Tools created")

    # Create sub-agents
    print("Creating sub-agents...")
    calendar_agent = create_calendar_agent(calendar_tool, calendar_names_tool, llm)
    tasks_agent = create_tasks_agent(tasks_tool, weekend_tasks_tool, llm)
    print("Sub-agents created")

    # Create orchestrator with sub-agents + utility tools
    print("Creating orchestrator...")
    utility_tools = [good_morning_tool, current_work_tool]
    agent = create_orchestrator(calendar_agent, tasks_agent, utility_tools, llm)
    print("Orchestrator ready")

    return agent


def extract_response_text(response) -> str:
    """Extract the response text from the agent response."""
    if "messages" in response:
        last_message = response["messages"][-1]
        if hasattr(last_message, 'content'):
            return last_message.content
        else:
            return str(last_message)
    else:
        return str(response)


async def run_cli(agent):
    """Run the command line interface loop."""
    # Welcome message
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

            # Invoke the orchestrator agent asynchronously
            response = await agent.ainvoke(
                {"messages": [{"role": "user", "content": user_input}]}
            )

            # Debugging response and message flow
            if DEBUG:
                debug_response(response)

            # Extract and display the response
            response_text = extract_response_text(response)
            print(f"\nAssistant: {response_text}\n")

        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            break
        except Exception as e:
            import traceback
            print(f"\nError: {e}")
            print(f"Traceback:\n{traceback.format_exc()}\n")


async def main_cli():
    """Main entry point for CLI mode."""
    params = StdioServerParameters(
        command="python3",
        args=[PATH_MCP_SERVER]
    )

    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as session:
            print("Initialising MCP session...")
            await session.initialize()
            print("MCP session initialized")

            agent = await initialize_agent(session)
            await run_cli(agent)


async def main_gui():
    """Main entry point for GUI mode."""
    params = StdioServerParameters(
        command="python3",
        args=[PATH_MCP_SERVER]
    )

    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as session:
            print("Initialising MCP session...")
            await session.initialize()
            print("MCP session initialized")

            agent = await initialize_agent(session)

            # Run GUI in a way that keeps the MCP session alive
            from ui.chat_ui import create_chat_ui
            import threading

            async def handle_message(user_input: str) -> str:
                """Handle user message and return response."""
                try:
                    response = await agent.ainvoke(
                        {"messages": [{"role": "user", "content": user_input}]}
                    )

                    if DEBUG:
                        debug_response(response)

                    return extract_response_text(response)
                except Exception as e:
                    return f"Error: {str(e)}"

            ui = create_chat_ui(handle_message)
            ui.run()


def main():
    """Main entry point with argument parsing."""
    args = parse_args()

    if args.gui:
        print("Starting GUI mode...")
        asyncio.run(main_gui())
    else:
        print("Starting CLI mode...")
        asyncio.run(main_cli())


if __name__ == "__main__":
    main()
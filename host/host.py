import asyncio
import nest_asyncio
import os

from mcp import ClientSession
from mcp.client.sse import sse_client
from langchain_ollama import ChatOllama
from dotenv import load_dotenv

from agents.agents import create_calendar_agent, create_tasks_agent, create_orchestrator
from debug.logger import debug_response
from tools.calendar_tools import make_calendar_tool, make_calendar_names_tool
from tools.tasks_tools import make_tasks_tool, make_weekend_tasks_tool
from tools.notes_tools import make_current_work_tool
from tools.simple_tools import make_good_morning_tool


load_dotenv()
MCP_SERVER_URL = os.getenv("MCP_SERVER_URL", "http://127.0.0.1:8000/sse")
MODEL_NAME = os.getenv("MODEL_NAME")
TEMPERATURE = float(os.getenv("TEMPERATURE"))
NUM_PREDICT = int(os.getenv("NUM_PREDICT"))
DEBUG = os.getenv("DEBUG", "False").lower() == "true"


# Apply nest_asyncio to allow nested event loops
nest_asyncio.apply()

llm = ChatOllama(
    model=MODEL_NAME,
    temperature=TEMPERATURE,
    num_predict=NUM_PREDICT
)


async def main():
    async with sse_client(MCP_SERVER_URL) as (read, write):
        async with ClientSession(read, write) as session:
            print("Initialising MCP session...")
            await session.initialize()
            print("MCP session initialized")

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
            calendar_agent = create_calendar_agent(
                calendar_tool, calendar_names_tool, llm)
            tasks_agent = create_tasks_agent(
                tasks_tool, weekend_tasks_tool, llm)
            print("Sub-agents created")

            # Create orchestrator with sub-agents + utility tools
            print("Creating orchestrator...")
            utility_tools = [good_morning_tool, current_work_tool]
            agent = create_orchestrator(
                calendar_agent, tasks_agent, utility_tools, llm)
            print("Orchestrator ready")

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

                    # Invoke the orchestrator agent asynchronously (use _arun methods)
                    response = await agent.ainvoke(
                        {"messages": [{"role": "user", "content": user_input}]}
                    )

                    # Debugging response and message flow
                    if DEBUG:
                        debug_response(response)

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

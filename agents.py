from langchain.agents import create_agent

def create_chatbot_agent(tools, llm):
    """Create an agent with tool binding that forces Ollama to use tools.

    Args:
        tools: List of LangChain tools (calendar, tasks, etc.)
        llm: The language model to use
    """

    system_prompt = """You are a helpful AI assistant. You MUST use the available tools to get accurate information.

IMPORTANT: When the user asks about:
- Calendar or events → Use calendar_today tool
- Tasks or reminders → Use open_for_today_tasks or open_weekend_tasks tools
- Current work → Use current_work_note tool

DO NOT make up information. ALWAYS use tools to get real data.

Available tools:
- calendar_today: Get today's calendar events
- open_for_today_tasks: Get open reminders/tasks for today
- open_weekend_tasks: Get weekend tasks
- current_work_note: Get current work note content
- say_good_morning: Get a morning message"""

    # Bind tools to the LLM to force tool usage
    llm_with_tools = llm.bind_tools(tools)

    agent = create_agent(
        model=llm_with_tools,
        tools=tools,
        system_prompt=system_prompt
    )

    return agent

def run_day_planning(calendar_tool, tasks_tool, llm):
    """Legacy function for day planning - creates and runs a planning workflow."""

    planner_agent = create_agent(
        model=llm,
        tools=[calendar_tool, tasks_tool]
    )

    agenda = planner_agent.invoke(
        {"messages": [{"role": "user", "content": "Summarize today's fixed commitments and free slots."}]}
    )
    tasks = planner_agent.invoke(
        {"messages": [{"role": "user", "content": "Categorize tasks by urgency and efforts."}]}
    )
    final_plan = planner_agent.invoke(
        {"messages": [{"role": "user", "content": f"""
        Using this agenda:
        {agenda}
        And these tasks:
        {tasks}
        Create a prioritized plan for the day, allocating tasks to free slots and suggesting optimal times for high-effort tasks. Add some breaks as well.
        """}]}
    )

    return final_plan
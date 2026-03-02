from langchain.agents import create_agent
from pydantic import BaseModel, Field


class AgentQuery(BaseModel):
    """Input schema for sub-agent tools."""
    query: str = Field(description="The question or request to send to this agent")


def create_calendar_agent(calendar_tool, llm):
    """Create a sub-agent specialized in calendar and scheduling."""
    
    system_prompt = """You are a calendar specialist agent. You have access to the user's calendar.

Your job:
- Fetch and summarize today's calendar events
- Identify free time slots
- Report on scheduled meetings and commitments

ALWAYS use the calendar_today tool to get real data. NEVER make up events."""

    llm_with_tools = llm.bind_tools([calendar_tool])
    
    agent = create_agent(
        model=llm_with_tools,
        tools=[calendar_tool],
        system_prompt=system_prompt,
        name="calendar_agent"
    )
    
    return agent


def create_tasks_agent(tasks_tool, weekend_tasks_tool, llm):
    """Create a sub-agent specialized in tasks and reminders."""
    
    tools = [tasks_tool, weekend_tasks_tool]
    
    system_prompt = """You are a tasks specialist agent. You have access to the user's reminders and tasks.

Your job:
- Fetch and list today's tasks using open_for_today_tasks tool
- Fetch weekend tasks using open_weekend_tasks tool
- Categorize tasks by priority or type

ALWAYS use tools to get real data. NEVER make up tasks."""

    llm_with_tools = llm.bind_tools(tools)
    
    agent = create_agent(
        model=llm_with_tools,
        tools=tools,
        system_prompt=system_prompt,
        name="tasks_agent"
    )
    
    return agent


def create_orchestrator(calendar_agent, tasks_agent, utility_tools, llm):
    """Create the orchestrator agent that delegates to sub-agents.
    
    Args:
        calendar_agent: Compiled calendar sub-agent graph
        tasks_agent: Compiled tasks sub-agent graph
        utility_tools: List of simple tools (good_morning, current_work_note)
        llm: The language model
    """
    
    # Wrap sub-agents as tools
    calendar_agent_tool = calendar_agent.as_tool(
        args_schema=AgentQuery,
        name="calendar_specialist",
        description="Delegate to the calendar specialist agent. Use this when the user asks about calendar events, meetings, schedule, or free time slots."
    )
    
    tasks_agent_tool = tasks_agent.as_tool(
        args_schema=AgentQuery,
        name="tasks_specialist",
        description="Delegate to the tasks specialist agent. Use this when the user asks about tasks, reminders, to-dos, or things to do today or this weekend."
    )
    
    # Combine sub-agent tools with utility tools
    all_tools = [calendar_agent_tool, tasks_agent_tool] + utility_tools
    
    system_prompt = """You are an orchestrator AI assistant that delegates work to specialist agents.

You have access to:
- calendar_specialist: Handles all calendar, events, meetings, and scheduling questions
- tasks_specialist: Handles all tasks, reminders, and to-do questions
- say_good_morning: Returns a morning greeting
- current_work_note: Returns the content of the current work note

RULES:
1. When the user asks about calendar or events → delegate to calendar_specialist
2. When the user asks about tasks or reminders → delegate to tasks_specialist
3. When the user asks to plan the day → delegate to BOTH specialists, then combine their answers
4. For simple utility requests (good morning, current work) → use the utility tools directly
5. ALWAYS delegate to specialists instead of answering yourself for calendar/tasks questions
6. After receiving specialist responses, synthesize a clear and helpful answer for the user."""

    llm_with_tools = llm.bind_tools(all_tools)
    
    agent = create_agent(
        model=llm_with_tools,
        tools=all_tools,
        system_prompt=system_prompt,
        name="orchestrator"
    )
    
    return agent
from langchain.tools import BaseTool
import asyncio
import json
from typing import Optional, Type, Any
from pydantic import BaseModel, Field


class CalendarTodayTool(BaseTool):
    name: str = "calendar_today"
    description: str = "Get today's calendar events. Takes a comma-separated string of calendar names (e.g., 'Calendrier, EPITECH, HFT'). Returns a list of events with title, start_date, and end_date."
    session: object

    def _run(self, calendar_names: str = "Calendrier, EPITECH, HFT") -> str:
        async def _call():
            print(f"[DEBUG] CalendarTool called with: {calendar_names}")
            names_list = [name.strip() for name in calendar_names.split(',')]
            result = await self.session.call_tool("calendar_today", {"calendar_names": names_list})
            if hasattr(result, 'content') and len(result.content) > 0:
                content = result.content[0]
                if hasattr(content, 'text'):
                    print(f"[DEBUG] CalendarTool returning: {content.text[:200]}...")
                    return content.text
                print(f"[DEBUG] CalendarTool returning (no text attr): {str(content)[:200]}...")
                return str(content)
            print(f"[DEBUG] CalendarTool returning (no content): {str(result)[:200]}...")
        loop = asyncio.get_event_loop()
        return loop.run_until_complete(_call())

    async def _arun(self, **kwargs) -> str:
        # Extract calendar_names if provided, otherwise use default
        calendar_names = kwargs.get('calendar_names', "Calendrier, EPITECH, HFT")
        if isinstance(calendar_names, list):
            calendar_names = ", ".join(calendar_names)

        names_list = [name.strip() for name in calendar_names.split(',')]
        result = await self.session.call_tool("calendar_today", {"calendar_names": names_list})
        if hasattr(result, 'content') and len(result.content) > 0:
            content = result.content[0]
            if hasattr(content, 'text'):
                return content.text
            return str(content)
        return str(result)


class TasksTool(BaseTool):
    name: str = "open_for_today_tasks"
    description: str = "Get open reminders/tasks for today. No input needed."
    session: object

    def _run(self, **kwargs) -> str:
        print(f"[DEBUG] TasksTool called")
        print(f"[DEBUG] About to call MCP server...")

        async def _call():
            result = await self.session.call_tool("open_for_today_tasks", {})
            print(f"[DEBUG] MCP server returned")
            if hasattr(result, 'content') and len(result.content) > 0:
                content = result.content[0]
                if hasattr(content, 'text'):
                    print(f"[DEBUG] TasksTool returning: {content.text[:200]}...")
                    return content.text
                print(f"[DEBUG] TasksTool returning (no text attr): {str(content)[:200]}...")
                return str(content)
            print(f"[DEBUG] TasksTool returning (no content): {str(result)[:200]}...")
            return str(result)

        # With nest_asyncio applied, this should work in nested contexts
        loop = asyncio.get_event_loop()
        return loop.run_until_complete(_call())

    async def _arun(self, **kwargs) -> str:
        print(f"[DEBUG] TasksTool ASYNC called")
        print(f"[DEBUG] About to call MCP server (async)...")
        result = await self.session.call_tool("open_for_today_tasks", {})
        print(f"[DEBUG] MCP server returned (async)")
        if hasattr(result, 'content') and len(result.content) > 0:
            content = result.content[0]
            if hasattr(content, 'text'):
                print(f"[DEBUG] TasksTool returning (async): {content.text[:200]}...")
                return content.text
            print(f"[DEBUG] TasksTool returning (no text, async): {str(content)[:200]}...")
            return str(content)
        print(f"[DEBUG] TasksTool returning (no content, async): {str(result)[:200]}...")
        return str(result)


class WeekendTasksTool(BaseTool):
    name: str = "open_weekend_tasks"
    description: str = "Get open reminders/tasks for the weekend. No input needed."
    session: object

    def _run(self, **kwargs) -> str:
        async def _call():
            result = await self.session.call_tool("open_weekend_tasks", {})
            if hasattr(result, 'content') and len(result.content) > 0:
                content = result.content[0]
                if hasattr(content, 'text'):
                    return content.text
                return str(content)
            return str(result)
        loop = asyncio.get_event_loop()
        return loop.run_until_complete(_call())

    async def _arun(self, **kwargs) -> str:
        result = await self.session.call_tool("open_weekend_tasks", {})
        if hasattr(result, 'content') and len(result.content) > 0:
            content = result.content[0]
            if hasattr(content, 'text'):
                return content.text
            return str(content)
        return str(result)


class CurrentWorkNoteTool(BaseTool):
    name: str = "current_work_note"
    description: str = "Get the content of the 'Current Work' note. No input needed."
    session: object

    def _run(self, **kwargs) -> str:
        async def _call():
            result = await self.session.call_tool("current_work_note", {})
            if hasattr(result, 'content') and len(result.content) > 0:
                content = result.content[0]
                if hasattr(content, 'text'):
                    return content.text
                return str(content)
            return str(result)
        loop = asyncio.get_event_loop()
        return loop.run_until_complete(_call())

    async def _arun(self, **kwargs) -> str:
        result = await self.session.call_tool("current_work_note", {})
        if hasattr(result, 'content') and len(result.content) > 0:
            content = result.content[0]
            if hasattr(content, 'text'):
                return content.text
            return str(content)
        return str(result)


class GoodMorningTool(BaseTool):
    name: str = "say_good_morning"
    description: str = "Get a good morning message. No input needed."
    session: object

    def _run(self, **kwargs) -> str:
        async def _call():
            result = await self.session.call_tool("say_good_morning", {})
            if hasattr(result, 'content') and len(result.content) > 0:
                content = result.content[0]
                if hasattr(content, 'text'):
                    return content.text
                return str(content)
            return str(result)
        loop = asyncio.get_event_loop()
        return loop.run_until_complete(_call())

    async def _arun(self, **kwargs) -> str:
        result = await self.session.call_tool("say_good_morning", {})
        if hasattr(result, 'content') and len(result.content) > 0:
            content = result.content[0]
            if hasattr(content, 'text'):
                return content.text
            return str(content)
        return str(result)


def make_calendar_tool(session):
    """Create calendar tool with proper parameter handling"""
    return CalendarTodayTool(session=session)


def make_tasks_tool(session):
    """Create tasks tool"""
    return TasksTool(session=session)


def make_weekend_tasks_tool(session):
    """Create weekend tasks tool"""
    return WeekendTasksTool(session=session)


def make_current_work_tool(session):
    """Create current work note tool"""
    return CurrentWorkNoteTool(session=session)


def make_good_morning_tool(session):
    """Create good morning tool"""
    return GoodMorningTool(session=session)
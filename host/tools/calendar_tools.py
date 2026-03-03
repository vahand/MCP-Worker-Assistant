from langchain.tools import BaseTool
import asyncio

from host import DEBUG


class CalendarNamesTool(BaseTool):
    name: str = "calendar_names"
    description: str = "Get the names of all calendars available. Return as comma-separated string. No input needed."
    session: object

    def _run(self, **kwargs) -> str:
        async def _call():
            print(f"[DEBUG] CalendarNamesTool called") if DEBUG else None
            result = await self.session.call_tool("calendar_names", {})
            if hasattr(result, 'content') and len(result.content) > 0:
                content = result.content[0]
                if hasattr(content, 'text'):
                    return content.text
                return str(content)
            return str(result)

        loop = asyncio.get_event_loop()
        return loop.run_until_complete(_call())

    async def _arun(self, **kwargs) -> str:
        print(f"[DEBUG] CalendarNamesTool ASYNC called") if DEBUG else None
        result = await self.session.call_tool("calendar_names", {})
        if hasattr(result, 'content') and len(result.content) > 0:
            content = result.content[0]
            if hasattr(content, 'text'):
                return content.text
            return str(content)
        return str(result)

class CalendarTodayTool(BaseTool):
    name: str = "calendar_today"
    description: str = "Get today's events of calendar names passed as a comma-separated string for paramater 'calendar_names' (e.g.: 'Personal,Work'). Returns a list of events with title, start_date, end_date and calendar_name in JSON format."
    session: object

    def _run(self, **kwargs) -> str:
        async def _call():
            calendar_names = kwargs.get('calendar_names', "Personal")
            if isinstance(calendar_names, list):
                calendar_names = ",".join(calendar_names)

            names_list = [name.strip() for name in calendar_names.split(',')]
            result = await self.session.call_tool("calendar_today", {"calendar_names": names_list})
            if hasattr(result, 'content') and len(result.content) > 0:
                all_events = []
                for content in result.content:
                    if hasattr(content, 'text'):
                        all_events.append(content.text)
                if all_events:
                    return ";".join(all_events)
                return str(content)
            return str(result)

        loop = asyncio.get_event_loop()
        return loop.run_until_complete(_call())

    async def _arun(self, **kwargs) -> str:
        calendar_names = kwargs.get('calendar_names', "Personal")
        if isinstance(calendar_names, list):
            calendar_names = ",".join(calendar_names)

        names_list = [name.strip() for name in calendar_names.split(',')]
        print(f"[DEBUG] CalendarTool ASYNC called with calendar_names: {names_list}") if DEBUG else None
        result = await self.session.call_tool("calendar_today", {"calendar_names": names_list})
        if hasattr(result, 'content') and len(result.content) > 0:
            all_events = []
            for content in result.content:
                if hasattr(content, 'text'):
                    all_events.append(content.text)
            if all_events:
                return ";".join(all_events)
            return str(content)
        return str(result)


def make_calendar_tool(session):
    """Create calendar tool with proper parameter handling"""
    return CalendarTodayTool(session=session)


def make_calendar_names_tool(session):
    """Create calendar names tool"""
    return CalendarNamesTool(session=session)
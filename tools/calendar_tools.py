from langchain.tools import BaseTool
import asyncio


class CalendarNamesTool(BaseTool):
    name: str = "calendar_names"
    description: str = "Get the names of all calendars available. Return as comma-separated string. No input needed."
    session: object

    def _run(self, **kwargs) -> str:
        async def _call():
            print(f"[DEBUG] CalendarNamesTool called")
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
        print(f"[DEBUG] CalendarNamesTool ASYNC called")
        result = await self.session.call_tool("calendar_names", {})
        if hasattr(result, 'content') and len(result.content) > 0:
            content = result.content[0]
            if hasattr(content, 'text'):
                return content.text
            return str(content)
        return str(result)

class CalendarTodayTool(BaseTool):
    name: str = "calendar_today"
    description: str = "Get today's events of calendar names passed as a comma-separated string for paramater 'calendar_names' (e.g.: 'Personal,Work'). Returns a list of events with title, start_date, and end_date in JSON format."
    session: object

    def _run(self, calendar_names: str = "Personal") -> str:
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
        calendar_names = kwargs.get('calendar_names', "Personal")
        if isinstance(calendar_names, list):
            calendar_names = ",".join(calendar_names)

        names_list = [name.strip() for name in calendar_names.split(',')]
        print(f"[DEBUG] CalendarTool ASYNC called with calendar_names: {names_list}")
        print(f"[DEBUG] About to call MCP server (async)...")
        result = await self.session.call_tool("calendar_today", {"calendar_names": names_list})
        print(f"[DEBUG] MCP server returned (async)")
        if hasattr(result, 'content') and len(result.content) > 0:
            all_events = []
            print(f"[DEBUG] Result has content with length: {len(result.content)}")
            for content in result.content:
                if hasattr(content, 'text'):
                    all_events.append(content.text)
            if all_events:
                print(f"[DEBUG] CalendarTool returning (async): {';'.join(all_events)[:200]}...")
                return ";".join(all_events)
            print(f"[DEBUG] CalendarTool returning (no text, async): {str(content)[:200]}...")
            return str(content)
        print(f"[DEBUG] CalendarTool returning (no content, async): {str(result)[:200]}...")
        return str(result)


def make_calendar_tool(session):
    """Create calendar tool with proper parameter handling"""
    return CalendarTodayTool(session=session)


def make_calendar_names_tool(session):
    """Create calendar names tool"""
    return CalendarNamesTool(session=session)
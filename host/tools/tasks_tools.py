from langchain.tools import BaseTool
import asyncio

from debug.logger import Logger


class TasksTool(BaseTool):
    name: str = "open_for_today_tasks"
    description: str = "Get open reminders/tasks for today. No input needed."
    session: object

    def _run(self, **kwargs) -> str:
        async def _call():
            Logger.log("TasksTool called")
            result = await self.session.call_tool("open_for_today_tasks", {})
            if hasattr(result, 'content') and len(result.content) > 0:
                content = result.content[0]
                if hasattr(content, 'text'):
                    return content.text
                return str(content)
            return str(result)

        loop = asyncio.get_event_loop()
        return loop.run_until_complete(_call())

    async def _arun(self, **kwargs) -> str:
        Logger.log("TasksTool ASYNC called")
        result = await self.session.call_tool("open_for_today_tasks", {})
        if hasattr(result, 'content') and len(result.content) > 0:
            content = result.content[0]
            if hasattr(content, 'text'):
                return content.text
            return str(content)
        return str(result)


class WeekendTasksTool(BaseTool):
    name: str = "open_weekend_tasks"
    description: str = "Get open reminders/tasks for the weekend. No input needed."
    session: object

    def _run(self, **kwargs) -> str:
        async def _call():
            Logger.log("WeekendTasksTool called")
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
        Logger.log("WeekendTasksTool ASYNC called")
        result = await self.session.call_tool("open_weekend_tasks", {})
        if hasattr(result, 'content') and len(result.content) > 0:
            content = result.content[0]
            if hasattr(content, 'text'):
                return content.text
            return str(content)
        return str(result)



def make_tasks_tool(session):
    """Create tasks tool"""
    return TasksTool(session=session)


def make_weekend_tasks_tool(session):
    """Create weekend tasks tool"""
    return WeekendTasksTool(session=session)
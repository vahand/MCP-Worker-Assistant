from langchain.tools import BaseTool
import asyncio


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



def make_tasks_tool(session):
    """Create tasks tool"""
    return TasksTool(session=session)


def make_weekend_tasks_tool(session):
    """Create weekend tasks tool"""
    return WeekendTasksTool(session=session)
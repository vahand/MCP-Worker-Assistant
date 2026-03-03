from langchain.tools import BaseTool
import asyncio

from debug.logger import Logger

class CurrentWorkNoteTool(BaseTool):
    name: str = "current_work_note"
    description: str = "Get the content of the 'Current Work' note. No input needed."
    session: object

    def _run(self, **kwargs) -> str:
        async def _call():
            Logger.log("CurrentWorkNoteTool called")
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
        Logger.log("CurrentWorkNoteTool ASYNC called")
        result = await self.session.call_tool("current_work_note", {})
        if hasattr(result, 'content') and len(result.content) > 0:
            content = result.content[0]
            if hasattr(content, 'text'):
                return content.text
            return str(content)
        return str(result)


def make_current_work_tool(session):
    """Create current work note tool"""
    return CurrentWorkNoteTool(session=session)
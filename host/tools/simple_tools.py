from langchain.tools import BaseTool
import asyncio

from debug.logger import Logger

class GoodMorningTool(BaseTool):
    name: str = "say_good_morning"
    description: str = "Get a good morning message. No input needed."
    session: object

    def _run(self, **kwargs) -> str:
        async def _call():
            Logger.log("GoodMorningTool called")
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
        Logger.log("GoodMorningTool ASYNC called")
        result = await self.session.call_tool("say_good_morning", {})
        if hasattr(result, 'content') and len(result.content) > 0:
            content = result.content[0]
            if hasattr(content, 'text'):
                return content.text
            return str(content)
        return str(result)



def make_good_morning_tool(session):
    """Create good morning tool"""
    return GoodMorningTool(session=session)
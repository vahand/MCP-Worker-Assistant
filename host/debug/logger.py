"""Logger module for the MCP Host application for debugging purposes."""
from dotenv import load_dotenv
import os


load_dotenv()
LOG = os.getenv("LOG", "False").lower() == "true"
DEBUG = os.getenv("DEBUG", "False").lower() == "true"

class Logger:
    @staticmethod
    def log(message):
        if not LOG:
            return
        print(f"\033[92m[LOG] {message}\033[0m")

    @staticmethod
    def debug(message):
        if not DEBUG:
            return
        print(f"\033[94m[DEBUG] {message}\033[0m")



def debug_response(response):
    Logger.debug(f"Agent response type: {type(response)}")
    Logger.debug(f"Agent response keys: {response.keys() if isinstance(response, dict) else 'N/A'}")
    if "messages" in response:
        Logger.debug(f"Number of messages: {len(response['messages'])}")
        for i, msg in enumerate(response['messages']):
            if hasattr(msg, 'type'):
                msg_type = msg.type
                if hasattr(msg, 'tool_calls') and msg.tool_calls:
                    Logger.debug(f"Message {i}: type={msg_type}, has tool_calls")
                else:
                    Logger.debug(f"Message {i}: type={msg_type}")
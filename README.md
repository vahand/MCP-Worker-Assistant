# MCP Worker Assistant

## Introduction
This project is a simple multi-agents assistant for planning tasks. It uses a MCP server to retrieve user's calendar, tasks list and notes data to answer user's query for day planning.

## Architecture
<img width="2570" height="990" alt="image" src="https://github.com/user-attachments/assets/0b90d064-c6ae-4805-8027-f399d7e50367" />

## MCP Host
### Stack
[![Python](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=fff)](#)
[![LangChain](https://img.shields.io/badge/LangChain-1c3c3c.svg?logo=langchain&logoColor=white)](#)
[![Ollama](https://img.shields.io/badge/Ollama-fff?logo=ollama&logoColor=000)](#)

### Presentation
The MCP Host is responsible for retrieving user's data from the MCP Server through a SSE (Server-Sent Events) connection and processing user queries.

It uses a multi-agent approach using LangChain, where different agents are responsible for different aspects of the planning process (__**calendar_specialist**__ agent, __**tasks_specialist**__ agent). Each agent can call specific tools exposed by the MCP server to retrieve the necessary data and use that data to generate responses for the user. \
The orchestrator agent is responsible for coordinating the interactions between the specialist agents and ensuring that the user's query is addressed comprehensively. It can also call directly some tools which are not handled by specialist agents (__**Notes tools**__).

LLM interactions are managed through Ollama, which runs the LLM locally to keep the data private and secure. The MCP Host is designed to be modular and extensible, allowing for easy addition of new agents and tools as needed.

## MCP Server
### Stack
[![Python](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=fff)](#)
[![FastMCP](https://img.shields.io/badge/FastMCP-009688?logo=fastapi&logoColor=fff)](#)
[![macOS osascript](https://img.shields.io/badge/AppleScript-000000?logo=apple&logoColor=F0F0F0)](#)

### Presentation
The MCP server is designed to work on macOS. It exposes tools for retrieving calendar events, tasks, and notes data.
It uses AppleScript to interact with native macOS applications like _Calendar_, _Reminders_ and _Notes_ to fetch data.

The server is built using FastMCP, which allows it to handle multiple requests concurrently and efficiently.

The server listens for incoming requests on a specified port on the localhost and responds with the requested data in a format that can be easily consumed by the MCP Host.

## Get started
### Prerequisites
- Work on macOS (for the MCP Server)
- Python 3.10 or higher
- Ollama installed and set up with a local LLM (e.g., `ollama pull llama3`)
### Installation
1. Clone the repository
2. Create a virtual environment and activate it:
   ```bash
   python -m venv mcp-env
   source mcp-env/bin/activate
   ```
3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Set your environment variables in a `.env` file in the `/host` directory of the project (follow the `.env.example` file as a template):
   ```
   MCP_SERVER_URL=http://127.0.0.1:8000/sse
   DEBUG=false
   LOG=true
   MODEL_NAME="model_name_here"
   TEMPERATURE=0.2 # Lower temperature for more reliable tool usage
   NUM_PREDICT=512 # Limit response length
   ```
5. Navigate to the `server/` directory and start the MCP Server:
   ```bash
   cd server
   python3 server.py
   ```
6. Navigate to the `host/` directory and start the MCP Host:
   ```bash
   cd host
   python3 host.py
   ```
6. You can now interact with the assistant through the command line interface. Type your query and the assistant will respond with a plan for your day based on your calendar events, tasks, and notes.

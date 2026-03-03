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
The MCP Host is responsible for handling the communication with the MCP Server (providing tools for retrieving calendar and tasks data) and processing user queries.
It uses a multi-agent approach using LangChain, where different agents are responsible for different aspects of the planning process (__**calendar_specialist**__ agent, __**tasks_specialist**__ agent). Each agent can call specific tools to retrieve the necessary data from the MCP Server and use that data to generate responses for the user. The orchestrator agent is responsible for coordinating the interactions between the specialist agents and ensuring that the user's query is addressed comprehensively. It can also call directly some tools which are not handled by specialist agents (__**Notes tools**__).
LLM interactions are managed through Ollama, which runs the LLM locally to keep the data private and secure. The MCP Host is designed to be modular and extensible, allowing for easy addition of new agents and tools as needed.

## MCP Server
### Stack
[![Python](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=fff)](#)
[![FastMCP](https://img.shields.io/badge/FastMCP-009688?logo=fastapi&logoColor=fff)](#)
[![AppleScript](https://img.shields.io/badge/AppleScript-000000?logo=applescript&logoColor=fff)](#)

### Presentation
The MCP server is designed to work on macOS. It exposes tools for retrieving calendar events, tasks, and notes data.
It uses AppleScript to interact with native macOS applications like Calendar, Reminders and Notes to fetch the required data.

The server is built using FastMCP, which allows it to handle multiple requests concurrently and efficiently.

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
4. Edit the `config.py` file to set the necessary configuration values.
5. Naviguate to the `host` directory and start the MCP Host (MCP Server is lauched automatically as a subprocess by the host):
   ```bash
   cd host
   python3 host.py
   ```
6. You can now interact with the assistant through the command line interface. Type your query and the assistant will respond with a plan for your day based on your calendar events, tasks, and notes.
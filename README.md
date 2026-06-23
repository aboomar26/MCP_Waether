# MCP LangChain Weather Agent

A simple weather MCP server connected to a LangGraph agent. The agent calls the `weather` tool to fetch live weather for any city.

## Setup

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Create a `.env` file in the project root:

```env
OPENROUTER_API_KEY=your_api_key_here
```

## Usage

Start the MCP server (runs on `http://127.0.0.1:8000`):

```bash
python weatherserver.py
```

In a second terminal, run the agent client:

```bash
python client.py
```

The client connects to the weather MCP server, loads the `weather` tool, and asks the LLM about the weather.

## Files

| File | Description |
|------|-------------|
| `weatherserver.py` | MCP server with a `weather` tool (geocoding + Open-Meteo API) |
| `client.py` | LangGraph agent that uses the MCP weather tool |
| `requirements.txt` | Python dependencies |

## How it works

1. User asks a question like "what's the weather in Tokyo?"
2. The agent calls the `weather` MCP tool
3. The server geocodes the city name and fetches current weather from [Open-Meteo](https://open-meteo.com/)
4. The agent returns the result to the user

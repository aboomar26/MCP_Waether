from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import asyncio
import os

load_dotenv()

async def main():

    client = MultiServerMCPClient(
        {

            "weather": {
                "url": "http://127.0.0.1:8000/mcp",
                "transport": "streamable-http",
            },
        }
    )

    tools = await client.get_tools()

    model = ChatOpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=os.getenv("OPENROUTER_API_KEY"),
        model="cohere/north-mini-code:free",
    )

    agent = create_react_agent(model, tools)


    weather = await agent.ainvoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": "what's the weather in cairo egypt ?",
                }
            ]
        }
    )
    print(weather["messages"][-1].content)


asyncio.run(main())
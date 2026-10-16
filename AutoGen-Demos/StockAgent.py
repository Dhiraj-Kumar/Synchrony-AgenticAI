from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient
from dotenv import load_dotenv
import asyncio
import requests

load_dotenv()

model = OpenAIChatCompletionClient (
    model="gpt-4o-mini"
)

def call_stock_api(symbol: str):
    """
    Gets the stock data from online API based on stock symbol
    """
    result = requests.get(f'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey=XSY1XDQ5NTY1THUW')
    return result.json()

agent = AssistantAgent(
    name="assistant", 
    model_client=model,
    tools=[call_stock_api],
    system_message="""
    You are a Stock market agent who fetches the data from an online stock market api using tools and present the information in more readable and presentable format.
    """,
    reflect_on_tool_use=True
)

async def main():
    while True:
        user_input = input("You: ")
        if user_input=="exit":
            break
        result = await agent.run(task=user_input)
        print(f"AI: {result.messages[-1].content}")

asyncio.run(main())
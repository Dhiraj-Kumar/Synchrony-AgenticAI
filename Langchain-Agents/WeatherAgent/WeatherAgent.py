from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
from langchain.tools import tool
from langgraph.checkpoint.memory import InMemorySaver
from dotenv import load_dotenv
import requests
import os

load_dotenv()

llm = ChatOpenAI(model="gpt-4o-mini")

@tool
def getWeatherInfo(city: str):
    """
    Get the current weather information for a city using openweathermap api
    """
    response = requests.get('https://api.openweathermap.org/data/2.5/weather', {
        "q": city,
        "appid": os.getenv("WEATHER_API_KEY"),
        "units": "metric"
    })
    if response.status_code!=200:
        return "Unable to fetch data from API"
    return response.json()

agent = create_agent(
    model=llm,
    system_prompt=""""
    You are a helful AI weather agent who answers queries about current weather. While answering the questions add a bit of humour and use emojis. Keep your tone professional and answer the questions based on actual facts and do not make up things.
    """,
    checkpointer=InMemorySaver(),
    tools=[getWeatherInfo]
)

while True:
    user_input = input("You: ")
    if user_input.lower()=="exit":
        break
    response = agent.invoke({
        "messages": [
            {"role":"user", "content": user_input}
        ]
    }, {"configurable": {"thread_id": "thread1"}})
    print(f"AI: {response['messages'][-1].content}")
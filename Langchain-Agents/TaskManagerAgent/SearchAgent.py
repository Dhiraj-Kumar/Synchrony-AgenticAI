from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
from langgraph.checkpoint.memory import InMemorySaver
from langchain_tavily import TavilySearch
from dotenv import load_dotenv

load_dotenv()

llm = ChatOpenAI(model="gpt-4o-mini")

tavily_tool = TavilySearch(
    max_results=5,
    topic="general"
)

agent = create_agent(
    model=llm,
    system_prompt=""""
    You are a helpful AI assistant who answers queries of the user with professional tone. you use tools to gather latest information from the internet.
    """,
    checkpointer=InMemorySaver(),
    tools=[tavily_tool]
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
    print(response["messages"][-1].content)
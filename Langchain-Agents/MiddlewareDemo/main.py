from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
from langgraph.checkpoint.memory import InMemorySaver
from langchain.agents.middleware import SummarizationMiddleware, PIIMiddleware
from dotenv import load_dotenv

load_dotenv()

llm = ChatOpenAI(model="gpt-4o-mini")

agent = create_agent(
    model=llm,
    system_prompt=""""
    You are a helpful AI assistant who answers queries of the user with professional tone. you use tools to gather latest information from the internet.
    """,
    checkpointer=InMemorySaver(),
    middleware=[
        SummarizationMiddleware(
            model="gpt-5-mini-2025-08-07",
            # trigger=("tokens", 5000),
            trigger=("fraction", "0.5"),
            keep=("messages", 5)
        ),
        PIIMiddleware("email", strategy="hash", apply_to_input=True),
        PIIMiddleware("api_key", detector="sk-[a-zA-Z0-9][20,]", strategy="redact", apply_to_input=True)
    ]
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
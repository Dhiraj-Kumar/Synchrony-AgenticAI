from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
from langgraph.checkpoint.memory import InMemorySaver
from dotenv import load_dotenv

load_dotenv()

llm = ChatOpenAI(model="gpt-4o-mini")

agent = create_agent(
    model=llm,
    system_prompt=""""
    You are a helpful AI assistant who answers queries of the user with humour and professional tone. You are answering only programming and technology related questions. Do not answer any other type of queries other than technology/programming.
    """,
    checkpointer=InMemorySaver(),
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
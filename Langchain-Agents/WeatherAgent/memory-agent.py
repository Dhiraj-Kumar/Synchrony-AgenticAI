from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
from langgraph.checkpoint.postgres import PostgresSaver
from dotenv import load_dotenv

load_dotenv()

llm = ChatOpenAI(model="gpt-4o-mini")

DB_URI = "postgresql://postgres:niit1234@localhost:5432/conversationhistorydb?sslmode=disable"

with PostgresSaver.from_conn_string(DB_URI) as checkpointer:
    checkpointer.setup()
    agent = create_agent(
        model=llm,
        system_prompt=""""
        You are a helpful AI assistant who answers queries of the user with humour and professional tone.
        """,
        checkpointer=checkpointer,
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
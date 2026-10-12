from langchain_openai import ChatOpenAI
from langchain.messages import HumanMessage, SystemMessage, AIMessage
from dotenv import load_dotenv

load_dotenv()

model = ChatOpenAI(
    model = "gpt-4o-mini",
)

conversation_history=[
    SystemMessage(content="""
    You are an AI assistant who answers queries with a bit of humour. Use emojis to make your responses beautiful. Keep your tone professional. Answer questions only related to programming languages. Do not respond to any questions other than programming and refuse politely.
    """)
]

while True:
    user_input = input("You: ")
    if user_input.lower()=="exit":
        break
    conversation_history.append(HumanMessage(content=user_input)) # Appending user message
    response = model.invoke(conversation_history)
    conversation_history.append(AIMessage(content=response.content)) # Appending AI message
    print(f"AI: {response.content}")

print(conversation_history)

from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

model = ChatOpenAI(
    model = "gpt-4o-mini",
)

conversation_history=[]

while True:
    user_input = input("You: ")
    if user_input.lower()=="exit":
        break
    conversation_history.append(user_input) # Appending user message
    # response = model.invoke(conversation_history)

    response=""
    for chunk in model.stream(conversation_history):
        response=response+chunk.content
        print(chunk.content, end="", flush=True)
    conversation_history.append(response) # Appending AI message
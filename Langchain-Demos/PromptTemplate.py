from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv

load_dotenv()

model = ChatOpenAI(model="gpt-4o-mini")

template = PromptTemplate(template="Write an article on the topic of {topic}", input_variables=["topic"])

prompt = template.invoke({"topic": "AI"})

# print(prompt)

response = model.invoke(prompt)

print(response.content)
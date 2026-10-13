from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv

load_dotenv()

model = ChatOpenAI(model="gpt-4o-mini")

template = PromptTemplate(template="Write an article on the topic of {topic}", input_variables=["topic"], validate_template=True)

template2 = PromptTemplate(template="Generate 5 MCQ type questions with answers based on the below article.\n Article: {article}", input_variables=["article"], validate_template=True)

chain = template | model | StrOutputParser() | template2 | model | StrOutputParser() #LCEL

print(chain.invoke({"topic": "Cyber Security"}))
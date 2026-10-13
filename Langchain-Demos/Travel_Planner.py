from langchain_openai import ChatOpenAI
from langchain_core.prompts import load_prompt
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv

load_dotenv()

model = ChatOpenAI(model="gpt-4o-mini")

prompt = load_prompt("travel_planner_prompt.json")

chain = prompt | model | StrOutputParser()

print(chain.invoke({'username': 'Dhiraj', 'destination': 'Singapore', 'start_date':'25-01-2026', 'end_date':'30-01-2026','interests':'Adventure','travel_style':'Solo','dietary_preferences':'Non-Vegetarian', 'budget': '100000'}))
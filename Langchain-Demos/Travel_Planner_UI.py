from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from langchain_core.prompts import load_prompt
from langchain_core.output_parsers import StrOutputParser
import streamlit as st

load_dotenv()

st.header("Travel Planner")
username = st.text_input("Name")
destination = st.text_input("Destination")
start_date = st.date_input("Start Date")
end_date = st.date_input("End Date")
budget = st.slider("Select Budget", 100000, 1000000)
interests = st.multiselect("Interests", ["Adventure", "Beaches", "Nature", "Shopping"])
travel_style = st.selectbox("Travel Style", ["Solo", "Group", "Family"])
dietary_preferences = st.selectbox("Dietary Preferences", ["Vegetarian", "Non-Vegetarian", "Vegan"])

model = ChatOpenAI(model="gpt-4o-mini")
prompt = load_prompt("travel_planner_prompt.json")
chain = prompt | model | StrOutputParser()

if st.button("Submit"):
    st.write_stream(chain.stream({'username': username, 'destination': destination, 'start_date':start_date, 'end_date':end_date,'interests':interests,'travel_style':travel_style,'dietary_preferences':dietary_preferences, 'budget': budget}))
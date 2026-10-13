from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser, PydanticOutputParser
from langchain_core.runnables import RunnableBranch
from typing import Literal
from dotenv import load_dotenv

load_dotenv()

llm = ChatOpenAI(model="gpt-4o-mini")

class Feedback(BaseModel):
    participant_name: str = Field(description="Name of the participant")
    summary: str = Field(description="Brief summary of the overall feedback")
    sentiment: Literal['positive', 'negative']=Field(description="Sentiment of the feedback like positive or negative")
    highlights: list[str]=Field(description="List of positive highlights of the program described by the participants")
    lowlights: list[str]=Field(description="List of negative highlights of the program described by the participants")
    rating: int=Field(description="Rating of the program")
    email_address: str=Field(description="Email address of the participant")

pyparser = PydanticOutputParser(pydantic_object=Feedback)

prompt = PromptTemplate(
    template="Analyze the sentiment of the following feedback and classify it into positive or negative \n {feedback} \n {format_instructions}",
    input_variables=["feeedback", "format_instructions"],
    partial_variables={'format_instructions': pyparser.get_format_instructions()}
)

chain = prompt | llm | pyparser

positive_email_template = PromptTemplate(
    template="Write a thank you email to the participant for giving positive feedback about the recent training program the participant attended \n {feedback}", input_variables=["feedback"]
)

negative_email_template = PromptTemplate(
    template="Write an apology email to the participant for giving negative feedback about the recent training program the participant attended \n {feedback}", input_variables=["feedback"]
)

branch_chain = RunnableBranch(
    (lambda x: x.sentiment == "positive", positive_email_template | llm | StrOutputParser()),
    (lambda x: x.sentiment == "negative", negative_email_template | llm | StrOutputParser()),
    (lambda x: "Not able to analyze the sentiment")
)

main = chain | branch_chain


# response = main.invoke("""
# The Java Fullstack training program was well-structured and covered essential modules like Core Java, Spring Boot, Hibernate, and Angular. The hands-on projects and live coding sessions made it easier to apply concepts in real-world scenarios. The trainer was knowledgeable and supportive, and the sessions on Git and deployment provided a complete view of end-to-end development. However, the pace during the Spring Boot section felt a bit fast, and more time for practice would have been helpful. Additionally, a dedicated session on debugging and code optimization could enhance the learning experience. Some front-end sessions, especially on Angular, felt rushed, and could benefit from more real-time examples. Out of 5 I would give 4 rating for this program. Feedback given by Dhiraj Kumar
# """)

response = main.invoke("""
The Java Fullstack training program did not fully meet my expectations. Although the program covered important technologies such as Core Java, Spring Boot, Hibernate, and Angular, the overall delivery lacked sufficient depth and practical implementation. Several topics, particularly Spring Boot and Angular, were covered too quickly, making it difficult to understand and apply the concepts effectively. The hands-on exercises and live coding sessions were limited and did not provide enough opportunities to work on realistic, end-to-end application scenarios. The program also lacked adequate coverage of important areas such as debugging, code optimization, troubleshooting, testing, and industry best practices. More structured practical assignments, real-world examples, and dedicated time for resolving participant queries would have significantly improved the learning experience. Overall, the training needs considerable improvement in terms of pacing, practical exposure, topic depth, and alignment with real-world development practices. Rating: 2 out of 5 Feedback given by Dhiraj Kumar
""")

print(response)

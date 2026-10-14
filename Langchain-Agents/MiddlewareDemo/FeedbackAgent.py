from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
from langgraph.checkpoint.memory import InMemorySaver
from pydantic import BaseModel, Field
from langchain.tools import tool
from langchain.agents.middleware import HumanInTheLoopMiddleware
from typing import Literal
from langgraph.types import Command
import os
import resend
from dotenv import load_dotenv

load_dotenv()

llm = ChatOpenAI(model="gpt-4o-mini")

class Feedback(BaseModel):
    participant_name: str = Field(description="Name of the participant")
    summary: str = Field(description="Brief summary of the overall feedback")
    sentiment: Literal['positive', 'negative'] = Field(description="Sentiment of the feedback like positive or negative")
    highlights: list[str]=Field(description="List of positive highlights of the program described by the participant")
    lowlights: list[str]=Field(description="List of negative highlights of the program described by the participant")
    rating: int = Field(description="Rating of the program")
    email_address: str = Field("Email address of the participant")
    status: str = Field(description="Status of the email")

@tool
def send_email(email_address: str, body: str):
    """
    Tool for sending an email using resend api
    """
    resend.api_key=os.getenv("RESEND_API_KEY")
    params = resend.Emails.SendParams = {
        "from": "training@resend.dev",
        "to": [email_address],
        "subject": "Reply from Training Manager",
        "html": body
    }
    email = resend.Emails.send(params)
    return email

agent = create_agent(
    model=llm,
    system_prompt="""
    You are an AI assistant who analyze the customer feedback and draft an email to customer based on feedback sentiment. If sentiment is positive, you draft a thank you email and if sentiment is negative you draft an apology email. You use tool to send email. Use html format to draft an email.
    """,
    response_format=Feedback,
    checkpointer=InMemorySaver(),
    tools=[send_email],
    middleware=[
        HumanInTheLoopMiddleware(
            interrupt_on={
                "send_email": {
                    "allowed_decisions": ["approve", "reject"]
                }
            }
        )
    ]
)

result = agent.invoke(
    {
        "messages": [
            {"role": "user", "content": "The Java Fullstack training program did not meet expectations. Although it covered key technologies like Core Java, Spring Boot, Hibernate, and Angular, several sections were rushed—especially Spring Boot and Angular—leaving little time for hands-on practice. The lack of dedicated sessions on debugging and code optimization further reduced the program’s effectiveness. While the trainer was knowledgeable, the pace and structure limited meaningful learning and real-world application. Overall, the program requires better pacing and more practical focus. I would rate it 2 out of 5. Feedback given by Dhiraj Kumar. Email address - dhiraj2001@gmail.com"}
        ]
    }, {"configurable": {"thread_id": "thread1"}}
)

if "__interrupt__" in result:
    print("Workflow paused.... Waiting for approval")
    print("1. Approve \n 2. Reject")
    user_input= input("Enter your choice")
    choices = {"1":"approve", "2": "reject"}
    result = agent.invoke(
        Command(
            resume={
                "decisions": [
                    {"type": choices.get(user_input)}
                ]
            }
        ), {"configurable": {"thread_id": "thread1"}}
    )

    print(f"Result: {result['messages'][-1].content}")

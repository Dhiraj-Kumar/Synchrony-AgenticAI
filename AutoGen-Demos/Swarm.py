from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_agentchat.teams import Swarm
from autogen_agentchat.conditions import TextMentionTermination
from autogen_agentchat.ui import Console
from dotenv import load_dotenv
import asyncio

load_dotenv()

model_client = OpenAIChatCompletionClient(
    model="gpt-4o-mini"
)

designer = AssistantAgent(
    name="designer",
    model_client=model_client,
    system_message="""
    You are a Senior Graphic Designer.
    - You describe layout, color theory and visual branding.
    - If you need text for a layout, hand off to copywriter
    - When your design concept is ready, hand off back to the project_manager
    """,
    handoffs=["copywriter", "project_manager"]
)

copywriter = AssistantAgent(
    name="copywriter",
    model_client=model_client,
    handoffs=["designer", "project_manager"],
    system_message="""
    You are an expert copywriter.
    - You write punchy, persuasive text and headlines.
    - If you need any visual description to match your tone, hand off to the designer.
    - Once the copy is drafted, hand off back to project_manager
    """
)

project_manager = AssistantAgent(
    name="project_manager",
    model_client=model_client,
    handoffs=["designer", "copywriter"],
    system_message="""
    You are the Project Manager.
    - You gather the client's requierments for marketing campaigns.
    - Transfer to 'designer' for visual requests or 'copywriter' for text requests.
    - When both visuals and copy are finalised, say 'CAMPAIGN_READY'
    """
)

team = Swarm(
    participants=[project_manager, designer, copywriter],
    termination_condition=TextMentionTermination("CAMPAIGN_READY")
)

async def main():
    await Console(team.run_stream(task="I need a landing page for a new eo friendly water bottle. It needs a minimalist design and bold headline"))

asyncio.run(main())
from autogen_agentchat.agents import AssistantAgent, CodeExecutorAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_ext.code_executors.local import LocalCommandLineCodeExecutor
from autogen_agentchat.ui import Console
from dotenv import load_dotenv
import asyncio
import os

load_dotenv()

model_client = OpenAIChatCompletionClient(
    model="gpt-4o-mini"
)

workspace_path = os.path.abspath("demo_workspace")

executor = LocalCommandLineCodeExecutor(work_dir=workspace_path)

executor_agent = CodeExecutorAgent(
    name="executor",
    code_executor=executor
)

coder = AssistantAgent(
    name="coder",
    model_client=model_client,
    system_message=f"""
    You are a Python Expert.
    Your workspace is {workspace_path}.
    1. Always write code in 'python' markdown blocks.
    2. When creating data, explicitly save it to a file (CSV, TXT etc.)
    3. If the executor returns an error, fix it.
    """,
)

team = RoundRobinGroupChat(
    participants=[coder, executor_agent],
    max_turns=3
)

async def main():
    await Console(team.run_stream(task="Create a CSV file named products.csv with 10 rows of dummy data with columns- id, name, brand, quantity, price"))

asyncio.run(main())
from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
from langchain.tools import tool
from dotenv import load_dotenv
from langgraph.checkpoint.memory import InMemorySaver
import sqlite3
from datetime import date

load_dotenv()

llm = ChatOpenAI(model="gpt-4o-mini")

con = sqlite3.connect("tasks.db", check_same_thread=False)
cursor = con.cursor()

cursor.execute("""
Create table if not exists todos (
id integer primary key autoincrement,
todo text not null,
iscompleted boolean not null
)
""")

con.commit()

@tool
def add_todo(todo: str):
    """
    Add a new todo in todos table in database
    """
    cursor.execute("insert into todos (todo, iscompleted) values (?,?)", (todo, False))
    con.commit()


@tool
def get_all_todos():
    """
    Get all todos from todos table
    """
    cursor.execute("Select id, todo, iscompleted from todos order by id")
    return cursor.fetchall()

@tool
def get_todo_by_id(todo_id: str):
    """
    Get todo item from todos table based on todo_id
    """
    cursor.execute("Select id, todo, iscompleted from todos where id=?", (todo_id,))
    return cursor.fetchall()

@tool
def delete_todo(todo_id: str):
    """
    Delete a todo from todos table based on todo_id
    """
    cursor.execute("Delete from todos where id=?", (todo_id,))
    con.commit()

@tool
def update_todo(status: bool, todo_id: str):
    """
    Updates the iscompleted status of the todo in todos table based on todo_id
    """
    cursor.execute("Update todos set iscompleted=? where id=?", (status, todo_id))
    con.commit()

agent = create_agent(
    model=llm,
    system_prompt=f"""
    You are an AI todo assistant who helps in managing tasks for the user. You call tools to perform different actions. You are strictly managing the todos and do not answer queries related to anything else. For adding tasks it is important for you to know the current date of the system. Today's date is - {date.today()}. Do not take any task for past dates. If user is specifying the past date politely reject the request.
    """,
    checkpointer=InMemorySaver(),
    tools=[get_all_todos, get_todo_by_id, add_todo, update_todo, delete_todo]
)

while True:
    user_input = input("You: ")
    if user_input.lower()=="exit":
        break
    response = agent.invoke({
        "messages": [
            {"role": "user", "content": user_input}
        ]
    }, {"configurable": {"thread_id": "thread1"}})
    print(f"AI: {response['messages'][-1].content}")
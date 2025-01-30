"""Database Agent."""

# import sqlite3
# from typing import Any

from langchain import hub
from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit
from langchain_community.utilities.sql_database import SQLDatabase

# from langchain_core.messages import HumanMessage
from langchain_ollama import ChatOllama
from langgraph.prebuilt import create_react_agent
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.pool import StaticPool

model = ChatOllama(model="llama3-groq-tool-use:8b")

# "llama3-groq-tool-use:8b"
MODEL_TO_USE_DICT = {
    "provider": "groq",
    "model": ""
}

def get_llm_model(model_dict=MODEL_TO_USE_DICT):
    if model_name == "groq":
        from langchain_groq import ChatGroq
        model = ChatGroq(model=model_dict["name"])
    else:
        from langchain_ollama import ChatOllama
        model = ChatOllama(model=model_dict["name"])
    return model

def get_engine_power_plant() -> Engine:
    """Engine for opsd data."""
    return create_engine(
        "sqlite:////home/richhiey/Desktop/code/genai_db_poc/GenAI_data/GenAI_data/conventional_power_plants/conventional_power_plants.sqlite",
        poolclass=StaticPool,
    )

engine = get_engine_power_plant()
db = SQLDatabase(engine)
toolkit = SQLDatabaseToolkit(db=db, llm=model)
tools = toolkit.get_tools()

prompt_template = hub.pull("langchain-ai/sql-agent-system-prompt")
system_message = prompt_template.format(dialect="SQLite", top_k=10)

db_agent = create_react_agent(model, tools, state_modifier=system_message)

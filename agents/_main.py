from langchain.chat_models import ChatOpenAI
from langchain.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    MessagesPlaceholder,
)
from langchain.schema import SystemMessage
from langchain.agents import OpenAIFunctionsAgent, AgentExecutor
from dotenv import load_dotenv

from tools.sql import run_query_tool, list_tables, describe_table_tool
from tools.report import write_report_tool

load_dotenv()

chat = ChatOpenAI()

tables = list_tables()
# print(tables)
prompt = ChatPromptTemplate(
    messages=[
        SystemMessage(
            content=(
                "You are an AI that has access to a SQLite databases.\n"
                f"The database has tables of : {tables}\n"
                "Do not make any assumptions about tables exists or"
                "or what columns exists. Instead, use the 'describe_tables' function"
            )
        ),
        HumanMessagePromptTemplate.from_template("{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ],
)

tools = [run_query_tool, describe_table_tool, write_report_tool]

agent = OpenAIFunctionsAgent(llm=chat, prompt=prompt, tools=tools)

agent_executor = AgentExecutor(agent=agent, verbose=True, tools=tools)

# agent_executor("How many users are in the databases?")
# agent_executor("How many users have provided a shipping address?")
agent_executor(
    "Summarize the top 5 most popular products. Write the results to a report file."
)

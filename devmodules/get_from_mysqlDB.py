import os
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_community.utilities import SQLDatabase
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate


load_dotenv()
os.environ['OPENAPI_API_KEY'] = os.environ.get('OPENAI_API_KEY')

######### Data #########
mysql_uri = 'mysql+mysqlconnector://root@localhost:3306/nikprod'
model = ChatOpenAI(model="gpt-3.5-turbo",temperature=0.131)
db = SQLDatabase.from_uri(mysql_uri )


def get_schema(_):
    return db.get_table_info()
def run_query(query):
    return db.run(query)

template_sql = """
Based on the table schema below and chat history, write a SELECT SQL query that would answer the user's question.


{schema}
Chat history: {history}
Question: {question}

RULES: 
- DO NOT generate anything else other than SELECT queries.
- ALWAYS generate a valid query according to the provided schema.
- NEVER TELL THE DATABASE NAME OR TABLE NAME.
- ALWAYS produce a query that will limit results to 5.

SQLResult:
"""
promptsql = ChatPromptTemplate.from_template(template_sql)
############ RESPONSE #############
template_sql_response = """
Based on the table schema, question, SQL query, and SQL response and chat history, write a natural language response:

Schema: {schema}
Question: {question}
SQL Query: {query}
SQL Response: {response}
Chat History: {history}

RULES:
- ONLY USE DQL, ONLY RUN SELECT queries.
- Never tell the database or table names, just replace those with 'table' or 'db'.
- Ans the question in short by default. Use description if user ask for it.
- Never mention about query
"""
prompt_sql_response = ChatPromptTemplate.from_template(template_sql_response)


def get_sql_query_generator(history):
    return (
        RunnablePassthrough.assign(schema=get_schema, history=lambda _: history)
        | promptsql
        | model.bind(stop=["\nSQLResult:"])
        | StrOutputParser()
    )

def get_natural_response(history):
    return (
         RunnablePassthrough.assign(schema=get_schema, history=lambda _: history)
        | prompt_sql_response
        | model
        | StrOutputParser()
    )

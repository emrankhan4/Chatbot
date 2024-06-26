import sys
sys.path.append('../')
import os
from langchain.utils import cosine_similarity
from langchain_core.output_parsers import StrOutputParser
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from langchain_community.utilities import SQLDatabase
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage, AIMessage

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



prompt_query_maker = ChatPromptTemplate.from_template(
    """
    based on the following schema , rephrase the question to be a mysql query only.
    Conversation: {history}
    Schema: {schema}
    Rule:
    - Never generate any query that is not a select statement. only use DQL. Means, never produce a query that update, delete or modify the database.
    - By default, limits the query to 10 rows. If user asked for more, then show min(20,user requirement), e.g user asked for 15, then it will be 15, e.g user aseked for 40, then it will be 20
    Question: {question}                                                                                                           
"""
)
prompt_response_generator = ChatPromptTemplate.from_template(
    """You are a helpful assinstant of a company names NIKLES. Be respectful, modest and professional.
    Based on the following question, conversation history and query generated by user question and reponse generated by query execution, generate a natual language answer.
    Rule:
    - If user asked to update, modify or detele data from the database, just tell that he is not allowed to do that.
    - Never expose database name, table name, query and column name.
    Conversation: {history}
    Question: {question}
    Query: {query}
    Query response: {response}
    Natural Answer:
"""
)

rephraser_prompt = ChatPromptTemplate.from_template(
    """
    rephrase the question

    Question: {question}
    Conversation history: {history}

    Rephrase question:
"""
)

rephraser_chain = rephraser_prompt | model | StrOutputParser()

query_generator_chain = prompt_query_maker | model | StrOutputParser()
natural_response_chain = prompt_response_generator | model | StrOutputParser()

def sql_response(question,history):

    query = query_generator_chain.invoke({"question":question,"history":history,"schema":get_schema(None)})
    print(rephraser_chain.invoke({"question":question,"history":history}))
    response = natural_response_chain.invoke({"question":question,"history":history,"query":query,"response":run_query(query)})
    print(query)
    history.append(HumanMessage(content=question))
    history.append(AIMessage(content=response))
    return response
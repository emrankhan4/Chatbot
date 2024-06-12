import os
from langchain.utils import cosine_similarity
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from operator import itemgetter
from pydantic import BaseModel
from langchain_core.prompts import ChatPromptTemplate
from devmodules.get_from_chromaDB import *
from devmodules.get_from_mysqlDB import *
# get_general_chat_chain = get_from_chromaDB.get_general_chat_chain

load_dotenv()
os.environ['OPENAPI_API_KEY'] = os.environ.get('OPENAI_API_KEY')


class User(BaseModel):
    user: str

class ChatHistory:
    def __init__(self):
        self.history = []

    def add_message(self, role, message):
        # self.history.append({"role": role, "message": message})
        if role.lower()=='ai':
            self.history.append({f"AI: {message}"})
        else:
            
            self.history.append({f"USER: {message}"})
    def get_history(self):
        return self.history



history = ChatHistory()


classification_template = PromptTemplate.from_template(
    """
    Given the user question below, classify the question as either begin about "Database" or "Chat".
    
    <If the question is like these sample than its a 'Database' question>
    SAMPLE:
    Can you list all the products available in the database?"
    "What is the price of the product with ID 123?"
    "How many products are available"
    "How many units of the product named 'Shower Head Model X' are in stock?"
    "Show me the details of the product with the SKU 'ABCD1234'."
    "Which products were added to the database in the last month?"]
    "How many different types of shower heads do we have?"
    "Can you fetch the product names and prices for all products in the 'Premium' category?"
    "What are the dimensions of the 'Eco Shower System'?"
    "How many reviews does the product 'Rain Shower XL' have?"
    "What is the average rating of the product 'Eco-Friendly Shower'?"
    "How many products are currently out of stock?"
    "List all the products that are on sale."
    "What are the specifications of the product with ID 456?"
    "Which products have a discount greater than 20%?"
    "What are the top 5 best-selling products?"
    "How many products are there in the 'Luxury' category?"
    "Fetch the supplier details for the product 'High-Pressure Shower Head'."
    "What is the reorder level for the product 'Compact Shower System'?"
    "List all the products with a 5-star rating."
    "Show me all products that were discontinued last year."
    "What is the manufacturing date of the product with SKU 'EFG5678'?"
    "Can you provide a summary of the latest product additions to the database?"
    "What are the shipping details for the product 'Dual Shower System'?"
    "List all products that have received customer complaints."
    "What is the return policy for the product 'Adjustable Shower Arm'?"
    "How many products are supplied by 'Nikles Manufacturing'?"
    "Fetch the inventory levels for all products in the 'Economy' range."
    "What are the dimensions and weight of the 'Ultra-Thin Shower Head'?"
    "How many units of 'Deluxe Shower Kit' were sold last month?"
    "What is the customer feedback for the product 'Thermostatic Shower Mixer'?"
    "List all products that require special installation services."
    "What is the lead time for the product 'Handheld Shower Wand'?"
    "Can you show the sales trends for the product 'Luxury Rain Shower' over the past year?"
    <If the question is about warrenty or Nikles company products or other, then its a 'Chat' topic>
    
    <question>
    {question}
    Classification:
    </question>

    Classification:"""
)

#### rephraser####
template_rephrase = """
Based on the chat history and schema below , rephrase the user's question to provide more context and clarity:

Chat history: {history}
Schema: {schema}
Original Question: {question}
Rephrased Question:
"""
prompt_rephrase = ChatPromptTemplate.from_template(template_rephrase)

def get_rephrased_question_chain(history):
    return (
        RunnablePassthrough.assign(
            history=lambda _: history,
            schema=get_schema,
            question=itemgetter("question")
        )
        | prompt_rephrase
        | model
        | StrOutputParser()
    )
classification_chain = classification_template | ChatOpenAI() | StrOutputParser()

def Ai_response(user_question):
    # rephraser = get_general_chat_chain(history)
    rephrased_question = user_question;
    x_class = classification_chain.invoke({"question":rephrased_question})
    x_class=str(x_class)
    
    print(x_class)
    print("Rephrased question: ",rephrased_question)
    print(history.history)


    if x_class.lower() == 'database':
        sql_gen=get_sql_query_generator(history)
        natual_response_gen=get_natural_response(history)
        sql_query = sql_gen.invoke({"question":rephrased_question})
        sql_response = run_query(sql_query)
        ai_response = natual_response_gen.invoke({ "question": rephrased_question, "query": sql_query,"response":sql_response}) 
    else:
        gen_chat = get_general_chat_chain(history)
        ai_response = gen_chat.invoke({'question': user_question})
        
    history.add_message('AI', ai_response)
    history.add_message('USER', user_question)
    
    

    return ai_response
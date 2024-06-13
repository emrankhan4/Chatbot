import sys
sys.path.append('../')
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
from get_from_mysqlDB import sql_response
from models.get_from_chromaDB_and_general_Chat import c_response
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage
# get_general_chat_chain = get_from_chromaDB.get_general_chat_chain

load_dotenv()
os.environ['OPENAPI_API_KEY'] = os.environ.get('OPENAI_API_KEY')


class User(BaseModel):
    user: str




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
rephraser_prompt = ChatPromptTemplate.from_template(
    """
    rephrase the question, NEVER CHANGE THE MEANING OF USER INPUT
    Rule:
    - it if it is like greetings like, 'hi', 'hello', or good by types sentence like "thats all" , "that all", "thank you", "thanks", "thank you so much", "thank you so much for your service", "thats all" then the rephrased question is will be as it is ( Do not change the question, keep that as it is).
    - Do not add any question mark at the end of the rephrased question
    - Your task is to rephrase the question, NEVER CHANGE THE MEANING OF USER INPUT
    Question: {question}
    Conversation history: {history}

    Rephrase question:
"""
)
model = ChatOpenAI(model="gpt-3.5-turbo",temperature=0.131)
rephraser_chain = rephraser_prompt | model | StrOutputParser()
classification_chain = classification_template | ChatOpenAI() | StrOutputParser()

history =[]
def Ai_response(user_question):
    # rephraser = get_general_chat_chain(history)
    rephrased_question = rephraser_chain.invoke({"question":user_question,"history":history})
  
    x_class = classification_chain.invoke({"question":rephrased_question})
    x_class=str(x_class)
    
    print("CLASS: ",x_class)
    print("Rephrased question: ",rephrased_question)
    

    if x_class.lower() == 'database':
        ai_response = sql_response(user_question,history)
    else:
        ai_response = c_response(rephrased_question)
        
    
    history.append(HumanMessage(content=rephrased_question))
    history.append(AIMessage(content=ai_response))

    while(len(history)//2 >= 3):
        history.pop(0)
        history.pop(0)

    return ai_response
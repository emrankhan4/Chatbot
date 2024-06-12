import os
from langchain.utils import cosine_similarity
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import OpenAIEmbeddings
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from langchain_chroma import Chroma
from dotenv import load_dotenv
from operator import itemgetter
from langchain_core.prompts import ChatPromptTemplate
# import sys
# sys.path.insert(1,'C://Users//BS01216//Desktop//battleGround//ML//NLP_//Chatbot//data//')


load_dotenv()
os.environ['OPENAPI_API_KEY'] = os.environ.get('OPENAI_API_KEY')
model = ChatOpenAI(model="gpt-3.5-turbo",temperature=0.131)
chroma_db = Chroma(persist_directory="chroma_db", embedding_function=OpenAIEmbeddings())
retriver = chroma_db.as_retriever()
# print(retriver.)



template_for_general_chat = """
Answer the question with in 50 words based only on the following context and chat history:
{context}
Question: {question}
Chat history: {history}
Rule:
- If your are asked "what is/was my last question?" then look at the chat history and the last User question is the answer
"""
prompt_for_general_chat = ChatPromptTemplate.from_template(template_for_general_chat)

def get_general_chat_chain(history):
    return (
        {
            "context": itemgetter("question") | retriver,
            "question": itemgetter("question"),
            "history": lambda _: history
        }
        | prompt_for_general_chat
        | model
        | StrOutputParser()
    )




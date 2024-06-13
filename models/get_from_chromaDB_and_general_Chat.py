import os
from langchain.utils import cosine_similarity
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import OpenAIEmbeddings
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from langchain_chroma import Chroma
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
# import sys
# sys.path.insert(1,'C://Users//BS01216//Desktop//battleGround//ML//NLP_//Chatbot//data//')


load_dotenv()
os.environ['OPENAPI_API_KEY'] = os.environ.get('OPENAI_API_KEY')
model = ChatOpenAI(model="gpt-3.5-turbo",temperature=0.131)
chroma_db = Chroma(persist_directory="chroma_db", embedding_function=OpenAIEmbeddings())
retriever = chroma_db.as_retriever()

template = """You are a helpful assinstant of a company names NIKLES. You are Nikky. Be respectful, modest and professional. Answer the question based only on the following context:

{context}
Question: {question}
Rule:
- If its greeting like Hello, hi, Good [morning/afternoon/evening], greet him and ask user if he wants to ask any further question
- This is the contact info: info@nikles.com , suggest this if you think its necessary
- Answer the question with no more than 30 words
- If user ask any good by sentece kind of like "thank you", "thanks", "thank you so much", "thank you so much for your service", "thats all", "ok bye" , "good bye" or any similar sentece then reply like "you are welcome", "Goodbye! We hope to see you again at Nikles soon.", We look forward to seeing you again at Nikles!", "Thanks for chatting with us! Until next time!"
"Have a great day! Feel free to reach out if you need more help." etc...
- If you are asked question out of context, answer "Can your provide more context please? Thanks"
Answer:
"""
prompt = ChatPromptTemplate.from_template(template)

chain = (
    {"context": retriever , "question": RunnablePassthrough()}
    | prompt
    | model
    | StrOutputParser()
)

def c_response(question):
    return chain.invoke(question)
from langchain_chroma import Chroma
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings


warrenty_loader = PyPDFLoader('../data/Warranty.pdf')
webdata_loader = PyPDFLoader('../data/informationFromWeb.pdf')

warrenty_pages = warrenty_loader.load_and_split()
web_pages = webdata_loader.load_and_split()

all_docs=warrenty_pages+web_pages


text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
splits = text_splitter.split_documents(all_docs)
vectorstore = Chroma.from_documents(documents=splits, embedding=OpenAIEmbeddings())

db2 = Chroma.from_documents(all_docs, OpenAIEmbeddings(), persist_directory="../chroma_db")
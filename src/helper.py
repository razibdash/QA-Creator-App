import os
from dotenv import load_dotenv
from langchain.document_loaders import PyPDFLoader
from langchain_groq import ChatGroq
from langchain.text_splitter import TokenTextSplitter
from langchain.prompts import PromptTemplate
from langchain.chains.summarize import load_summarize_chain
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain.docstore.document import Document
from src.prompt import *


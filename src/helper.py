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

# Load environment variables from .env file
load_dotenv()
# Set the GROQ API key from the environment variable
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
os.environ["GROQ_API_KEY"] = GROQ_API_KEY

def file_proessing(file_path):
    #load the PDF file
    loader = PyPDFLoader(file_path)
    data = loader.load()
    questions = ""
    for page in data:
        questions += page.page_content

    # Split the text into chunks
    splitter_gen_ques = TokenTextSplitter(
        chunk_size=10000,
          chunk_overlap=200
          )
    
    chunks_ques_gen = splitter_gen_ques.split_text(questions)

    document_ques_gen= [Document(page_content=chunk) for chunk in chunks_ques_gen]
    
    splitter_ans_gen= TokenTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )
    document_ans_gen = splitter_ans_gen.split_documents(document_ans_gen)

    return  document_ques_gen, document_ans_gen

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

def file_processing(file_path):
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




def llm_pipeline(file_path):

    document_ques_gen, document_answer_gen = file_processing(file_path)

    llm_ques_gen_pipeline = ChatGroq(
        temperature = 0.3,
        model="llama3-70b-8192",
        api_key= os.getenv("GROQ_API_KEY"),
    )

   

    PROMPT_QUESTIONS = PromptTemplate(template=prompt_template, input_variables=["text"])

    

    REFINE_PROMPT_QUESTIONS = PromptTemplate(
        input_variables=["existing_answer", "text"],
        template=refine_template,
    )

    ques_gen_chain = load_summarize_chain(llm = llm_ques_gen_pipeline, 
                                            chain_type = "refine", 
                                            verbose = True, 
                                            question_prompt=PROMPT_QUESTIONS, 
                                            refine_prompt=REFINE_PROMPT_QUESTIONS)

    ques = ques_gen_chain.run(document_ques_gen)

    embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

    vector_store = FAISS.from_documents(document_answer_gen, embeddings)

    llm_answer_gen = ChatGroq(
        temperature = 0.3,
        model="llama3-70b-8192",
        api_key= os.getenv("GROQ_API_KEY"),
    )

    ques_list = ques.split("\n")
    filtered_ques_list = [element for element in ques_list if element.endswith('?') or element.endswith('.')]

    answer_generation_chain = RetrievalQA.from_chain_type(llm=llm_answer_gen, 
                                                chain_type="stuff", 
                                                retriever=vector_store.as_retriever())

    return answer_generation_chain, filtered_ques_list
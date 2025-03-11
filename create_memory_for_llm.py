from langchain.document_loaders import PyMuPDFLoader,DirectoryLoader
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from dotenv import load_dotenv
import os

load_dotenv()
DATA_PATH = os.environ.get("DATA_PATH")
DB_FAISS_PATH = os.environ.get("DB_FAISS_PATH")


#loading the data
def load_pdf_file(data):
    loader = DirectoryLoader(data,
        glob= "*.pdf",
        loader_cls = PyMuPDFLoader
    )
    return loader.load()


#creating clusters 
def create_chunks(extracted_data):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=5000,chunk_overlap=50
    )
    text_chunk = text_splitter.split_documents(extracted_data)
    return text_chunk

#covertingt he chunks into embedding
def get_embedding_model():
    embedding_model = HuggingFaceEmbeddings(
        model_name = "sentence-transformers/all-MiniLM-L6-V2"
    )
    return embedding_model


embedding_model = get_embedding_model()
documents = load_pdf_file(DATA_PATH)
chunks = create_chunks(documents)
db = FAISS.from_documents(chunks,embedding_model)
db.save_local(DB_FAISS_PATH)

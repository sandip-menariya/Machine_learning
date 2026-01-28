# 1. Load and Split Documents
from langchain_community.document_loaders import PyPDFLoader,TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_classic.prompts import ChatPromptTemplate

document=None
vectorstore=None
qa_chain=None

text_splitter = RecursiveCharacterTextSplitter(
      chunk_size=100,
      chunk_overlap=20
  )
def upload_file(file_path): 
  global document
  if file_path.endswith(".pdf"):
    loader = PyPDFLoader(file_path)
  elif file_path.endswith(".txt"):
    loader=TextLoader(file_path)
  else:
    raise ValueError("invalid file format")
  document=loader.load()

# 2. Generate Embeddings and Create Vector Store
from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings

def vector_store_embeddings():
  global document,vectorstore
  if document==None:
    raise ValueError("Document is not uploaded")
  chunks = text_splitter.split_documents(document)
  embeddings = GoogleGenerativeAIEmbeddings(
      model="models/gemini-embedding-001",
      google_api_key="GEMINI_API_KEY"
  )
  vectorstore = FAISS.from_documents(chunks, embeddings)

# 3. A RetrievalQA Chain
from langchain_classic.chains.retrieval import create_retrieval_chain
from langchain_google_genai import ChatGoogleGenerativeAI

def retrieval_chain():
  global vectorstore,qa_chain
  if vectorstore==None:
    raise ValueError("vector store is not created")
  llm = ChatGoogleGenerativeAI(
      temperature=0,
      model="models/gemini-2.5-flash",
      api_key="GEMINI_API_KEY")
  prompt=ChatPromptTemplate.from_template(
      """You are a helpful AI assistant. Use the following context to answer the question at the end.\n\n
      <context>
    {context}
    </context>
      Question: {input}\n
      Answer:"""
  )
  doc_chain=create_stuff_documents_chain(llm,prompt)
  retriever=vectorstore.as_retriever(search_kwargs={"k": 4})
  qa_chain = create_retrieval_chain(retriever,doc_chain)

from fastapi import FastAPI,UploadFile,File
from pydantic import BaseModel

app=FastAPI()

class QuestionRequest(BaseModel):
  question:str
from fastapi import BackgroundTasks
@app.post("/upload")
async def load_file(file:UploadFile=File(...),background_tasks:BackgroundTasks=None):
  file_path=f"C:\\Users\\Dell\\OneDrive\\Desktop\\RAG_Model\\.venv\\my_file\\{file.filename}"
  with open(file_path,'wb') as fp:
    fp.write(await file.read())
  background_tasks.add_task(process_document,file_path)

def process_document(file_path):
  upload_file(file_path)
  vector_store_embeddings()
  retrieval_chain()

from slowapi import Limiter
from slowapi.util import get_remote_address
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

# @limiter.limit("5/minute")
@app.post("/ask")
def ask_question(req: QuestionRequest):
    if qa_chain is None:
        return {"error": "No document uploaded and processed yet."}
    result = qa_chain.invoke({"input": req.question})
    return {"answer": result["answer"]}
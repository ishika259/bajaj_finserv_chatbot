from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI
import os

DATA_DIR = "data"
VECTOR_STORE_DIR = "vector_store"

def get_all_text_documents():
docs = []
for fname in os.listdir(DATA_DIR):
if fname.endswith(".txt"):
with open(os.path.join(DATA_DIR, fname), "r", encoding="utf-8") as f:
docs.append(f.read())
return docs

def load_or_create_vector_store():
if not os.path.exists(os.path.join(VECTOR_STORE_DIR, "index")):
print("🧠 Creating new vector store from scratch...")
docs = get_all_text_documents()
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
texts = text_splitter.create_documents(docs)
vectorstore = Chroma.from_documents(texts, OpenAIEmbeddings(), persist_directory=VECTOR_STORE_DIR)
vectorstore.persist()
return Chroma(persist_directory=VECTOR_STORE_DIR, embedding_function=OpenAIEmbeddings())

def answer_question(query):
vectorstore = load_or_create_vector_store()
llm = ChatOpenAI(temperature=0)
qa_chain = RetrievalQA.from_chain_type(llm=llm, retriever=vectorstore.as_retriever())
return qa_chain.run(query)
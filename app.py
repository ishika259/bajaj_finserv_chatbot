import streamlit as st
from modules.data_handler import handle_stock_query
from modules.document_qa import answer_question
from modules.cfo_responder import generate_cfo_comment
from dotenv import load_dotenv

load_dotenv()
st.set_page_config(page_title="Bajaj Finserv Chatbot", layout="wide")
st.title("🤖 Bajaj Finserv Smart Chatbot")

query = st.text_input("Ask your question")

if query:
if "price" in query.lower() or "stock" in query.lower():
response = handle_stock_query(query)
elif "cfo" in query.lower():
response = generate_cfo_comment(query)
else:
response = answer_question(query)
st.markdown(response)




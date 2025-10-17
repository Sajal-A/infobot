import streamlit as st
from sidebar import display_sidebar
from display_chat_interface import display_chat_interface

# title 
st.title('🤖 RAG Chatbot')

# initialize 
if "messages" not in st.session_state:
    st.session_state.messages = []

if "session_id" not in st.session_state:
    st.session_state.session_id =  None

# display the sidebar
display_sidebar()

# display the chat interface
display_chat_interface()




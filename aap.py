import streamlit as st
from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

st.title("Harshit's AI Chatbot 🤖")

if "messages" not in st.session_state:
    st.session_state.messages = []

# show previous chat
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

prompt = st.chat_input("Ask something...")

if prompt:

    st.session_state.messages.append(
        {"role": "user", "content": prompt}
    )

    with st.chat_message("user"):
        st.write(prompt)

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=st.session_state.messages
    )

    reply = response.choices[0].message.content

    st.session_state.messages.append(
        {"role": "assistant", "content": reply}
    )

    with st.chat_message("assistant"):
        st.write(reply)
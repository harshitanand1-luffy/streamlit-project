import streamlit as st
from groq import Groq
import time

# Page config
st.set_page_config(
    page_title="Hello Bhai Log",
    page_icon="🤖",
    layout="wide"
)

# Custom CSS styling
st.markdown("""
<style>

.stApp {
    background-color: #0e1117;
}

h1 {
    text-align: center;
    font-size: 48px;
}

.block-container {
    max-width: 900px;
    margin: auto;
}

</style>
""", unsafe_allow_html=True)

# Groq client
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# Title
st.markdown("<h1>Hello bhai log...</h1>", unsafe_allow_html=True)
st.caption("AI chatbot powered by Groq ⚡")

# Chat memory
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous chat
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# Chat input
prompt = st.chat_input("Pucho jo puchna hai...")

if prompt:

    # Store user message
    st.session_state.messages.append(
        {"role": "user", "content": prompt}
    )

    # Display user message
    with st.chat_message("user"):
        st.write(prompt)

    # Get AI response
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=st.session_state.messages
    )

    reply = response.choices[0].message.content

    # Store AI response
    st.session_state.messages.append(
        {"role": "assistant", "content": reply}
    )

    # Typing animation
    with st.chat_message("assistant"):
        placeholder = st.empty()
        text = ""

        for word in reply.split():
            text += word + " "
            placeholder.markdown(text)
            time.sleep(0.03)
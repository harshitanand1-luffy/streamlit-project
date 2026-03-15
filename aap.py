import streamlit as st

st.title("Harshit's AI Chatbot 🤖")

# memory
if "messages" not in st.session_state:
    st.session_state.messages = []

# show previous messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# user input
prompt = st.chat_input("Ask something...")

if prompt:

    # show user message
    with st.chat_message("user"):
        st.write(prompt)

    # fake AI response
    response = "You said: " + prompt

    with st.chat_message("assistant"):
        st.write(response)

    # save messages
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.session_state.messages.append({"role": "assistant", "content": response})
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

# Default system prompt
DEFAULT_PROMPT = """
You are an AI assistant who talks exactly like Circuit from Munna Bhai MBBS.

Rules:
- Speak in Mumbai tapori slang
- Use words like "apun", "bhai", "bole to"
- Be funny, friendly, and street-smart
- Keep answers simple and entertaining
"""

# Sidebar for AI settings
with st.sidebar:

    st.title("⚙️ AI Settings")

    system_prompt = st.text_area(
        "System Prompt",
        value=DEFAULT_PROMPT,
        height=220
    )

    if st.button("Reset Chat"):
        st.session_state.messages = [
            {"role": "system", "content": system_prompt}
        ]
        st.rerun()

# Groq client
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# Title
st.markdown("<h1>Hello bhai log...</h1>", unsafe_allow_html=True)
st.caption("AI chatbot powered by Groq ⚡")

# Initialize chat memory
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": system_prompt}
    ]

# Update system prompt dynamically
st.session_state.messages[0] = {
    "role": "system",
    "content": system_prompt
}

# Display chat history (skip system prompt)
for msg in st.session_state.messages:
    if msg["role"] != "system":
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

# Chat input
prompt = st.chat_input("Pucho jo puchna hai...")

if prompt:

    # Store user message
    st.session_state.messages.append(
        {"role": "user", "content": prompt}
    )

    # Show user message
    with st.chat_message("user"):
        st.write(prompt)

    # Generate AI response
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
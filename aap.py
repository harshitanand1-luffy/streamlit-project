import os
import streamlit as st
from groq import Groq
import time

# ---------------- SECRETS UTIL ----------------
def get_groq_api_key():
    try:
        return st.secrets.get("GROQ_API_KEY", "")
    except Exception:
        return os.environ.get("GROQ_API_KEY", "")

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Circuit Bhai AI",
    page_icon="🤖",
    layout="wide"
)

st.write("✅ Circuit Bhai AI starting...")

# ---------------- CUSTOM CSS ----------------
st.markdown("""
<style>
.stApp {
    background: linear-gradient(120deg, #ffedb5, #ff8800);
}

h1 {
    text-align: center;
    font-size: 52px;
}

[data-testid="stChatMessage"] {
    background: rgba(0,0,0,0.8);
    color: white;
    border-radius: 15px;
    padding: 14px;
}

[data-testid="stChatMessage"][data-testid*="user"] {
    background: linear-gradient(135deg, #ffcc00, #ff8800);
    color: black;
}
</style>
""", unsafe_allow_html=True)

# ---------------- IMAGE PATH ----------------
image_path = os.path.join(os.path.dirname(__file__), "circuit.png")

# ---------------- SIDEBAR ----------------
with st.sidebar:
    st.image(image_path, width=120)
    st.markdown("## ⚙️ Circuit Settings")

    system_prompt = st.text_area(
        "🧠 Personality",
        value="Talk like Circuit in Hinglish, funny and street smart",
        height=150
    )

# ---------------- GROQ ----------------
api_key = get_groq_api_key()

if api_key:
    client = Groq(api_key=api_key)
else:
    client = None

# ---------------- HEADER ----------------
col1, col2 = st.columns([1,3])

with col1:
    st.image(image_path, width=120)

with col2:
    st.markdown("<h1>😎 Hello Bhai Log...</h1>", unsafe_allow_html=True)

st.markdown("""
"Bhai tension nahi lene ka… apun hai na 😎"
""")

# ---------------- CHAT ----------------
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": system_prompt}
    ]

st.session_state.messages[0] = {
    "role": "system",
    "content": system_prompt
}

# Show chat
for msg in st.session_state.messages:
    if msg["role"] != "system":
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

# Input
prompt = st.chat_input("Bole to kya puchna hai bhai...")

if prompt:

    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.write(prompt)

    if client:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=st.session_state.messages
        )
        reply = response.choices[0].message.content
    else:
        reply = "Bhai demo mode chal raha hai 😎"

    st.session_state.messages.append({"role": "assistant", "content": reply})

    with st.chat_message("assistant"):
        st.write(reply)
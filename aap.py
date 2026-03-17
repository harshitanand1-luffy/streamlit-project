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

/* 🔥 DARK CINEMATIC BACKGROUND */
.stApp {
    background: radial-gradient(circle at top, #1a1a1a, #000000 80%);
    color: white;
    overflow: hidden;
}

/* 🔥 HEADER */
h1 {
    text-align: center;
    font-size: 54px;
    font-weight: bold;
    color: #ffcc00;
    text-shadow: 0px 0px 20px rgba(255, 200, 0, 0.8);
}

/* 🔥 QUOTE */
blockquote {
    text-align: center;
    font-size: 20px;
    font-style: italic;
    color: #ffdd88;
}

/* 🔥 CHAT CONTAINER */
.block-container {
    max-width: 900px;
    margin: auto;
}

/* 🔥 CHAT BUBBLES */
[data-testid="stChatMessage"] {
    background: rgba(20, 20, 20, 0.75);
    backdrop-filter: blur(12px);
    color: #ffffff;
    border-radius: 18px;
    padding: 14px;
    margin-bottom: 12px;
    box-shadow: 0 0 20px rgba(255, 140, 0, 0.3);
    border: 1px solid rgba(255,255,255,0.1);
}

/* 🔥 USER MESSAGE */
[data-testid="stChatMessage"][data-testid*="user"] {
    background: linear-gradient(135deg, #ff9900, #ff3300);
    color: white;
}

/* 🔥 INPUT BOX */
textarea, .stChatInput textarea {
    background-color: rgba(0,0,0,0.9) !important;
    color: #ffcc00 !important;
    border-radius: 14px !important;
    border: 1px solid #ff9900 !important;
}

/* 🔥 SIDEBAR */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #111, #000);
    color: #ffcc00;
}

/* 🔥 BUTTON */
.stButton>button {
    background: linear-gradient(135deg, #ff6600, #ff0000);
    color: white;
    border-radius: 12px;
    font-weight: bold;
}

/* 🔥 GLOW */
img {
    filter: drop-shadow(0px 0px 15px rgba(255, 150, 0, 0.9));
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
<blockquote>
"Bhai tension nahi lene ka… apun hai na 😎"
</blockquote>
""", unsafe_allow_html=True)

# ---------------- CHAT ----------------
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": system_prompt}
    ]

st.session_state.messages[0] = {
    "role": "system",
    "content": system_prompt
}

# ---------------- DISPLAY CHAT ----------------
for msg in st.session_state.messages:
    if msg["role"] != "system":

        if msg["role"] == "assistant":
            avatar = image_path   # circuit image
        else:
            avatar = "😎"         # user emoji

        with st.chat_message(msg["role"], avatar=avatar):
            st.write(msg["content"])

# ---------------- INPUT ----------------
prompt = st.chat_input("Bole to kya puchna hai bhai...")

if prompt:

    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user", avatar="😎"):
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

    with st.chat_message("assistant", avatar=image_path):

        placeholder = st.empty()
        text = ""

        for word in reply.split():
            text += word + " "
            placeholder.markdown(text)
            time.sleep(0.03)
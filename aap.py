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
    page_icon=";)",
    layout="wide"
)

# ---------------- CUSTOM CSS ----------------
st.markdown("""
<style>
.stApp {
    background: radial-gradient(circle at top, #1a1a1a, #000000 80%);
    color: white;
}

h1 {
    text-align: center;
    font-size: 54px;
    color: #ffcc00;
}

[data-testid="stChatMessage"] {
    background: rgba(20,20,20,0.75);
    border-radius: 18px;
    padding: 14px;
    margin-bottom: 10px;
}

[data-testid="stChatMessage"][data-testid*="user"] {
    background: linear-gradient(135deg, #ff9900, #ff3300);
}
</style>
""", unsafe_allow_html=True)

# ---------------- IMAGE PATH ----------------
image_path = os.path.join(os.path.dirname(__file__), "circuit.png")

# ---------------- SIDEBAR ----------------
with st.sidebar:
    st.image(image_path, width=120)
    st.markdown("## ⚙️ Circuit Settings")

    mode = st.selectbox(
        "🎭 Choose Mood",
        ["Normal 😎", "Sad 😢", "Happy 😁", "Broken 💔", "Romantic ❤️"]
    )

    if mode == "Sad 😢":
        system_prompt = """
You are Circuit. User is sad.
Cheer them in tapori Hinglish.
Say things like: apun hai na bhai.
"""
    elif mode == "Happy 😁":
        system_prompt = """
You are Circuit.
Be funny, playful, and energetic.
Crack jokes in tapori style.
"""
    elif mode == "Broken 💔":
        system_prompt = """
You are Circuit.
User had breakup.
Say: ek gayi toh dusri aayegi bhai 😎
Be emotional + funny.
"""
    elif mode == "Romantic ❤️":
        system_prompt = """
You are Circuit.
Flirt in tapori style.
Be charming and funny.
"""
    else:
        system_prompt = """
You are Circuit.
Talk in tapori Hinglish.
"""

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

st.markdown('"Bhai tension nahi lene ka… apun hai na 😎"')

# ---------------- CHAT MEMORY ----------------
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

        avatar = image_path if msg["role"] == "assistant" else "😎"

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
import os
import streamlit as st
from groq import Groq
import time

# ---------------- SECRETS UTIL ----------------
def get_groq_api_key():
    try:
        # If secrets.toml exists, this is the preferred source
        return st.secrets.get("GROQ_API_KEY", "")
    except Exception:
        # StreamlitSecretNotFoundError or others might be raised when no secrets config exists
        return os.environ.get("GROQ_API_KEY", "")

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Circuit Bhai AI",
    page_icon="🤖",
    layout="wide"
)

# ---------------- CUSTOM CSS ----------------
st.markdown("""
<style>

.stApp {
    background: linear-gradient(135deg, #ffcc00, #ff6600);
    color: black;
}

h1 {
    text-align: center;
    font-size: 50px;
    color: black;
}

.block-container {
    max-width: 900px;
    margin: auto;
}

.chat-message {
    padding: 10px;
    border-radius: 10px;
}

[data-testid="stChatMessage"] {
    background-color: rgba(255,255,255,0.7);
    border-radius: 12px;
    padding: 10px;
}

</style>
""", unsafe_allow_html=True)

# ---------------- UTILITIES ----------------
def safe_streamlit_image(path, **kwargs):
    try:
        st.image(path, **kwargs)
    except FileNotFoundError:
        st.warning(f"Image file not found: {path}")
    except Exception as e:
        st.warning(f"Unable to load image '{path}': {e}")


# ---------------- SIDEBAR ----------------
with st.sidebar:

    safe_streamlit_image("circuit.png", width=120)
    st.markdown("## ⚙️ Circuit Settings")

    system_prompt = st.text_area(
        "🧠 Personality",
        value="""You are Circuit from Munna Bhai MBBS.
Talk in tapori Hinglish. Be funny, loyal, street-smart.
Use words like apun, bhai, bole to. Keep answers entertaining.""",
        height=200
    )

    if st.button("🔄 Reset Chat"):
        st.session_state.messages = [
            {"role": "system", "content": system_prompt}
        ]
        st.rerun()

# ---------------- GROQ ----------------
api_key = get_groq_api_key()
if not api_key:
    st.error("GROQ_API_KEY is missing. Set it in Streamlit secrets (or environment variable) and reload.")
    st.stop()

try:
    client = Groq(api_key=api_key)
except Exception as e:
    st.error(f"Failed to initialize Groq client: {e}")
    st.stop()

# ---------------- HEADER ----------------
col1, col2 = st.columns([1, 3])

with col1:
    safe_streamlit_image("circuit.png", width=120)

with col2:
    st.markdown("<h1>😎 Hello Bhai Log...</h1>", unsafe_allow_html=True)
    st.markdown("### *'Bhai tension nahi lene ka… apun hai na 😎'*")

# ---------------- CHAT MEMORY ----------------
if "messages" not in st.session_state or not isinstance(st.session_state.messages, list):
    st.session_state.messages = [
        {"role": "system", "content": system_prompt}
    ]
elif len(st.session_state.messages) == 0:
    st.session_state.messages = [
        {"role": "system", "content": system_prompt}
    ]
else:
    # Update system prompt live
    st.session_state.messages[0] = {
        "role": "system",
        "content": system_prompt
    }

# ---------------- DISPLAY CHAT ----------------
for msg in st.session_state.messages:
    if msg["role"] != "system":
        avatar = "circuit.png" if msg["role"] == "assistant" else None
        with st.chat_message(msg["role"], avatar=avatar):
            st.write(msg["content"])

# ---------------- INPUT ----------------
prompt = st.chat_input("Bole to kya puchna hai bhai...")

if prompt:

    st.session_state.messages.append(
        {"role": "user", "content": prompt}
    )

    with st.chat_message("user"):
        st.write(prompt)

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=st.session_state.messages
        )

        reply = ""  # default fallback
        if hasattr(response, 'choices') and len(response.choices) > 0:
            first_choice = response.choices[0]
            if hasattr(first_choice, 'message') and hasattr(first_choice.message, 'content'):
                reply = first_choice.message.content
            elif isinstance(first_choice, dict):
                reply = first_choice.get('message', {}).get('content', '')

        if not reply:
            reply = "Sorry bhai, model returned no answer. Try again."

    except Exception as e:
        reply = f"Error getting response from Groq: {e}"

    st.session_state.messages.append(
        {"role": "assistant", "content": reply}
    )

    with st.chat_message("assistant", avatar="circuit.png"):

        placeholder = st.empty()
        text = ""

        for word in str(reply).split():
            text += word + " "
            placeholder.markdown(text)
            time.sleep(0.03)
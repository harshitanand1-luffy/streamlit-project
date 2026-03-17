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

/* Background */
.stApp {
    position: relative;
    background:
      linear-gradient(120deg, #ffedb5 0%, #ffc565 25%, #ffb22e 50%, #f59300 75%, #e27800 100%),
      repeating-linear-gradient(45deg, rgba(255,255,255,0.15), rgba(255,255,255,0.15) 8px, transparent 8px, transparent 16px);
    color: #1a1a1a;
    background-blend-mode: overlay;
    filter: brightness(0.92) contrast(1.05);
}

/* Decorative sides */
.stApp::before,
.stApp::after {
    content: "";
    position: absolute;
    top: 0;
    width: 130px;
    height: 100%;
    z-index: -1;
    background-image: radial-gradient(circle at top, rgba(255,239,165,0.9), transparent 45%),
                      repeating-linear-gradient(0deg, rgba(255,255,255,0.3), rgba(255,255,255,0.3) 2px, transparent 2px, transparent 6px);
}
.stApp::before {
    left: 0;
    transform: skewY(-8deg);
}
.stApp::after {
    right: 0;
    transform: skewY(8deg);
}

/* Balloons + guns icons */
.stApp .balloon-gun {
    position: fixed;
    width: 60px;
    height: 60px;
    font-size: 40px;
    line-height: 60px;
    text-align: center;
    opacity: 0.8;
    pointer-events: none;
    animation: floatAround 8s ease-in-out infinite;
}
.stApp .balloon-gun:nth-child(1) { left: 15px; top: 180px; animation-delay: 0s; }
.stApp .balloon-gun:nth-child(2) { right: 18px; top: 240px; animation-delay: 1.3s; }
.stApp .balloon-gun:nth-child(3) { left: 10px; top: 340px; animation-delay: 2.7s; }
.stApp .balloon-gun:nth-child(4) { right: 20px; top: 420px; animation-delay: 0.6s; }
.stApp .balloon-gun:nth-child(5) { left: 22px; top: 520px; animation-delay: 1.9s; }

@keyframes floatAround {
    0%,100% { transform: translateY(0px) scale(1); }
    50% { transform: translateY(-8px) scale(1.06); }
}

/* Header */
h1 {
    text-align: center;
    font-size: 52px;
    font-weight: bold;
    color: #111;
}

/* Quote styling */
blockquote {
    text-align: center;
    font-size: 20px;
    font-style: italic;
    color: #2b2b2b;
}

/* Chat container */
.block-container {
    max-width: 900px;
    margin: auto;
}

/* Chat bubbles */
[data-testid="stChatMessage"] {
    background: rgba(0, 0, 0, 0.75);
    color: #ffffff;
    border-radius: 15px;
    padding: 14px;
    margin-bottom: 10px;
    box-shadow: 0 4px 15px rgba(0,0,0,0.4);
}

/* User messages */
[data-testid="stChatMessage"][data-testid*="user"] {
    background: linear-gradient(135deg, #ffcc00, #ff8800);
    color: black;
}

/* Input box */
textarea, .stChatInput textarea {
    background-color: rgba(0,0,0,0.8) !important;
    color: white !important;
    border-radius: 12px !important;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #ffcc00, #ff6600);
    color: black;
}

/* Buttons */
.stButton>button {
    background: linear-gradient(135deg, #ff6600, #ff3300);
    color: white;
    border-radius: 10px;
    font-weight: bold;
}

/* Glow effect */
img {
    filter: drop-shadow(0px 0px 10px rgba(255, 200, 0, 0.8));
}

</style>
""", unsafe_allow_html=True)

# ---------------- IMAGE PATH ----------------
image_path = os.path.join(os.path.dirname(__file__), "circuit.png")

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

    safe_streamlit_image(image_path, width=120)
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

# Decorative emoji objects on sides (balloons + guns)
st.markdown("""
<div class='balloon-gun'>🎈</div>
<div class='balloon-gun'>🔫</div>
<div class='balloon-gun'>🎈</div>
<div class='balloon-gun'>🔫</div>
<div class='balloon-gun'>🎈</div>
""", unsafe_allow_html=True)

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
    safe_streamlit_image(image_path, width=120)

with col2:
    st.markdown("<h1>😎 Hello Bhai Log...</h1>", unsafe_allow_html=True)

# Movie-style quote
st.markdown("""
<blockquote>
"Bhai tension nahi lene ka… apun hai na 😎<br>
Jadoo ki jhappi AI version 💛"
</blockquote>
""", unsafe_allow_html=True)

# Divider
st.markdown("---")

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
        avatar = image_path if msg["role"] == "assistant" else None
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
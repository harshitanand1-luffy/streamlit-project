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

# quick debug banner (confirm code execution)
st.write("✅ Circuit Bhai AI starting...")

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

# ---------------- GROQ ----------------
api_key = get_groq_api_key()
use_demo = False

if not api_key:
    st.warning("GROQ_API_KEY is missing. App will run in demo mode. Set the env variable or secrets and refresh for live GPT responses.")
    use_demo = True
else:
    try:
        client = Groq(api_key=api_key)
    except Exception as e:
        st.warning(f"Failed to initialize Groq client: {e}. Switching to demo mode.")
        use_demo = True

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
user_avatar_url = "https://img.icons8.com/emoji/48/000000/loudly-crying-face.png"
assistant_avatar = image_path

for msg in st.session_state.messages:
    if msg["role"] != "system":
        avatar = assistant_avatar if msg["role"] == "assistant" else user_avatar_url
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

    if use_demo:
        # Demo fallback when API key is missing or client init fails
        reply = "Bhai, demo mode speak kar raha hoon—full offline. API key missing or connection issue, toh live model nahi chala paaya."
    else:
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
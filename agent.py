import streamlit as st
from google import genai

# 1. Configure the Client (The "Brain")
try:
    # If this fails, make sure you have a .streamlit/secrets.toml file
    client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])
except Exception:
    st.error("⚠️ API Key not found. Please add it to your secrets.toml file.")
    st.stop()

# 2. Setup the Page
st.title("🤖 My Personal Agent")
if "messages" not in st.session_state:
    st.session_state.messages = []

# 3. Display Old Chat History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 4. Handle New Input
if prompt := st.chat_input("What's on your mind?"):
    # A. Show User Message
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # B. Build Memory (The "Context")
    # We convert Streamlit's history to the format Google expects
    gemini_history = []
    for msg in st.session_state.messages:
        # Google uses "model" instead of "assistant"
        role = "model" if msg["role"] == "assistant" else "user"
        gemini_history.append({
            "role": role,
            "parts": [{"text": msg["content"]}]
        })

    # C. Generate Reply
    with st.chat_message("assistant"):
        try:
            # FIXED: We use 'client.models', not 'model'
            # FIXED: We use 'gemini-1.5-flash' (2.5 is not out yet!)
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=gemini_history
            )
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"An error occurred: {e}")


import streamlit as st
from google import genai

# 1. Configure the Client (The "Brain")
# This reads from your .streamlit/secrets.toml file
try:
    client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])
except Exception:
    st.error("⚠️ API Key not found. Please add it to your secrets.toml file.")
    st.stop()

# 2. Title and Setup
st.title("🤖 My Personal Agent")
if "messages" not in st.session_state:
    st.session_state.messages = []

# 3. Display Chat History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 4. Handle New Input
if prompt := st.chat_input("What's on your mind?"):
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

 gemini_history = []
    for msg in st.session_state.messages:
        role = "model" if msg["role"] == "assistant" else "user"
        gemini_history.append({
            "role": role,
            "parts": [{"text": msg["content"]}]
        })

    # Generate and display AI response
    with st.chat_message("assistant"):
        try:
            # FIX: Use 'client.models' instead of 'model'
            response = client.models.generate_content(
                model="gemini-2.5-flash", 
                contents=prompt
            )
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"An error occurred: {e}")



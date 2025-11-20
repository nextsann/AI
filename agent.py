import streamlit as st
from google import genai
from google.genai import types  # <--- 1. IMPORT TYPES

# 2. Configure the Client
try:
    client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])
except Exception:
    st.error("⚠️ API Key not found. Please add it to your secrets.toml file.")
    st.stop()

st.title("🤖 My Personal Agent")

if "messages" not in st.session_state:
    st.session_state.messages = []

# 3. Display History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 4. Handle New Input
if prompt := st.chat_input("What's on your mind?"):
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # --- MEMORY BUILDER (FIXED FOR NEW SDK) ---
    gemini_history = []
    for msg in st.session_state.messages:
        # Convert role names
        role = "model" if msg["role"] == "assistant" else "user"
        
        # Create the strict objects the new SDK demands
        part = types.Part(text=msg["content"])
        content = types.Content(role=role, parts=[part])
        gemini_history.append(content)
    # ------------------------------------------

    with st.chat_message("assistant"):
        try:
            # Define Personality
            sys_instruct = "You are a helpful, slightly sarcastic personal assistant."

            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=gemini_history,  # Now contains valid types.Content objects
                config=types.GenerateContentConfig(
                    system_instruction=sys_instruct
                )
            )
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"An error occurred: {e}")

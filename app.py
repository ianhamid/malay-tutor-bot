import streamlit as st
import os
from google import genai
from google.genai import types

st.set_page_config(page_title="Madam K", page_icon="🇲🇾")

# Password check
if "password_correct" not in st.session_state:
    if st.text_input("Enter password:", type="password") == "kukubird14":
        st.session_state["password_correct"] = True
        st.rerun()
    st.stop()

# Initialize Client
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

st.title("Madam K")

# Track if this is the first interaction
if "is_first_turn" not in st.session_state:
    st.session_state.is_first_turn = True

# Chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Cache answers
@st.cache_data(ttl=3600)
def get_answer(prompt, is_first):
    # Conditional instruction based on turn
    greeting_instr = "Include a warm, friendly greeting." if is_first else "Do not use a greeting. Start directly with the answer."
    instruction = f"You are a warm, educational Malay tutor. {greeting_instr} Structure: Definition (DBP), Story/Example, English Equivalent, Conclusion. Use emojis."
    
    response = client.models.generate_content_stream(
        model='gemini-3.5-flash',
        contents=f"{instruction}\n\nUser Question: {prompt}",
        config=types.GenerateContentConfig(
            safety_settings=[types.SafetySetting(category="HARM_CATEGORY_HARASSMENT", threshold="BLOCK_NONE")]
        )
    )
    return response

if prompt := st.chat_input("Apa maksud peribahasa...?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        try:
            # Pass the current state to the helper
            for chunk in get_answer(prompt, st.session_state.is_first_turn):
                if chunk.text:
                    full_response += chunk.text
                    message_placeholder.markdown(full_response + "▌")
            
            message_placeholder.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            
            # After first turn, lock it to False
            st.session_state.is_first_turn = False
            
        except Exception as e:
            st.error("Too busy! Try again.")
import streamlit as st
import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

st.set_page_config(page_title="Madam K", page_icon="🇲🇾")

# 1. Global Client
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# 2. Stream response WITHOUT caching (streaming + cache = conflict)
def get_tutor_response(prompt):
    """Stream Malay tutor response from Gemini."""
    instruction = "You are a warm Malay tutor. Concise, emojis, DBP definition."
    
    return client.models.generate_content_stream(
        model='gemini-2.0-flash-lite',
        contents=f"{instruction}\n\nQuestion: {prompt}"
    )

st.title("Madam K")

if prompt := st.chat_input("Apa maksud buntal...?"):
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        try:
            for chunk in get_tutor_response(prompt):
                if chunk.text:
                    full_response += chunk.text
                    message_placeholder.markdown(full_response + "▌")
            message_placeholder.markdown(full_response)
        except Exception as e:
            st.error(f"API Error: {str(e)}")
            st.info("Check: API key valid? Quota available? Network stable?")
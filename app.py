import streamlit as st
import os
from google import genai
from google.genai import types

st.set_page_config(page_title="Madam K", page_icon="🇲🇾")

# 1. Global Client (Pre-warmed)
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# 2. Simple Caching for Speed
@st.cache_data(ttl=3600)
def get_fast_response(prompt):
    instruction = "You are a warm Malay tutor. Concise, emojis, DBP definition."
    return client.models.generate_content_stream(
        model='gemini-2.0-flash-lite', # Stable, high-availability model
        contents=f"{instruction}\n\nQuestion: {prompt}"
    )
    # Stream the content directly
    return client.models.generate_content_stream(
        model='gemini-3.5-flash',
        contents=f"{instruction}\n\nQuestion: {prompt}",
        config=types.GenerateContentConfig(
            safety_settings=[types.SafetySetting(category="HARM_CATEGORY_HARASSMENT", threshold="BLOCK_NONE")]
        )
    )

st.title("Madam K")

if prompt := st.chat_input("Apa maksud buntal...?"):
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        # Immediate streaming execution
        try:
            for chunk in get_fast_response(prompt):
                if chunk.text:
                    full_response += chunk.text
                    message_placeholder.markdown(full_response + "▌")
            message_placeholder.markdown(full_response)
        except Exception:
            st.error("Too busy. Try again immediately.")
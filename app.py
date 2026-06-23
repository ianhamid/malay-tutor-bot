import streamlit as st
import os
import time
import random
from google import genai
from google.genai import types

# Set up page configuration
st.set_page_config(page_title="Madam K", page_icon="🇲🇾")

# Password Protection
def check_password():
    if "password_correct" not in st.session_state:
        password = st.text_input("Enter password to start learning:", type="password")
        if password == "kukubird14":
            st.session_state["password_correct"] = True
            st.rerun()
        return False
    return True

if not check_password():
    st.stop()

# Configure the modern Client
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

st.title("Madam K")

# Chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat Input
if prompt := st.chat_input("Apa maksud peribahasa...?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        instruction = """
        You are a warm, educational Malay tutor for children. 
        Follow this strict output structure: Greeting, Definition (DBP), Story/Example, English Equivalent, Conclusion.
        Use emojis. Maintain a patient, encouraging tone.
        """
        
        # Define model chain for fallback
        # Updated to models compatible with your SDK and environment
        model_chain = ['gemini-3.5-flash', 'gemini-3.1-flash-lite']
        response_text = None
        
        with st.spinner("Madam K is thinking..."):
            for model_name in model_chain:
                try:
                    # Retry logic (Exponential Backoff)
                    for attempt in range(3): 
                        try:
                            response = client.models.generate_content(
                                model=model_name,
                                contents=f"{instruction}\n\nUser Question: {prompt}",
                                config=types.GenerateContentConfig(
                                    safety_settings=[
                                        types.SafetySetting(category="HARM_CATEGORY_HARASSMENT", threshold="BLOCK_NONE"),
                                        types.SafetySetting(category="HARM_CATEGORY_HATE_SPEECH", threshold="BLOCK_NONE"),
                                        types.SafetySetting(category="HARM_CATEGORY_SEXUALLY_EXPLICIT", threshold="BLOCK_NONE"),
                                        types.SafetySetting(category="HARM_CATEGORY_DANGEROUS_CONTENT", threshold="BLOCK_NONE"),
                                    ]
                                )
                            )
                            response_text = response.text
                            break 
                        except Exception as e:
                            # If it's a 503, wait and retry
                            if "503" in str(e) and attempt < 2:
                                time.sleep(2 ** attempt + random.uniform(0, 1))
                                continue
                            raise e
                    if response_text: break 
                except Exception:
                    continue 

        if response_text:
            st.markdown(response_text)
            st.session_state.messages.append({"role": "assistant", "content": response_text})
        else:
            st.error("Madam K is currently overloaded on all models. Please try again shortly.")
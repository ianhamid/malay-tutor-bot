import streamlit as st
import os
from google import genai

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
# This automatically handles the correct production API endpoints
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
        
        try:
            # Modern API call
            response = client.models.generate_content(
                model='gemini-1.5-flash',
                contents=f"{instruction}\n\nUser Question: {prompt}",
                config=genai.types.GenerateContentConfig(
                    safety_settings=[
                        genai.types.SafetySetting(category="HARM_CATEGORY_HARASSMENT", threshold="BLOCK_NONE"),
                        genai.types.SafetySetting(category="HARM_CATEGORY_HATE_SPEECH", threshold="BLOCK_NONE"),
                        genai.types.SafetySetting(category="HARM_CATEGORY_SEXUALLY_EXPLICIT", threshold="BLOCK_NONE"),
                        genai.types.SafetySetting(category="HARM_CATEGORY_DANGEROUS_CONTENT", threshold="BLOCK_NONE"),
                    ]
                )
            )
            
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
            
        except Exception as e:
            st.error(f"DEBUG ERROR: {str(e)}")
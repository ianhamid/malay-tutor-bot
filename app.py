import streamlit as st
import google.generativeai as genai
import os
import time

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

# Configure Gemini
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-2.5-flash')

# UPDATED: Header changed to just "Madam K"
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
        
        # UPDATED: Added Error Handling for Quota (429)
        try:
            response = model.generate_content(f"{instruction}\n\nUser Question: {prompt}")
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            if "429" in str(e):
                error_msg = "Madam K is resting for a moment, let's try again in a few seconds! ☕"
                st.warning(error_msg)
            else:
                st.error("Something went wrong. Please try again.")
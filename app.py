import streamlit as st
import google.generativeai as genai
import os

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
# Forced to use production endpoint to avoid v1beta 404 errors
genai.configure(
    api_key=os.getenv("GEMINI_API_KEY"),
    client_options={"api_endpoint": "https://generativelanguage.googleapis.com"}
)

# Initialize the model
model = genai.GenerativeModel('gemini-1.5-flash')

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
            # Added safety settings to prevent blocks
            response = model.generate_content(
                f"{instruction}\n\nUser Question: {prompt}",
                safety_settings={
                    'HARM_CATEGORY_HARASSMENT': 'BLOCK_NONE',
                    'HARM_CATEGORY_HATE_SPEECH': 'BLOCK_NONE',
                    'HARM_CATEGORY_SEXUALLY_EXPLICIT': 'BLOCK_NONE',
                    'HARM_CATEGORY_DANGEROUS_CONTENT': 'BLOCK_NONE',
                }
            )
            
            if response.text:
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            else:
                st.error("Madam K was unable to generate a response.")
                
        except Exception as e:
            st.error(f"DEBUG ERROR: {str(e)}")
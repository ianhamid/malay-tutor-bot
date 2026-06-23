import streamlit as st
import google.generativeai as genai
import os

# Set up page configuration
st.set_page_config(page_title="Cikgu AI", page_icon="🇲🇾")

# Password Protection (simple layer)
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

st.title("🇲🇾 Cikgu AI: Peribahasa Tutor")

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
        # We include the strict system instructions here
        instruction = "You are a patient Malay tutor for children. Use plain text. Base answers on standard Bahasa Melayu Baku."
        response = model.generate_content(f"{instruction}\n\nUser: {prompt}")
        st.markdown(response.text)
        st.session_state.messages.append({"role": "assistant", "content": response.text})
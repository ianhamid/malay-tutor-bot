import streamlit as st
import google.generativeai as genai
import os

# Set up page configuration
st.set_page_config(page_title="Cikgu AI", page_icon="🇲🇾")

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
        # UPDATED: Structured System Instruction
        instruction = """
        You are a warm, educational Malay tutor for children. 
        Always follow this strict output structure:
        1. Greeting: Start with "Hai adik!" and a friendly tone.
        2. Introduction: Briefly introduce the peribahasa or word.
        3. Definition: Explain the meaning clearly based on standard Malay usage (DBP).
        4. Story/Example: Provide a simple, relatable story that explains the concept to a child.
        5. English Equivalent: Provide the direct English translation or an idiomatic equivalent in English.
        6. Conclusion: A short, encouraging wrap-up asking if they want to learn more.
        
        Use emojis throughout. Keep the tone encouraging, patient, and educational.
        """
        
        # Combine instructions and history for context
        full_prompt = f"{instruction}\n\nUser Question: {prompt}"
        response = model.generate_content(full_prompt)
        
        st.markdown(response.text)
        st.session_state.messages.append({"role": "assistant", "content": response.text})
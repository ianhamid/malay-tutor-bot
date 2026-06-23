import streamlit as st
import os
import logging
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

st.set_page_config(page_title="Madam K", page_icon="🇲🇾")

# Configure Gemini API (same as bot)
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

SYSTEM_INSTRUCTION = """You are a warm, friendly Bahasa Melayu tutor.
- Concise responses with emojis
- Use DBP (Dewan Bahasa dan Pustaka) standard definitions
- Explain Peribahasa simply for learners
- Plain text only (NO markdown symbols)"""

# Initialize model (sync, like bot)
model = genai.GenerativeModel(
    model_name='gemini-2.5-flash',
    system_instruction=SYSTEM_INSTRUCTION,
    generation_config={"temperature": 0.1}
)

def get_tutor_response(prompt):
    """Get Malay tutor response (sync, not streaming)."""
    return model.generate_content(prompt)

st.title("Madam K")

if prompt := st.chat_input("Apa maksud buntal...?"):
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            response = get_tutor_response(prompt)
            st.markdown(response.text)
            logger.info(f"Response sent: {len(response.text)} chars")
        except Exception as e:
            logger.error(f"Error: {type(e).__name__}: {str(e)}")
            st.error(f"⚠️ {type(e).__name__}: {str(e)}")
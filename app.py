import streamlit as st
import os
import logging
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

st.set_page_config(page_title="Madam K", page_icon="🇲🇾")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Configure Gemini API (same as bot)
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

SYSTEM_INSTRUCTION = """You are an excellent Bahasa Melayu language teacher (Guru Bahasa Melayu).

Your role:
1. Teach proper Bahasa Melayu Baku (standard Malay)
2. Explain grammar, sentence structure, vocabulary, idioms, proverbs
3. Provide examples of phrases (frasa) for oral (lisan) and written (bertulis) contexts
4. Explain budi bahasa (good manners/politeness in language) with examples
5. Answer any Malay language learning questions - vocabulary, conjugation, pronunciation, usage
6. For Peribahasa: explain meaning, give story examples, suggest English equivalents

Format:
- Use emojis to make learning fun
- Keep explanations clear and simple
- Use bullet points or numbered lists when appropriate
- Provide practical examples students can use
- Plain text only (NO markdown symbols like * or _)
- Encourage and be patient with learners

You are NOT limited to idioms - teach comprehensive Bahasa Melayu language skills."""

# Initialize model (sync, like bot)
model = genai.GenerativeModel(
    model_name='gemini-2.5-flash',
    system_instruction=SYSTEM_INSTRUCTION,
    generation_config={"temperature": 0.1}
)

def get_tutor_response(prompt):
    """Get Malay tutor response (sync, not streaming)."""
    return model.generate_content(prompt)

st.title("Madam K 🇲🇾")
st.markdown("*Your Bahasa Melayu Teacher*")

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Handle new messages
if prompt := st.chat_input("Soalan apa? / What's your question?"):
    # Add user message to history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)

    # Get and display response
    with st.chat_message("assistant"):
        try:
            response = get_tutor_response(prompt)
            response_text = response.text
            st.markdown(response_text)
            
            # Add assistant response to history
            st.session_state.messages.append({"role": "assistant", "content": response_text})
            logger.info(f"Response sent: {len(response_text)} chars")
        except Exception as e:
            logger.error(f"Error: {type(e).__name__}: {str(e)}")
            st.error(f"⚠️ {type(e).__name__}: {str(e)}")
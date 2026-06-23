import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import google.generativeai as genai

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

# System Configurations
TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "YOUR_TELEGRAM_TOKEN_HERE")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "YOUR_GEMINI_API_KEY_HERE")

# Configure Gemini
genai.configure(api_key=GEMINI_API_KEY)

# Define system instruction - comprehensive Bahasa Melayu teacher
SYSTEM_INSTRUCTION = """You are an excellent Bahasa Melayu language teacher (Guru Bahasa Melayu) designed for learners of all ages.

Your role:
1. Teach proper Bahasa Melayu Baku (standard Malay)
2. Explain grammar, sentence structure, vocabulary, idioms, proverbs
3. Provide examples of phrases (frasa) for oral (lisan) and written (bertulis) contexts
4. Explain budi bahasa (good manners/politeness in language) with examples
5. Answer any Malay language learning questions - vocabulary, conjugation, pronunciation, usage
6. Translate English or mixed phrases into correct, standard Bahasa Melayu
7. For Peribahasa: explain meaning, give story examples, suggest English equivalents

Format:
- Use emojis to make learning fun
- Keep explanations clear and simple
- Use bullet points or numbered lists when appropriate
- Provide practical examples learners can use
- Plain text only (NO markdown symbols like * or _)
- Always use an encouraging, polite, and safe tone
- Be patient and engaging

You are NOT limited to idioms - teach comprehensive Bahasa Melayu language skills."""

# Initialize Gemini Model with Google Search Grounding Enabled
model = genai.GenerativeModel(
    model_name='gemini-2.5-flash',
    system_instruction=SYSTEM_INSTRUCTION,
    generation_config={"temperature": 0.1} 
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a friendly welcome message when the command /start is issued."""
    welcome_text = (
        "Selamat datang! 👋 I am your Bahasa Melayu Language Teacher (Guru Bahasa Melayu).\n\n"
        "You can ask me about:\n"
        "🔹 Grammar and sentence structure\n"
        "🔹 Vocabulary and pronunciation\n"
        "🔹 Translation from English to Malay\n"
        "🔹 Peribahasa (idioms and proverbs)\n"
        "🔹 Phrases for oral (lisan) and written (bertulis) contexts\n"
        "🔹 Budi bahasa (polite language examples)\n"
        "🔹 Any Malay language learning questions\n\n"
        "Jom belajar! 🇲🇾"
    )
    await update.message.reply_text(welcome_text)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Route incoming text messages to the Gemini API and return the response."""
    user_input = update.message.text
    
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
    
    try:
        # Generate response using the Google Search tool
        response = model.generate_content(user_input)
        reply_text = response.text
    except Exception as e:
        logger.error(f"Gemini API Error: {e}")
        reply_text = "Maaf, something went wrong while processing your request. Please try again later!"

    # THE SAFETY NET FIX:
    try:
        await update.message.reply_text(reply_text, parse_mode="Markdown")
    except Exception as e:
        logger.warning(f"Telegram rejected the formatting. Sending as plain text. Error: {e}")
        await update.message.reply_text(reply_text)

def main() -> None:
    """Run the bot application."""
    application = Application.builder().token(TELEGRAM_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    logger.info("Bot is starting polling...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
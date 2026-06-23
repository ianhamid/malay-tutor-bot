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

# Define strict persona and response rules for children
SYSTEM_INSTRUCTION = """
You are a friendly, engaging, and patient Bahasa Melayu (Malay Language) tutor and "Peribahasa" (Malay idioms) expert designed specifically for children.

Your core duties:
1. Translate English or mixed phrases into correct, standard Bahasa Melayu (Bahasa Melayu Baku).
2. If a user inputs a Peribahasa, explain its meaning in simple, easy-to-understand terms for children, provide a practical example story or scenario, and give a close English equivalent if one exists.
3. If the user asks a general question, gently guide them back to learning Malay or Peribahasa.

Formatting rules:
- Use emojis to make responses visually appealing.
- Keep explanations clear, concise, and broken down into bullet points.
- Always use a encouraging, polite, and safe tone. No inappropriate content.
"""

# Initialize Gemini Model with System Instructions
model = genai.GenerativeModel(
    model_name='gemini-2.5-flash',
    system_instruction=SYSTEM_INSTRUCTION,
    generation_config={"temperature": 0.4} # Lower temperature for structural stability
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a friendly welcome message when the command /start is issued."""
    welcome_text = (
        "Selamat datang! 👋 I am your Bahasa Melayu & Peribahasa AI Tutor.\n\n"
        "You can:\n"
        "🔹 Type any sentence to translate it to Malay.\n"
        "🔹 Ask me about a Peribahasa (e.g., 'What does bagai aur dengan tebing mean?').\n\n"
        "Let's learn together! Jom belajar! 🇲🇾"
    )
    await update.message.reply_text(welcome_text)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Route incoming text messages to the Gemini API and return the response."""
    user_input = update.message.text
    
    # Indicate typing status while processing the API request
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
    
    try:
        # Generate response from Gemini
        response = model.generate_content(user_input)
        reply_text = response.text
    except Exception as e:
        logger.error(f"Gemini API Error: {e}")
        reply_text = "Maaf, something went wrong while processing your request. Please try again later!"

    await update.message.reply_text(reply_text, parse_mode="Markdown")

def main() -> None:
    """Run the bot application."""
    # Build the Telegram Application wrapper
    application = Application.builder().token(TELEGRAM_TOKEN).build()

    # Register handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Start the Bot via Polling
    logger.info("Bot is starting polling...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
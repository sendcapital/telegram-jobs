import logging
from telegram import Update
from telegram.ext import filters, MessageHandler, ContextTypes

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I didn't understand that command.")

# Add unknown handler to reply to all commands that were not recognized by the previous handlers
unknown_handler = MessageHandler(filters.COMMAND, unknown)
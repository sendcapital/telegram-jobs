import logging
from telegram import  InlineKeyboardButton, InlineKeyboardMarkup, Update
from typing import Any, Dict, Tuple
from telegram.ext import filters, CommandHandler, MessageHandler, ContextTypes,  ConversationHandler
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

END = ConversationHandler.END



async def markdown(update:Update, context: ContextTypes.DEFAULT_TYPE) -> int:
  """Retrieves and returns the latest job information based on user's entries and end."""
  await context.bot.send_message(chat_id=update.effective_chat.id, 
                                   text="*_bold and italic_*",
                                   parse_mode="MarkdownV2")
  return END
  
markdown_handler = CommandHandler("markdown", markdown)


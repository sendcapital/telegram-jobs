import logging
from uuid import uuid4
from typing import Any, Dict, Tuple
from telegram import __version__ as TG_VER
try:
  from telegram import __version_info__
except ImportError:
  __version_info__ = (0, 0, 0, 0, 0)  # type: ignore[assignment]

if __version_info__ < (20, 0, 0, "alpha", 5):
  raise RuntimeError(
      f"This example is not compatible with your current PTB version {TG_VER}. To view the "
      f"{TG_VER} version of this example, "
      f"visit https://docs.python-telegram-bot.org/en/v{TG_VER}/examples.html"
  )
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
  CallbackQueryHandler,
  CommandHandler,
  ContextTypes,
  ConversationHandler,
  MessageHandler,
  filters,
)

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

EMPLOYMENT, QUERY, ROLE, LOCATION, BIO = range(5)
END = ConversationHandler.END

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
  """Starts the conversation and asks the user about their employment status."""
  reply_keyboard = [["Yes", "No"]]

  await update.message.reply_text(
      "Hi! My name is fired Bot. I'm here to find a job for you so that you do not become like me "
      "Send /cancel to stop talking to me.\n\n"
      "Are you looking for a job?",
      reply_markup=ReplyKeyboardMarkup(
          reply_keyboard, one_time_keyboard=True, input_field_placeholder="Yes or No?"
      ),
  )

  return EMPLOYMENT

async def employment(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
  """Stores the selected employment status and asks for a search query"""
  user = update.message.from_user
  logger.info("Seeking employment for %s: %s", user.first_name, update.message.text)
  context.user_data["Employment"] = update.message.text
  await update.message.reply_text("What is the ideal job that you are searching for?")
  return QUERY


async def query(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
  """Stores the selected employment status and asks for a role."""
  reply_keyboard = [["Full-Time", "Part-Time","Internship"]]
  user = update.message.from_user
  logger.info("Seeking ideal job for %s: %s", user.first_name, update.message.text)
  context.user_data["Query"] = update.message.text
  await update.message.reply_text(
      "I see! What is your ideal role? "
      "So I know what you are searching for, or send /skip if you don't want to.",
      reply_markup=ReplyKeyboardMarkup(
          reply_keyboard, one_time_keyboard=True 
      ),
  )

  return ROLE

async def role(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
  """Stores the Role and asks for a location."""
  user = update.message.from_user
  logger.info("Role seeked by %s: %s", user.first_name, update.message.text)
  context.user_data["Role"] = update.message.text
  await update.message.reply_text(
      "Gorgeous! Now, send me your location please, or send /skip if you don't want to."
  )

  return LOCATION

async def skip_role(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
  """Skips the role and asks for a location."""
  user = update.message.from_user
  logger.info("User %s did not send a role.", user.first_name)
  await update.message.reply_text(
      "I bet you look great! Now, send me your location please, or send /skip."
  )

  return LOCATION


async def location(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
  """Stores the location and asks for some info about the user."""
  user = update.message.from_user
  logger.info("Location of %s: %s", user.first_name, update.message.text)
  context.user_data["Location"] = update.message.text
  await update.message.reply_text(
      "Maybe I can visit you sometime! At last, tell me something about yourself."
  )

  return BIO


async def skip_location(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
  """Skips the location and asks for info about the user."""
  user = update.message.from_user
  logger.info("User %s did not send a location.", user.first_name)
  await update.message.reply_text(
      "You seem a bit paranoid! At last, tell me something about yourself."
  )

  return BIO


async def bio(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
  """Stores the info about the user and ends the conversation."""
  user = update.message.from_user
  logger.info("Bio of %s: %s", user.first_name, update.message.text)
  context.user_data["Bio"] = update.message.text
  await update.message.reply_text("Thank you! You may now proceed to run /jobs to search for jobs in your area")
  return END


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
  """Cancels and ends the conversation."""
  user = update.message.from_user
  logger.info("User %s canceled the conversation.", user.first_name)
  await update.message.reply_text(
      "Bye! I hope we can talk again some day.", reply_markup=ReplyKeyboardRemove()
  )

  return END
  

# Add conversation handler with the states EMPLOYMENT, ROLE, LOCATION and BIO
query_handler = ConversationHandler(
    entry_points=[CommandHandler("start", start)],
    states={
        EMPLOYMENT: [MessageHandler(filters.Regex("^(Yes|No)$"), employment)],
        # RESUME: [MessageHandler(filters.Document.ALL, resume), CommandHandler("skip", skip_resume)],
        QUERY: [MessageHandler(filters.TEXT & ~filters.COMMAND, query)],
        ROLE: [MessageHandler(filters.TEXT & ~filters.COMMAND, role), CommandHandler("skip", skip_role)],
        LOCATION: [MessageHandler(filters.TEXT & ~filters.COMMAND, location), CommandHandler("skip", skip_location)],
        BIO: [MessageHandler(filters.TEXT & ~filters.COMMAND, bio)],      
    },
    fallbacks=[CommandHandler("cancel", cancel)],
)



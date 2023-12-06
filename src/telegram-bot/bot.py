import os
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
from telegram import Update
from telegram.ext import Application
from handlers import query_handler, jobs_handler, unknown_handler, markdown_handler

from dotenv import load_dotenv

load_dotenv() 

TOKEN = os.getenv("TOKEN")

def main() -> None:
    """Run the bot."""
    # Create the Application and pass it your bot's token.
    
    application = Application.builder().token(TOKEN).build()
    application.add_handler(query_handler)
    application.add_handler(jobs_handler)
    application.add_handler(markdown_handler)

    # last handler 
    application.add_handler(unknown_handler)
    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
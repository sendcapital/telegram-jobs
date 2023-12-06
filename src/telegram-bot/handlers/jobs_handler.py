import logging
from telegram import  InlineKeyboardButton, InlineKeyboardMarkup, Update
from typing import Any, Dict, Tuple
from telegram.ext import filters, CommandHandler, MessageHandler, ContextTypes,  ConversationHandler
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
# module to launch job search
import <launch> 

# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

END = ConversationHandler.END

def data_to_str(user_data: Dict[str, str]) -> str:
  """Helper function for formatting the gathered user info."""
  facts = [f"{key} - {value}" for key, value in user_data.items()]
  return "\n".join(facts).join(["\n", "\n"])


class postFactory():
  
  def __init__(self):
    self.posts = []
    self.post_template: str = (
    "• *Job Title* : {} \n"
    "• *Company* : {} \n"
    "• *Location* : {} \n"
    "• *Job Link* : {} \n"
    )
  
  def generate(self, jobs_data):
    for index, job in jobs_data.iterrows():
      post = {
        "job_details": 
          f"• *Job Title* : {job['job-title']}\n"
          f"• *Company* : {job['company']}\n"
          f"• *Location* : {job['date_posted']}\n"
          f"• *Job Link* : [LINK 🔗]({job['link']})",
        "job_link": job["link"],
      }
      self.posts.append(post)
    print('generated')

class InlineKeyboardCreator:
    def __init__(self, keyboard: dict[str, str], row_width: int = 1) -> None:
        self.kb = keyboard
        self.width = row_width

    def create_kb(self) -> InlineKeyboardMarkup:
        kb = InlineKeyboardMarkup()

        kb.row_width(self.width)

        for text, link in self.kb.items():
            kb.add(InlineKeyboardButton(text=text, link=link))
        return kb

def jobs_post_inline_kb(job_link: str) -> InlineKeyboardMarkup:
    inline_kb = InlineKeyboardMarkup()
    inline_kb.row_width = 1
    inline_kb.add(
        InlineKeyboardButton("👆 Click Here To Apply 👆", url=job_link),
    )
    return inline_kb

async def jobs(update:Update, context: ContextTypes.DEFAULT_TYPE) -> int:
  """Retrieves and returns the latest job information based on user's entries and end."""
  user_info = data_to_str(context.user_data)
  user_data = context.user_data
  query = user_data['Query']
  role = user_data['Role']
  location = user_data['Location']
  job_data =  await launch(query, role, location)
  postings = postFactory()
  postings.generate(job_data)
  for post in postings.posts:
    await context.bot.send_message(chat_id=update.effective_chat.id, 
                                   text=post,
                                   parse_mode="MarkdownV2")
  return END
  
jobs_handler = CommandHandler("jobs",jobs)

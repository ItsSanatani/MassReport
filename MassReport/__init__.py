from pyrogram import Client
from .config import API_ID, API_HASH, BOT_TOKEN

app = Client(
    "mass_report_bot",
    bot_token=BOT_TOKEN,
    api_id=API_ID,
    api_hash=API_HASH
)

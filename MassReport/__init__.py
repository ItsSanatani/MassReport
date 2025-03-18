import logging
from pyrogram import Client
from config import API_ID, API_HASH, BOT_TOKEN

# Setup Logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    handlers=[
        logging.FileHandler("mass_report.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)
logger.info("Initializing Mass Report Bot...")

app = Client(
    "mass_report_bot",
    bot_token=BOT_TOKEN,
    api_id=API_ID,
    api_hash=API_HASH
)

logger.info("Mass Report Bot Initialized Successfully!")

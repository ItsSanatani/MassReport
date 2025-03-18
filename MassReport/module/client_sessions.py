from pyrogram import Client
from config import API_ID, API_HASH, SESSION_STRINGS
import logging

logger = logging.getLogger(__name__)

clients = []

for idx, session_str in enumerate(SESSION_STRINGS, start=1):
    try:
        client = Client(
            f"session_{idx}",
            api_id=API_ID,
            api_hash=API_HASH,
            session_string=session_str
        )
        clients.append(client)
        logger.info(f"Successfully loaded session: session_{idx}")
    except Exception as e:
        logger.error(f"Failed to load session_{idx}: {e}")

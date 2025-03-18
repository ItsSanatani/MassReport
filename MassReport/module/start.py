import logging
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from MassReport.module import report
from MassReport import app
from MassReport.database import database

@app.on_message(filters.command("start") & filters.private)
async def start_command(client, message):
    user_id = message.from_user.id
    username = message.from_user.username or "None"
    language = message.from_user.language_code or "unknown"

    await database.add_user(user_id, username, language)

    buttons = [
        [InlineKeyboardButton("➕ Start Reporting", callback_data="start_report")]
    ]

    # Logging System Message
    log_text = f"""
New User Started Bot!

👤 User: [{message.from_user.first_name}](tg://user?id={user_id})

🆔 Username: @{username}

🌐 Language: {language}
"""
    # Send log to your log channel (optional)
    LOG_CHANNEL = -1002640038102  # Replace with your log channel ID
    try:
        await app.send_message(LOG_CHANNEL, log_text, disable_web_page_preview=True)
    except Exception as e:
        logger.warning(f"Failed to log user: {e}")

    await message.reply_photo(
        photo="https://files.catbox.moe/31g9nf.jpg",
        caption="**Welcome to Mass Report Bot!**\n\nClick the button below to start reporting.",
        reply_markup=InlineKeyboardMarkup(buttons)
    )

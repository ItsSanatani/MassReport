from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from MassReport import app

@app.on_message(filters.command("start") & filters.private)
async def start_command(client, message):
    buttons = [
        [InlineKeyboardButton("➕ Start Reporting", callback_data="start_report")]
    ]
    await message.reply_photo(
        photo="https://files.catbox.moe/31g9nf.jpg",  # Put your image URL here
        caption="**Welcome to Mass Report Bot!**\n\nClick the button below to start reporting.",
        reply_markup=InlineKeyboardMarkup(buttons)
    )

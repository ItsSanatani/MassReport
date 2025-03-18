import logging
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from MassReport.module import report
from MassReport import app

# लॉगिंग कॉन्फ़िगरेशन
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(name)s - %(message)s',
    handlers=[
        logging.FileHandler('mass_report_bot.log'),  # लॉग फ़ाइल का नाम
        logging.StreamHandler()  # कंसोल पर भी लॉग दिखाए
    ]
)
logger = logging.getLogger(__name__)

@app.on_message(filters.command("start") & filters.private)
async def start_command(client, message):
    buttons = [
        [InlineKeyboardButton("➕ Start Reporting", callback_data="start_report")]
    ]
    await message.reply_photo(
        photo="https://files.catbox.moe/31g9nf.jpg",  # अपनी इमेज URL यहाँ डालें
        caption="**Welcome to Mass Report Bot!**\n\nClick the button below to start reporting.",
        reply_markup=InlineKeyboardMarkup(buttons)
    )
    # लॉगिंग: नए उपयोगकर्ता ने बॉट शुरू किया
    user = message.from_user
    logger.info(
        f"New User Started Bot!\n\n"
        f"👤 User: [{user.first_name}](tg://user?id={user.id})\n"
        f"🆔 Username: @{user.username}\n"
        f"🌐 Language: {user.language_code}"
    )

if __name__ == "__main__":
    logger.info("Starting Mass Report Bot...")
    app.run()

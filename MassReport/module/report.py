import logging
from pyrogram import filters, errors
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.raw.functions.account import ReportPeer
from pyrogram.raw.types import *
import asyncio
from MassReport import app
from MassReport.database import database
from MassReport.module.client_sessions import clients

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

REASON_MAP = {
    "1": ("Spam", InputReportReasonSpam),
    "2": ("Child Abuse", InputReportReasonChildAbuse),
    "3": ("Violence", InputReportReasonViolence),
    "4": ("Illegal Drugs", InputReportReasonIllegalDrugs),
    "5": ("Pornography", InputReportReasonPornography),
    "6": ("Personal Details", InputReportReasonPersonalDetails),
    "7": ("Geo Irrelevant", InputReportReasonGeoIrrelevant),
    "8": ("Copyright", InputReportReasonCopyright),
    "9": ("Other", InputReportReasonOther)
}

@app.on_message(filters.command("report") & filters.private)
async def report_command(client, message):
    logger.info(f"User {message.from_user.id} initiated report.")
    await initiate_report_process(message.from_user.id, message)

@app.on_callback_query(filters.regex(r"^start_report$"))
async def start_report_callback(client, callback_query):
    logger.info(f"User {callback_query.from_user.id} clicked start report button.")
    await initiate_report_process(callback_query.from_user.id, callback_query.message)

async def initiate_report_process(user_id, message):
    # Await the async database method
    await database.set_user_data(user_id, {"step": "awaiting_target"})
    logger.info(f"User {user_id}: Awaiting target group/channel link.")
    await message.reply_text(
        "**Mass Report Initiated!**\n\n"
        "Please send me the **Target Group/Channel Link**:"
    )

@app.on_message(filters.private & filters.text)
async def handle_steps(client, message):
    user_id = message.from_user.id
    # Await the async database method
    data = await database.get_user_data(user_id)  
    step = data.get("step")

    if step == "awaiting_target":
        data["target"] = message.text.strip()
        data["step"] = "awaiting_message_link"
        await database.set_user_data(user_id, data)
        logger.info(f"User {user_id}: Provided target link: {data['target']}")
        await message.reply_text("Now send me the **Message Link** (Target Message to report):")
        return

    if step == "awaiting_message_link":
        data["message_link"] = message.text.strip()
        data["step"] = "awaiting_reason"
        await database.set_user_data(user_id, data)
        logger.info(f"User {user_id}: Provided message link: {data['message_link']}")

        buttons = [
            [InlineKeyboardButton(f"{key}. {val[0]}", callback_data=f"reason_{key}")]
            for key, val in REASON_MAP.items()
        ]
        await message.reply_text(
            "**Select Report Reason:**",
            reply_markup=InlineKeyboardMarkup(buttons)
        )
        return

    if step == "awaiting_count":
        try:
            count = int(message.text.strip())
            data["count"] = count
            await database.set_user_data(user_id, data)
            logger.info(f"User {user_id}: Provided count: {count}")
            await message.reply_text(f"**Starting Mass Report...**")
            await start_reporting(client, message, data)
        except ValueError:
            logger.warning(f"User {user_id}: Invalid count input.")
            await message.reply_text("Please send a valid number for count!")
        return

@app.on_callback_query(filters.regex(r"^reason_\d+$"))
async def reason_selected(client, callback_query):
    user_id = callback_query.from_user.id
    reason_num = callback_query.data.split("_")[1]
    reason_tuple = REASON_MAP.get(reason_num)

    if not reason_tuple:
        logger.warning(f"User {user_id}: Selected invalid reason.")
        await callback_query.answer("Invalid Reason!", show_alert=True)
        return

    data = await database.get_user_data(user_id)
    data["reason"] = reason_tuple[1]
    data["step"] = "awaiting_count"
    await database.set_user_data(user_id, data)
    logger.info(f"User {user_id}: Selected reason {reason_tuple[0]}")
    await callback_query.message.edit_text(f"Selected Reason: **{reason_tuple[0]}**\n\nNow send me **Report Count**:")

async def start_reporting(client, message, data):
    target_link = data["target"]
    message_link = data["message_link"]
    reason = data["reason"]()
    count = data["count"]

    username = target_link.split("/")[-1]
    msg_id = int(message_link.split("/")[-1])

    logger.info(f"Starting mass reporting on {username} message {msg_id} for {count} times.")

    success, failed = 0, 0

    for i in range(count):
        for session_client in clients:
            try:
                await session_client.start()
                logger.info(f"Session {session_client.name}: Started.")

                try:
                    await session_client.join_chat(username)
                    logger.info(f"Session {session_client.name}: Joined {username}")
                except errors.UserAlreadyParticipant:
                    logger.info(f"Session {session_client.name}: Already in {username}")
                except Exception as e:
                    logger.error(f"Session {session_client.name}: Join error: {e}")

                peer = await session_client.resolve_peer(username)

                await session_client.invoke(
                    ReportPeer(
                        peer=peer,
                        reason=reason,
                        message=f"Reported message {msg_id}"
                    )
                )
                logger.info(f"Session {session_client.name}: Successfully reported.")
                success += 1

            except errors.FloodWait as e:
                logger.warning(f"Session {session_client.name}: FloodWait {e.value} sec. Sleeping.")
                await asyncio.sleep(e.value)
                failed += 1
            except Exception as e:
                logger.error(f"Session {session_client.name}: Reporting Error: {e}")
                failed += 1
            finally:
                await session_client.stop()
                logger.info(f"Session {session_client.name}: Stopped.")
        await asyncio.sleep(1)

    logger.info(f"Mass Reporting Completed! Success: {success} | Failed: {failed}")

    await message.reply_text(
        f"✅ **Mass Reporting Completed!**\n\n"
        f"**Successful Reports:** {success}\n"
        f"**Failed Reports:** {failed}"
    )
    await database.clear_user_data(message.from_user.id)
    logger.info(f"User {message.from_user.id}: Cleared session data.")

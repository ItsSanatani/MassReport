import motor.motor_asyncio
import logging

logger = logging.getLogger(__name__)

MONGO_URL = "mongodb+srv://Radheee:sanatani@cluster0.sgop4.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URL)
db = client["MassReportDB"]
users = db["users"]

async def add_user(user_id, username, language):
    user = await users.find_one({"user_id": user_id})
    if not user:
        await users.insert_one({
            "user_id": user_id,
            "username": username,
            "language": language
        })
        logger.info(f"Added New User -> ID: {user_id}, Username: @{username}, Lang: {language}")
    else:
        logger.info(f"User Already Exists -> ID: {user_id}")

async def get_user(user_id):
    user = await users.find_one({"user_id": user_id})
    logger.info(f"Fetching data for user_id: {user_id} | Data: {user}")
    return user

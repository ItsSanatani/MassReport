import motor.motor_asyncio
import logging

# Initialize logger
logger = logging.getLogger(__name__)

# MongoDB connection details
MONGO_URL = "mongodb+srv://Radheee:sanatani@cluster0.sgop4.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
DATABASE_NAME = "MassReportDB"

# Initialize MongoDB client
client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URL)
db = client[DATABASE_NAME]
users_collection = db["users"]

# Function to add a new user
async def add_user(user_id: int, username: str, language: str):
    user = await users_collection.find_one({"user_id": user_id})
    if user:
        logger.info(f"User already exists: user_id={user_id}")
    else:
        new_user = {
            "user_id": user_id,
            "username": username,
            "language": language,
            "reports": [],
            "step": "awaiting_target",  # Initialize with default step
        }
        await users_collection.insert_one(new_user)
        logger.info(f"New user added: user_id={user_id}, username={username}, language={language}")

# Function to retrieve user data
async def get_user_data(user_id: int):
    user = await users_collection.find_one({"user_id": user_id})
    if user:
        logger.info(f"User data retrieved: user_id={user_id}")
        return user
    else:
        logger.info(f"No data found for user_id={user_id}")
        # Return an empty dictionary with a default step if no data exists
        return {"step": "awaiting_target"}

# Function to update or set user data
async def set_user_data(user_id: int, data: dict):
    result = await users_collection.update_one(
        {"user_id": user_id},
        {"$set": data},
        upsert=True  # If the user doesn't exist, create a new document
    )
    if result.modified_count > 0 or result.upserted_id:
        logger.info(f"User data updated: user_id={user_id}")
    else:
        logger.warning(f"Failed to update user data for user_id={user_id}")

# Function to add a report to a user's record
async def add_report(user_id: int, report_data: dict):
    result = await users_collection.update_one(
        {"user_id": user_id},
        {"$push": {"reports": report_data}}
    )
    if result.modified_count > 0:
        logger.info(f"Report added for user_id={user_id}")
    else:
        logger.warning(f"Failed to add report for user_id={user_id}")

# Function to clear user data after report completion
async def clear_user_data(user_id: int):
    result = await users_collection.update_one(
        {"user_id": user_id},
        {"$unset": {"step": "", "target": "", "message_link": "", "reason": "", "count": ""}}  # Unset all steps data
    )
    if result.modified_count > 0:
        logger.info(f"User data cleared for user_id={user_id}")
    else:
        logger.warning(f"Failed to clear user data for user_id={user_id}")

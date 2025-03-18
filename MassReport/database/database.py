import logging

logger = logging.getLogger(__name__)

user_data = {}

def get_user_data(user_id):
    data = user_data.get(user_id, {})
    logger.info(f"Fetching data for user_id: {user_id} | Data: {data}")
    return data

def set_user_data(user_id, data):
    user_data[user_id] = data
    logger.info(f"Setting data for user_id: {user_id} | Data: {data}")

def clear_user_data(user_id):
    removed = user_data.pop(user_id, None)
    if removed:
        logger.info(f"Cleared data for user_id: {user_id}")
    else:
        logger.info(f"No data found to clear for user_id: {user_id}")

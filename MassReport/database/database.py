user_data = {}

def get_user_data(user_id):
    return user_data.get(user_id, {})

def set_user_data(user_id, data):
    user_data[user_id] = data

def clear_user_data(user_id):
    user_data.pop(user_id, None)

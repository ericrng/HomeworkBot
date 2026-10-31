from db import get_data_by_value, get_specific_data, delete_specific_data, insert_specific_data
from datetime import datetime as dt

def get_settings(user_id):
    user_settings = get_data_by_value("user_settings", "user_id", user_id)
    if user_settings:
        return user_settings[0][1], user_settings[0][2], user_settings[0][3]
    else:
        insert_specific_data("user_settings", "user_id", user_id)
        return False, False, False

def auto_delete_function(status, user_id):
    if status:
        output = get_specific_data("homework_data", "due_date", user_id, "user_id")
        if not output:
            pass
        else:
            for dates in output:
                if dt.strptime(dates, "%m/%d/%Y") < dt.now():
                    delete_specific_data("homework_data", output, "due_date")
    else:
        pass
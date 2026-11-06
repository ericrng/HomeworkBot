from db import get_data_by_value, delete_specific_data, insert_specific_data, get_column_by_value, insert_many_data, check_existence
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
        output = get_column_by_value("homework_data", "user_id", "due_date", user_id)
        if not output:
            pass
        else:
            for dates in output:
                if dt.strptime(dates[0], "%m/%d/%Y") < dt.now():
                    delete_specific_data("homework_data", dates[0], "due_date")
    else:
        pass


def auto_sync_function(status, columns, values):
    if status:
        insert_many_data("homework_data", columns, values)


def datetime_check(due_date):
    try:
        if dt.now() <= dt.strptime(due_date, "%m/%d/%Y"):
            return True
        else:
            return False
    except ValueError:
        return None

def check_add_hw_parameter():
    pass


# Used specifically for show commands. Checks for existence and inserts single value.
def check_single_insert(table, column, value):
    if not check_existence(table, column, value):
        insert_specific_data(table, column, value)
        return True
    else:
        return False


# Used specifically for delete commands. Checks for existence and deletes.
def check_single_delete(table, column, value):
    if check_existence(table, column, value):
        delete_specific_data(table, value, column)
        return True
    else:
        return False


def insert_periods(start, end):
    if not end > start >= 1:
        return False
    else:
        for i in range(start, end+1):
            check_single_insert("homework_data", "class_period", i)
        return True
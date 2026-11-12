from db import get_data_by_value, delete_specific_data, insert_specific_data, get_column_by_value, insert_many_data, \
    check_existence, get_all_data_in_column, get_all_data_in_table, get_dynamic_data
from datetime import datetime as dt


def get_settings(user_id):
    user_settings = get_data_by_value("user_settings", "user_id", user_id)
    if user_settings:
        return user_settings[0][1], user_settings[0][2], user_settings[0][3], user_settings[0][4]
    else:
        insert_specific_data("user_settings", "user_id", user_id)
        return False, False, False, False


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


def check_add_hw_parameter(period, class_name, class_teacher, due_date, data_col, val_col):
    # Checks due date.
    match datetime_check(due_date):
        case True:
            pass
        case False:
            return "You cannot have a due-date that is in the past!", False
        case None:
            return "Invalid due date format! *(Hint: m/d/yyyy)*", False
    # Checks if period, name, and teacher name are valid.
    if period not in get_all_data_in_table("valid_periods") or class_name not in get_all_data_in_column("valid_names", "class_name") or class_teacher not in get_all_data_in_column("valid_teachers", "class_teacher"):
        return "The parameters of this homework are not valid!", False
    # Checks for existence.
    elif get_dynamic_data("homework_data", data_col, val_col):
        return "This homework already exists!", False
    else:
        return "Successfully inserted homework!", True


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
            if check_single_insert("valid_periods", "class_period", i):
                pass
        return True


# Checks if the index of data (typically, the number of data you have implies a certain number of embed fields) is equal to the embed limit, which is variable.
def embed_lim_check(embed_limit, num_of_data, data):
    if (num_of_data + 1) % embed_limit == 0:
        return True
    elif (num_of_data + 1) == len(data):
        return True
    else:
        return False


def whitelist_check(whitelist, data):
    if data == whitelist:
        return True
    else:
        return False


def dynamic_insert_delete(whitelist_status, cmd_type, table, column, value):
    if whitelist_status:
        if cmd_type == "insert":
            if check_single_insert(table, column, value):
                return f"Successfully inserted {column} {value}!"
            else:
                return f"A value already exists for {column} {value}!"
        else:
            if check_single_delete(table, column, value):
                return f"Successfully deleted {column} {value}!"
            else:
                return f"No value exists for {column} {value}!"
    else:
        return "You do not have permission to use this command!"
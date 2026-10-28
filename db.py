import psycopg2
import os
from dotenv import load_dotenv
from psycopg2.extras import execute_batch, execute_values
from psycopg2 import sql

load_dotenv(override=True)
# IF YOU ARE NOT USING A DATABASE URL
DB_NAME = str(os.getenv("DB_NAME"))
PASSWORD = str(os.getenv("PASSWORD"))
USERNAME = str(os.getenv("USERNAME"))
HOST = str(os.getenv("HOST"))
DB_URL = str(os.getenv("DB_URL"))
conn = psycopg2.connect(dbname=DB_NAME, user=USERNAME, password=PASSWORD, host=HOST)
cur = conn.cursor()

# Need to check against to prevent SQL injections.
VALID_TABLES = {"user_data", "homework_data", "valid_periods", "valid_names", "valid_teachers", "user_settings"}
VALID_COLUMNS = {"user_id", "class_name", "class_period", "class_teacher", "homework_name", "homework_status", "due_date", "auto_sync", "auto_delete"}


# Structure for future use.
cur.execute("""CREATE TABLE IF NOT EXISTS user_data (
               user_id BIGINT PRIMARY KEY,
               class_period INT,
               class_teacher VARCHAR(100),
               class_name VARCHAR(100)
    );""")

cur.execute("""CREATE TABLE IF NOT EXISTS homework_data (
               user_id BIGINT,
               class_period INT,
               class_teacher VARCHAR(100),
               class_name VARCHAR(100),
               homework_name VARCHAR(100),
               homework_status BOOLEAN DEFAULT FALSE,
               due_date VARCHAR(100)
    );""")

# auto_sync will automatically sync homework additions to your to-do list to other people's to-do lists.
# auto_delete will automatically get rid of any homework that is already past due.
cur.execute("""CREATE TABLE IF NOT EXISTS user_settings (
               user_id BIGINT PRIMARY KEY,
               auto_sync BOOLEAN DEFAULT FALSE,
               auto_delete BOOLEAN DEFAULT FALSE
               );""")

cur.execute("""CREATE TABLE IF NOT EXISTS valid_periods (
               class_period INT PRIMARY KEY);""")

cur.execute("""CREATE TABLE IF NOT EXISTS valid_teachers (
               class_teacher VARCHAR(100) PRIMARY KEY);""")

cur.execute("""CREATE TABLE IF NOT EXISTS valid_names (
               class_name VARCHAR(100) PRIMARY KEY);""")

conn.commit()


def connect_db():
    return conn, cur


def close_db():
    cur.close()
    conn.close()


# FOR CHECKING IF TABLE IS ONE I MADE.
def check_table_validity(table):
    if table in VALID_TABLES:
        return True
    else:
        return False

# FOR CHECKING IF COLUMN IS ONE I MADE.
def check_column_validity(column):
    if column in VALID_COLUMNS:
        return True
    else:
        return False


# Gets a specific piece of data using a reference column and a reference value.
def get_specific_data(table, column, unique_value, unique_column):
    if check_table_validity(table) and check_column_validity(column) and check_column_validity(unique_column):
        query = sql.SQL("SELECT {column} FROM {table} WHERE {unique_column} = %s;").format(table=sql.Identifier(table), column=sql.Identifier(column), unique_column=sql.Identifier(unique_column))
        cur.execute(query, (unique_value,))
        data = cur.fetchone()
        return data
    else:
        raise ValueError


# Gets whatever is in a table that matches the columns and values.
def get_dynamic_data(table, columns, values):
    for column in columns:
        if not check_column_validity(column):
            raise ValueError
    if not check_table_validity(table):
        raise ValueError
    else:
        col = sql.SQL(", ").join(sql.Identifier(elements) for elements in columns)
        val = sql.SQL(", ").join(sql.Placeholder() for elements in range(len(columns)))
        query = sql.SQL("SELECT ({columns}) FROM {table} WHERE ({columns}) = ({values})").format(table=sql.Identifier(table), columns=col, values=val)
        execute_batch(cur, query, values)
        record_data = cur.fetchmany(size=len(columns))
        return record_data


# Gets one value from one column from the table that matches the columns and values.
def get_singular_by_many(table, columns, values, singular_column):
    for column in columns:
        if not check_column_validity(column):
            raise ValueError
    if not check_table_validity(table):
        raise ValueError
    else:
        col = sql.SQL(", ").join(sql.Identifier(elements) for elements in columns)
        val = sql.SQL(", ").join(sql.Placeholder() for elements in range(len(columns)))
        query = sql.SQL("SELECT ({singular_column}) FROM {table} WHERE ({columns}) = ({values})").format(table=sql.Identifier(table), columns=col, values=val, singular_column=sql.Identifier(singular_column))
        execute_batch(cur, query, values)
        record_data = cur.fetchone()
        return record_data


# Gets all data in a column where it is equal to a value.
def get_data_by_value(table, column, value):
    if check_table_validity(table) and check_column_validity(column):
        query = sql.SQL("SELECT * FROM {table} WHERE {unique_column} = %s;").format(table=sql.Identifier(table), unique_column=sql.Identifier(column))
        cur.execute(query, (value,))
        data = cur.fetchall()
        return data
    else:
        raise ValueError


# Gets all the data in a column.
def get_all_data_in_column(table, column):
    if check_table_validity(table) and check_column_validity(column):
        query = sql.SQL("SELECT {column} FROM {table};").format(table=sql.Identifier(table), column=sql.Identifier(column))
        cur.execute(query)
        data = cur.fetchall()
        return data
    else:
        raise ValueError


# Gets all the data from a table.
def get_all_data_in_table(table):
    if check_table_validity(table):
        query = sql.SQL("SELECT * FROM {table};").format(table=sql.Identifier(table))
        cur.execute(query)
        data = cur.fetchall()
        return data
    else:
        raise ValueError


# Inserts a singular value to a column in a table.
def insert_specific_data(table, column, value):
    if check_table_validity(table) and check_column_validity(column):
        query = sql.SQL("INSERT INTO {table} ({column}) VALUES (%s);").format(table=sql.Identifier(table), column=sql.Identifier(column))
        cur.execute(query, (value,))
        conn.commit()
    else:
        raise ValueError


# Inserts multiple columns and values in a table.
def insert_many_data(table, columns, values):
    for column in columns:
        if not check_column_validity(column):
            raise ValueError
    if not check_table_validity(table):
        raise ValueError
    else:
        col = sql.SQL(", ").join(sql.Identifier(elements) for elements in columns)
        val = sql.SQL(", ").join(sql.Placeholder() for elements in range(len(columns)))
        query = sql.SQL("INSERT INTO {table} ({columns}) VALUES ({values})").format(table=sql.Identifier(table), columns=col, values=val)
        execute_batch(cur, query, values)
        conn.commit()


# Updates a specific columns value when it matches a reference value and reference column.
def update_specific_data(table, column, value, unique_value, unique_column):
    if check_table_validity(table) and check_column_validity(column) and check_column_validity(unique_column):
        query = sql.SQL("UPDATE {table} SET {column} = %s WHERE {unique_column} = %s;").format(table=sql.Identifier(table), column=sql.Identifier(column), unique_column=sql.Identifier(unique_column))
        cur.execute(query, (value, unique_value))
        conn.commit()
    raise ValueError


# Updates one specific column's value if it matches reference values and columns.
# However, it is quite rudimentary and requires specific formatting to work in this instance.
# Needs to be refactored in the future.
def update_singular_by_many(table, columns, values, unique_column):
    for column in columns:
        if not check_column_validity(column):
            raise ValueError
    if not check_table_validity(table):
        raise ValueError
    else:
        col = sql.SQL(", ").join(sql.Identifier(elements) for elements in columns)
        val = sql.SQL(", ").join(sql.Placeholder() for elements in range(len(columns)))
        query = sql.SQL("UPDATE {table} SET {unique_column} = %s WHERE ({columns}) = ({values})").format(table=sql.Identifier(table), columns=col, values=val, unique_column=sql.Identifier(unique_column))
        execute_batch(cur, query, values)
        conn.commit()


# Resets a columns value in a table if it matches a reference value and column.
def reset_specific_data(table, column, unique_value, unique_column):
    if check_table_validity(table) and check_column_validity(column) and check_column_validity(unique_column):
        query = sql.SQL("UPDATE {table} SET {column} = DEFAULT WHERE {unique_column} = %s;").format(table=sql.Identifier(table), column=sql.Identifier(column), unique_column=sql.Identifier(unique_column))
        cur.execute(query, (unique_value,))
        conn.commit()
    else:
        raise ValueError

# Resets multiple column values when it matches a reference value and column.
def reset_column(table, column):
    if check_table_validity(table) and check_column_validity(column):
        query = sql.SQL("UPDATE {table} SET {column} = DEFAULT;").format(table=sql.Identifier(table), column=sql.Identifier(column))
        cur.execute(query)
        conn.commit()
    else:
        raise ValueError


# Deletes a specific piece of data from a specific column.
def delete_specific_data(table, unique_value, unique_column):
    if check_table_validity(table) and check_column_validity(unique_column):
        query = sql.SQL("DELETE FROM {table} WHERE {unique_column} = %s;").format(table=sql.Identifier(table), unique_column=sql.Identifier(unique_column))
        cur.execute(query, (unique_value,))
        conn.commit()
    else:
        raise ValueError


# Deletes specifically where the reference values equal the reference columns in a table.
def delete_dynamic_data(table, columns, values):
    for column in columns:
        if not check_column_validity(column):
            raise ValueError
    if not check_table_validity(table):
        raise ValueError
    else:
        col = sql.SQL(", ").join(sql.Identifier(elements) for elements in columns)
        val = sql.SQL(", ").join(sql.Placeholder() for elements in range(len(columns)))
        query = sql.SQL("DELETE FROM {table} WHERE ({columns}) = ({values})").format(table=sql.Identifier(table), columns=col, values=val)
        execute_batch(cur, query, values)
        conn.commit()


# Checks if a specific column and value exist.
def check_existence(table, column, value):
    if check_table_validity(table) and check_column_validity(column):
        query = sql.SQL("SELECT * FROM {table} WHERE {column} = %s;").format(table=sql.Identifier(table), column=sql.Identifier(column))
        cur.execute(query, (value,))
        data = cur.fetchone()
        if data is None:
            return False
        else:
            return True
    else:
        return None
import psycopg2
import os
from dotenv import load_dotenv
load_dotenv(override=True)
DB_URL = str(os.getenv("DB_URL"))
PASSWORD = str(os.getenv("PASSWORD"))
USERNAME = str(os.getenv("USERNAME"))
HOST = str(os.getenv("HOST"))
conn = psycopg2.connect(host=HOST, dbname=DB_URL, user=USERNAME, password=PASSWORD)
cur = conn.cursor()

# Need to check against to prevent SQL injections.
VALID_TABLES = {"user_data", "homework_data", "valid_periods", "valid_names", "valid_teachers"}
VALID_COLUMNS = {"user_id", "class_name", "class_period", "class_teacher", "homework_name", "homework_status"}

# Structure for future use.
cur.execute("""CREATE TABLE IF NOT EXISTS user_data (
               user_id BIGINT PRIMARY KEY,
               class_period INT,
               class_teacher VARCHAR(100),
               class_name VARCHAR(100)
    );""")

cur.execute("""CREATE TABLE IF NOT EXISTS homework_data (
               user_id BIGINT PRIMARY KEY,
               class_period INT,
               class_teacher VARCHAR(100),
               homework_name VARCHAR(100),
               homework_status BOOLEAN DEFAULT FALSE
    );""")

cur.execute("""CREATE TABLE IF NOT EXISTS valid_periods (
               class_period INT PRIMARY KEY)""")

cur.execute("""CREATE TABLE IF NOT EXISTS valid_teachers (
               class_teacher VARCHAR(100) PRIMARY KEY)""")

cur.execute("""CREATE TABLE IF NOT EXISTS valid_names (
               class_name VARCHAR(100) PRIMARY KEY)""")

conn.commit()

def connect_db():
    return conn, cur

def close_db():
    cur.close()
    conn.close()

# FOR CHECKING IF TABLE IS ONE I MADE.
def check_table_validity(table):
    table_validity = bool()
    if table in VALID_TABLES:
        table_validity = True
        return table_validity
    else:
        table_validity = False
        return table_validity

# FOR CHECKING IF COLUMN IS ONE I MADE.
def check_column_validity(column):
    column_validity = bool()
    if column in VALID_COLUMNS:
        column_validity = True
        return column_validity
    else:
        table_validity = False
        return column_validity

def get_specific_data(table, column, unique_value, unique_column):
    if check_table_validity(table) and check_column_validity(column) and check_column_validity(unique_column):
        query = f"SELECT {column} FROM {table} WHERE %s = {unique_column};"
        cur.execute(query, (unique_value,))
        data = cur.fetchone()
        return data
    else:
        return None

def get_all_data_in_column(table, unique_value, unique_column):
    if check_table_validity(table) and check_column_validity(unique_column):
        query = f"SELECT * FROM {table} WHERE %s = {unique_column};"
        cur.execute(query, (unique_value,))
        data = cur.fetchall()
        return data
    else:
        return None

def get_all_data_in_table(table):
    if check_table_validity(table):
        query = f"SELECT * FROM {table};"
        cur.execute(query)
        data = cur.fetchall()
        return data
    else:
        return None

def insert_specific_data(table, column, value):
    if check_table_validity(table) and check_column_validity(column):
        query = f"INSERT INTO {table} ({column}) VALUES (%s);"
        cur.execute(query, (value,))
        conn.commit()
    pass

def update_specific_data(table, column, value, unique_value, unique_column):
    if check_table_validity(table) and check_column_validity(column) and check_column_validity(unique_column):
        query = f"UPDATE {table} SET {column} = {value} WHERE %s = {unique_column};"
        cur.execute(query, (unique_value,))
        conn.commit()
    pass

def reset_specific_data(table, column, unique_value, unique_column):
    if check_table_validity(table) and check_column_validity(column) and check_column_validity(unique_column):
        query = f"UPDATE {table} SET {column} = DEFAULT WHERE %s = {unique_column};"
        cur.execute(query, (unique_value,))
        conn.commit()
    pass

def reset_column(table, column, unique_value, unique_column):
    if check_table_validity(table) and check_column_validity(column) and check_column_validity(unique_column):
        query = f"UPDATE {table} SET {column} = DEFAULT WHERE %s = {unique_column};"
        cur.execute(query, (unique_value,))
        conn.commit()
    pass

def delete_specific_data(table, unique_value, unique_column):
    if check_table_validity(table) and check_column_validity(unique_column):
        query = f"DELETE FROM {table} WHERE {unique_value} = {unique_column};"
        cur.execute(query, (unique_value,))
        conn.commit()
    pass

def check_existence(table, column, value):
    if check_table_validity(table) and check_column_validity(column):
        query = f"SELECT * FROM {table} WHERE {column} = %s;"
        cur.execute(query, (value,))
        data = cur.fetchone()
        if data is None:
            return False
        else:
            return True
    else:
        return None
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

cur.execute("""CREATE TABLE IF NOT EXISTS valid_data (
               class_period INT,
               class_teacher VARCHAR(100),
               class_name VARCHAR(100)
    );""")
conn.commit()

def connect_db():
    return conn, cur

def close_db():
    cur.close()
    conn.close()

def get_specific_data(table, column, unique_value, unique_column):
    query = f"SELECT {column} FROM {table} WHERE {unique_value} = {unique_column};"
    cur.execute(query)
    data = cur.fetchone()
    return data

def get_all_data(table, unique_value, unique_column):
    query = f"SELECT * FROM {table} WHERE {unique_value} = {unique_column};"
    cur.execute(query)
    data = cur.fetchall()
    return data

def insert_specific_data(table, column, value):
    query = f"INSERT INTO {table} ({column}) VALUES ({value });"
    cur.execute(query)
    conn.commit()

def update_specific_data(table, column, value, unique_value, unique_column):
    query = f"UPDATE {table} SET {column} = {value} WHERE {unique_value} = {unique_column};"
    cur.execute(query)
    conn.commit()

def reset_specific_data(table, column, unique_value, unique_column):
    query = f"UPDATE {table} SET {column} = DEFAULT WHERE {unique_value} = {unique_column};"
    cur.execute(query)
    conn.commit()

def reset_column(table, column, unique_value, unique_column):
    query = f"UPDATE {table} SET {column} = DEFAULT WHERE {unique_value} = {unique_column};"
    cur.execute(query)
    conn.commit()

def delete_specific_data(table, unique_value, unique_column):
    query = f"DELETE FROM {table} WHERE {unique_value} = {unique_column};"
    cur.execute(query)
    conn.commit()
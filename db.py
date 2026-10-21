import psycopg2
import os
from dotenv import load_dotenv
load_dotenv()
DB_URL = os.getenv("DB_URL")
PASSWORD = os.getenv("PASSWORD")
USERNAME = os.getenv("USERNAME")
HOST = os.getenv("HOST")

conn = psycopg2.connect(host=HOST, user=USERNAME, password=PASSWORD, database=DB_URL)
cur = conn.cursor()


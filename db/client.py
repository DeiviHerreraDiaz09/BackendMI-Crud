import os
import asyncpg
from dotenv import load_dotenv


load_dotenv()

DATABASE_URL = os.getenv("DB_URL")


async def get_db_connection():
    try:
        conn = await asyncpg.connect(DATABASE_URL)
        return conn
    except Exception as e:
        print(e)
        return None

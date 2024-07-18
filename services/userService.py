from db.client import get_db_connection
from models.userModel import User
import logging

async def update_user(user: User):
    pass

async def listado():
    try:
        conn = await get_db_connection()
        async with conn.transaction():
            users = await conn.fetch("SELECT * FROM users")
            logging.info(users)
            return users
    except Exception as e:
        logging.error(e)
        raise


async def createTableUsers():
    try:
        conn = await get_db_connection()
        async with conn.transaction():
            await conn.execute(
                """
                CREATE TABLE IF NOT EXISTS users (
                    id SERIAL PRIMARY KEY,
                    name TEXT NOT NULL,
                    last_name TEXT NOT NULL,
                    sucursal TEXT NOT NULL,
                    marca TEXT NOT NULL
                );
                """
            )
            logging.info("Table created successfully")
            return True
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        return False
    finally:
        if conn:
            await conn.close()



async def dropTableUser():
    try:
        conn = await get_db_connection()
        async with conn.transaction():
            await conn.execute("""DROP TABLE IF EXISTS test_table""")
            logging.info("Table dropped successfully")
            return True
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        return False
    finally:
        if conn:
            await conn.close()


async def insertUser(user: User):
    try:
        conn = await get_db_connection()
        async with conn.transaction():
            result = await conn.fetchrow(
                """
                INSERT INTO users (name, last_name, sucursal, marca)
                VALUES ($1, $2, $3, $4)
                RETURNING id
                """,
                user.name, user.last_name, user.sucursal, user.marca
            )
            user_id = result['id']
            logging.info("User inserted successfully")
            return {**user.dict(), "id": user_id}
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        return None
    finally:
        if conn:
            await conn.close()

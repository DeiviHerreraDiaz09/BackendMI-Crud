from db.client import get_db_connection
from models.userModel import User
import logging


async def list_users_Service():
    try:
        conn = await get_db_connection()
        async with conn.transaction():
            users = await conn.fetch("SELECT * FROM users")
            logging.info(users)
            return users
    except Exception as e:
        logging.error(e)
        raise


async def list_user_Service(id: int):
    try:
        conn = await get_db_connection()
        async with conn.transaction():
            user = await conn.fetchrow("SELECT * FROM users WHERE id = $1", id)
            logging.info(f"User fetched: {user}")
            return user
    except Exception as e:
        logging.error(e)
        raise


async def insert_user_Service(user: User):
    try:
        conn = await get_db_connection()
        async with conn.transaction():
            result = await conn.fetchrow(
                """
                INSERT INTO users (fullname, sucursal, marca)
                VALUES ($1, $2, $3)
                RETURNING id
                """,
                user.fullname,
                user.sucursal,
                user.marca,
            )
            user_id = result["id"]
            logging.info("User inserted successfully")
            return {**user.dict(), "id": user_id}
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        return None
    finally:
        if conn:
            await conn.close()


async def create_tableUsers_Service():
    try:
        conn = await get_db_connection()
        async with conn.transaction():
            await conn.execute(
                """
                CREATE TABLE IF NOT EXISTS users (
                    id SERIAL PRIMARY KEY,
                    fullname TEXT NOT NULL,
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


async def update_user_Service(id: int, user: User):
    try:
        conn = await get_db_connection()
        async with conn.transaction():
            existing_user = await list_user_Service(id)

            if existing_user is None:
                logging.error(f"User with id {id} does not exist")
                return False

            await conn.execute(
                """
                UPDATE users
                SET fullname = $1, sucursal = $2, marca = $3
                WHERE id = $4
                """,
                user.fullname,
                user.sucursal,
                user.marca,
                id,
            )

            logging.info(f"User with id {id} updated successfully")
            return True
    except Exception as e:
        logging.error(f"An error occurred while updating user with id {id}: {e}")
        return False
    finally:
        if conn:
            await conn.close()


async def delete_user_Service(id: int):
    try:
        conn = await get_db_connection()
        async with conn.transaction():
            user = await list_user_Service(id)

            if user is None:
                logging.error(f"User with id {id} does not exist")
                return False

            await conn.execute("DELETE FROM users WHERE id = $1", id)
            logging.info(f"User with id {id} deleted successfully")
            return True
    except Exception as e:
        logging.error(f"An error occurred while deleting user with id {id}: {e}")
        return False
    finally:
        if conn:
            await conn.close()


async def drop_tableUsers_Service():
    try:
        conn = await get_db_connection()
        async with conn.transaction():
            await conn.execute("""DROP TABLE IF EXISTS users""")
            logging.info("Table dropped successfully")
            return True
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        return False
    finally:
        if conn:
            await conn.close()

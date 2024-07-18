from fastapi import APIRouter, HTTPException, status
from services.userService import createTableUsers, dropTableUser, insertUser, listado
from models.userModel import User
import logging

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/")
async def listadoUsuarios():
    try:
        users = listado()
        if not users:
            logging.info("Lista de usuarios vacía")
        return users
    except Exception as e:
        logging.error(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )



@router.post("/")
async def create_user(user: User):
    try:
        new_user = await insertUser(user)
        if not new_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User could not be created",
            )
        logging.info("New user created")
        return new_user
    except Exception as e:
        logging.error(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


# ajustes de tablas


@router.post("/create_table")
async def create_table():
    try:
        tableUser = await createTableUsers()
        if not tableUser:
            return {"message": "Table creation failed"}
        return {"message": "Table creation successful"}
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Table creation failed",
        )


@router.delete("/delete")
async def delete_table():
    try:
        tables = await dropTableUser()
        if tables is None:
            raise HTTPException(
                status_code=404, detail="Table not found or already deleted"
            )
        return {"message": "Table deletion successful"}
    except HTTPException as e:
        raise e
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Internal server error")

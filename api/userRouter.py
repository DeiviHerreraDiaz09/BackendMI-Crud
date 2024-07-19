from fastapi import APIRouter, HTTPException, status
from services.userService import (
    list_users_Service,
    list_user_Service,
    insert_user_Service,
    create_tableUsers_Service,
    drop_tableUsers_Service,
    update_user_Service,
    delete_user_Service,
)
from models.userModel import User
import logging

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/")
async def list_users():
    try:
        users = await list_users_Service()
        if not users:
            logging.error("No users found")
        return users
    except Exception as e:
        logging.error(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@router.get("/{id}")
async def list_user(id: int):
    try:
        user = await list_user_Service(id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )
        return user
    except HTTPException as e:
        raise e
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        )


@router.post("/create_table")
async def create_table():
    try:
        tableUser = await create_tableUsers_Service()
        if not tableUser:
            return {"message": "Table creation failed"}
        return {"message": "Table creation successful"}
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Table creation failed",
        )


@router.post("/")
async def create_user(user: User):
    try:
        new_user_successful = await insert_user_Service(user)
        if not new_user_successful:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User could not be created",
            )
        logging.info("New user created")
        return new_user_successful
    except Exception as e:
        logging.error(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@router.put("/{id}")
async def update_user(id: int, user: User):
    try:
        update_successful = await update_user_Service(id, user)
        if not update_successful:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User does not exist",
            )
        return {"message": "User updated successfully"}
    except HTTPException as e:
        raise e
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        )


@router.delete("/table")
async def delete_table():
    try:
        tables = await drop_tableUsers_Service()
        if tables is None:
            raise HTTPException(
                status_code=404, detail="Table not found or already deleted"
            )
        return {"message": "Table deletion successful"}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Internal server error")


@router.delete("/{id}")
async def delete_user(id: int):
    try:
        deleted_successful = await delete_user_Service(id)
        if not deleted_successful:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User does not exist",
            )
        return {"message": "User deleted successfully"}
    except HTTPException as e:
        raise e
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        )

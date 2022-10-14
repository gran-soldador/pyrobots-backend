from fastapi import APIRouter, HTTPException, status
from pony.orm import *
from db import *
from functions_jwt import validate_token, write_token

db = Database()


auth_routes = APIRouter()

# Login de usuario que genera token de autenticación


@auth_routes.post("/login")
async def login(username: str, password: str):
    with db_session:
        if not user_exist(username):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="User doesn't exist.")
        elif not correct_login(username, password):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail="Wrong Password.")
        elif correct_login(username, password):
            return write_token(devolver_user(username))

# Verificacion de que el token sea válido


@auth_routes.post("/login/verify_token")
async def verify_token(Authorization: str):
    return validate_token(Authorization, output=True)

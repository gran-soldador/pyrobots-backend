from fastapi import APIRouter, HTTPException, status, Form
from pony.orm import *
from db import *
from .functions_jwt import write_token
from .validation import *


auth_routes = APIRouter()

# Login de usuario que genera token de autenticación


@auth_routes.post("/login")
async def login(username: str = Form(...),
                password: str = Form(...)):
    with db_session:
        if not user_exist(username):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="User doesn't exist.")
        elif not correct_login(username, password):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail="Wrong Password.")
        else:
            user_id = Usuario.get(nombre_usuario=username).user_id
            return write_token({"user_id": user_id})

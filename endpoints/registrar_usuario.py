from fastapi import APIRouter, HTTPException, status
from db import *

router = APIRouter()

MAX_NICKNAME_SIZE = 25
MIN_NICKNAME_SIZE = 8
MIN_PASSWORD_SIZE = 3


@router.post("/user/registro_de_usuario/",
             status_code=status.HTTP_200_OK,
             tags=["User Methods"],
             name="Registro de Usuarios")
async def registro_usuario(name: str, password: str, email: str):
    with db_session:
        if len(name) > MAX_NICKNAME_SIZE:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="Username too long.")
        elif len(name) < MIN_NICKNAME_SIZE:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="Username too short.")
        elif len(password) < MIN_PASSWORD_SIZE:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="Password too Short.")
        elif user_exist(name):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="User name already exist.")
        elif email_exist(email):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="Email already registered.")
        elif (not password_is_correct(password)):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="Password inválido, el password "
                                       "requiere al menos una mayuscula, una "
                                       "minusucula y un numero.")
        elif not ("@" in email):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="Email inválido.")
        else:
            crear_usuario(name, password, email)
            return {"new user created": name}

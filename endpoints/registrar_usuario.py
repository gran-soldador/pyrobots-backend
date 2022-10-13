from email.mime import image
from fileinput import filename
from logging import exception
from fastapi import APIRouter, HTTPException, status, File, UploadFile
from db import *
from PIL import Image
import imghdr

router = APIRouter()

MAX_NICKNAME_SIZE = 32
MIN_NICKNAME_SIZE = 1
MIN_PASSWORD_SIZE = 8


#  Creacion de usuario con o sin avatar
@router.post("/user/registro_de_usuario/",
             tags=["User Methods"],
             name="Registro de Usuarios")
async def registro_usuario(username: str,
                           password: str,
                           useremail: str,
                           userAvatar: UploadFile = File(None)
                           ):
    with db_session:
        if len(username) > MAX_NICKNAME_SIZE:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="Username too long.")
        elif len(username) < MIN_NICKNAME_SIZE:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="Username too short.")
        elif len(password) < MIN_PASSWORD_SIZE:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="Password too Short.")
        elif user_exist(username):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="User name already exist.")
        elif email_exist(useremail):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="Email already registered.")
        elif (not password_is_correct(password)):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="Password inválido, el password "
                                       "requiere al menos una mayuscula, una "
                                       "minusucula y un numero.")
        elif not ("@" in useremail):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="Email inválido.")
        
        if (userAvatar is None):
            crear_usuario(username, password, useremail)
            return {"new user created": username}
        else:
            if not userAvatar.filename.lower().endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp')):
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                    detail="File is not an image.")

            crear_usuario_con_avatar(username, password, useremail)
            avatar = "UserAvatar"
            file_location = f"userUploads/avatars/{username+avatar}"
            change_avatar_user(username)
            with open(file_location, "wb+") as file_object:
                file_object.write(userAvatar.file.read())
            return {"new user with avatar created": username}


#  Actualizacion de avatar del usuario
@router.post("/user/uploadavatar/", tags=["User Methods"], name="Actualizacion de Avatar del Usuario")
async def upload_user_avatar(username: str, file: UploadFile = File(...)):
    with db_session:
        if not user_exist(username):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="User doesn't exist.")

        elif not file.filename.lower().endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp')):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                 detail="File is not an image.")
        else:
            avatar = "UserAvatar"
            file_location = f"userUploads/avatars/{username+avatar}"
            change_avatar_user(username)
            with open(file_location, "wb+") as file_object:
                file_object.write(file.file.read())
            return {"info": f"file '{file.filename}' saved at '{file_location}'"}
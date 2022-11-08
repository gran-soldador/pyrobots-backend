from fastapi import APIRouter, HTTPException, status, File, UploadFile, Form
from db import *
from .validation import *

router = APIRouter()

MAX_NICKNAME_SIZE = 32
MIN_NICKNAME_SIZE = 1
MIN_PASSWORD_SIZE = 8


#  Creacion de usuario con o sin avatar
@router.post("/user/register",
             tags=["User Methods"],
             name="Register new user")
async def registro_usuario(username: str = Form(...),
                           password: str = Form(...),
                           email: str = Form(...),
                           avatar: UploadFile = File(None)
                           ):
    with db_session:
        if len(username) > MAX_NICKNAME_SIZE:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="Username too long.")
        elif len(password) < MIN_PASSWORD_SIZE:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="Password too Short.")
        elif user_exist(username):
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

        avatar_location = "avatars/DefaultAvatar.png"
        if avatar is not None:
            ext = avatar.filename.split(".")[-1]
            if ext not in ['png', 'jpg', 'jpeg', 'tiff', 'bmp']:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                    detail="File is not an image.")
            avatar_location = f"avatars/{username}UserAvatar.{ext}"
            with open("userUploads/" + avatar_location, "wb+") as file_object:
                file_object.write(avatar.file.read())
        Usuario(
            nombre_usuario=username,
            contraseña=password,
            email=email,
            verificado=False,
            avatar=avatar_location
        )
        send_email(email)
        return {"new user created": username}

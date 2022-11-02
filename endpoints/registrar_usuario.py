from fastapi import APIRouter, HTTPException, status, File, UploadFile, Form
from db import *
from .validation import *

router = APIRouter()

MAX_NICKNAME_SIZE = 32
MIN_NICKNAME_SIZE = 1
MIN_PASSWORD_SIZE = 8


#  Creacion de usuario con o sin avatar
@router.post("/user/registro_de_usuario/",
             tags=["User Methods"],
             name="Registro de Usuarios")
async def registro_usuario(username: str = Form(...),
                           password: str = Form(...),
                           useremail: str = Form(...),
                           userAvatar: UploadFile = File(None)
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

        avatar_location = "avatars/DefaultAvatar.png"
        if userAvatar is not None:
            ext = userAvatar.filename.split(".")[-1]
            if ext not in ['png', 'jpg', 'jpeg', 'tiff', 'bmp']:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                    detail="File is not an image.")
            avatar_location = f"avatars/{username}UserAvatar.{ext}"
            with open("userUploads/" + avatar_location, "wb+") as file_object:
                file_object.write(userAvatar.file.read())
        Usuario(
            nombre_usuario=username,
            contraseña=password,
            email=useremail,
            verificado=False,
            avatar=avatar_location
        )
        send_email(useremail)
        return {"new user created": username}

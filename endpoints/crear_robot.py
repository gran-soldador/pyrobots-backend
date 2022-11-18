from fastapi import (APIRouter, HTTPException, status, File, UploadFile, Form,
                     Depends)
from db import *
from .validation import *
from .functions_jwt import *
router = APIRouter()


@router.post("/robot/new",
             tags=['Robot Methods'],
             name="Upload user robot")
async def creacion_de_robot(user_id: int = Depends(authenticated_user),
                            name: str = Form(...),
                            avatar: UploadFile = File(None),
                            code: UploadFile = File(...)
                            ):
    # Me da el codigo del robot en bytes -> b'<codigo de robot>
    code_of_robot = code.file.read()
    encoding = 'utf-8'
    # Acá me transforma el codigo a str
    code_of_robot = str(code_of_robot, encoding)
    with db_session:
        user = Usuario[user_id]
        if not code.filename.lower().endswith('.py'):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="File must be a .py")
        if Robot.get(nombre=name, usuario=user) is not None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="You already have"
                                "a robot with that name.")
        rpic_location = "robotAvatars/defaultAvatarRobot.png"
        if avatar is not None:
            ext = avatar.filename.split(".")[-1]
            if ext not in ['png', 'jpg', 'jpeg', 'tiff', 'bmp']:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                    detail="File is not an image.")

            rpic_location = f"robotAvatars/{user_id}{name}Avatar.{ext}"
            with open("userUploads/" + rpic_location, "wb+") as file_object:
                file_object.write(avatar.file.read())
        Robot(
            nombre=name,
            implementacion=code_of_robot,
            avatar=rpic_location,
            partidas_ganadas=0,
            partidas_jugadas=0,
            juegos_ganados=0,
            rondas_ganadas=0,
            defectuoso=False,
            usuario=user
        )
        return {"new robot created": name}

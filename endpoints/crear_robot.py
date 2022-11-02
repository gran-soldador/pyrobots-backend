from fastapi import (APIRouter, HTTPException, status, File, UploadFile, Form,
                     Depends)
from db import *
from .validation import *
from .functions_jwt import *
router = APIRouter()


@router.post("/user/creacion_de_robot/",
             name="Subida de Robots por el Usuario")
async def creacion_de_robot(user_id: int = Depends(authenticated_user),
                            robotName: str = Form(...),
                            robotAvatar: UploadFile = File(None),
                            robotCode: UploadFile = File(...)
                            ):
    # Me da el codigo del robot en bytes -> b'<codigo de robot>
    code_of_robot = robotCode.file.read()
    encoding = 'utf-8'
    # Acá me transforma el codigo a str
    code_of_robot = str(code_of_robot, encoding)
    with db_session:
        try:
            user = Usuario[user_id]
        except ObjectNotFound:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="User doesn't exist.")
        if not robotCode.filename.lower().endswith('.py'):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="File must be a .py")
        if Robot.get(nombre=robotName, usuario=user) is not None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="You already have"
                                "a robot with that name.")
        rpic_location = "userUploads/robotAvatars/defaultAvatarRobot.png"
        if robotAvatar is not None:
            ext = robotAvatar.filename.split(".")[-1]
            if ext not in ['png', 'jpg', 'jpeg', 'tiff', 'bmp']:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                    detail="File is not an image.")

            rpic_location = "userUploads/"
            rpic_location += f"robotAvatars/{user_id}{robotName}Avatar.{ext}"
            with open(rpic_location, "wb+") as file_object:
                file_object.write(robotAvatar.file.read())
        Robot(
            nombre=robotName,
            implementacion=code_of_robot,
            avatar=rpic_location,
            partidas_ganadas=0,
            partidas_jugadas=0,
            defectuoso=False,
            usuario=user
        )
        return {"new robot created": robotName}

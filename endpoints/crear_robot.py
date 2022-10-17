from fastapi import APIRouter, HTTPException, status, File, UploadFile, Form
from db import *
from validation import *

router = APIRouter()


@router.post("/user/creacion_de_robot/",
             name="Subida de Robots por el Usuario")
async def creacion_de_robot(username: str = Form(),
                            robotName: str = Form(),
                            robotAvatar: UploadFile = File(None),
                            robotCode: UploadFile = File(...)
                            ):
    # Me da el codigo del robot en bytes -> b'<codigo de robot>
    code_of_robot = robotCode.file.read()
    encoding = 'utf-8'
    # Acá me transforma el codigo a str
    code_of_robot = str(code_of_robot, encoding)
    with db_session:
        if not user_exist(username):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="User doesn't exist.")
        elif not robotCode.filename.lower().endswith(('.py')):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="File must be a .py")
        elif user_robot_already_exist(username, robotName):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="You already have"
                                "a robot with that name.")
        robot_pic_location = "userUploads/robotAvatars/defaultAvatarRobot.png"
        if robotAvatar is not None:
            ext = robotAvatar.filename.split(".")[-1]
            if ext not in ['png', 'jpg', 'jpeg', 'tiff', 'bmp']:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                    detail="File is not an image.")
            robot_pic_location = f"userUploads/robotAvatars/{username}{robotName}Avatar.{ext}"
            with open(robot_pic_location, "wb+") as file_object:
                file_object.write(robotAvatar.file.read())
        myUser_id = Usuario.get(nombre_usuario=username).user_id
        Robot(
            nombre=robotName,
            implementacion=code_of_robot,
            avatar=robot_pic_location,
            partidas_ganadas=0,
            partidas_jugadas=0,
            defectuoso=False,
            usuario=myUser_id
        )
        return {"new robot created": robotName}

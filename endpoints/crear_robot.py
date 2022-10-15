from fastapi import APIRouter, HTTPException, status, File, UploadFile, Form
from db import *

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
                                detail="You already have a robot with that name.")
        else:
            if (robotAvatar is None):
                subir_robot(username, robotName, code_of_robot)
                return {"new robot created": robotName}
            else:
                if not robotAvatar.filename.lower().endswith(('.png',
                                                              '.jpg',
                                                              '.jpeg',
                                                              '.tiff',
                                                              '.bmp')):
                    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                        detail="File is not an image.")
                subir_robot_con_avatar(username, robotName, code_of_robot)
                avatar_string = "Avatar"
                avatar_location = f"userUploads/robotAvatars/{username+robotName+avatar_string}"
                with open(avatar_location, "wb+") as file_object:
                    file_object.write(robotAvatar.file.read())
                return {"new robot with avatar created": robotName}

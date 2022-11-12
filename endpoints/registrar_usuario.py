from fastapi import APIRouter, HTTPException, status, File, UploadFile, Form
from db import *
from .validation import *

router = APIRouter()

MAX_NICKNAME_SIZE = 32
MIN_NICKNAME_SIZE = 1
MIN_PASSWORD_SIZE = 8

defaultrobots = [
    ("SpiralRobot", """
    class SpiralRobot(Robot):
        def initialize(self):
            pass
        def respond(self):
            x, y = self.get_position()
            vel, dir = self.get_velocity(), self.get_direction()
            if vel == 0:
                self.drive(random.uniform(0,360),50)
            else:
                self.drive((dir + 5) % 360, 50)
            if self.is_cannon_ready(): self.cannon(dir, 80)"""),
    ("GuardRobot", """
    class GuardRobot(Robot):
        def initialize(self):
            self.dir = 90

        def respond(self):
            x, y = self.get_position()
            vel, dir = self.get_velocity(), self.get_direction()

            if x < 100:
                self.drive(0, 50)
            elif x > 150:
                self.drive(180, 50)
            else:
                if y > 900:
                    self.dir = 270
                elif y < 100:
                    self.dir = 90
                self.drive(self.dir, 50)

            self.point_scanner(0, 10)
            result = self.scanned()

            if result is not None and self.is_cannon_ready():
                self.cannon(0, result)""")
]


#  Creacion de usuario con o sin avatar
@router.post("/user/register",
             tags=["User Methods"],
             name="Register new user")
async def registro_usuario(username: str = Form(...),
                           password: str = Form(...),
                           email: str = Form(...),
                           avatar: UploadFile = File(None)
                           ):
    if len(username) > MAX_NICKNAME_SIZE:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Username too long.")
    elif len(password) < MIN_PASSWORD_SIZE:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Password too Short.")
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
    with db_session:
        if user_exist(username):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="User name already exist.")
        elif email_exist(email):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="Email already registered.")
        user = Usuario(
            nombre_usuario=username,
            contraseña=password,
            email=email,
            verificado=False,
            avatar=avatar_location
        )
        for robot in defaultrobots:
            Robot(
                nombre=robot[0],
                implementacion=robot[1],
                avatar="robotAvatars/defaultAvatarRobot.png",
                partidas_ganadas=0,
                partidas_jugadas=0,
                juegos_ganados=0,
                rondas_ganadas=0,
                defectuoso=False,
                usuario=user
            )
    send_email(email)
    return {"new user created": username}

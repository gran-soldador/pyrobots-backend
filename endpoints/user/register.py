from fastapi import (APIRouter, HTTPException, status, File, UploadFile, Form,
                     Depends, BackgroundTasks)
from db import *
from utils.password_validator import password_validator_generator
from utils.mailing import send_verification_email

router = APIRouter()

MAX_USERNAME_LEN = 32
DEFAULT_ROBOTS = (
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
        if self.is_cannon_ready(): self.cannon(dir, 80)
"""),
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
            self.cannon(0, result)
""")
)

password_validator = password_validator_generator("password")


@router.post("/user/register",
             tags=["User Methods"],
             name="Register new user")
async def register(username: str = Form(...),
                   password: str = Depends(password_validator),
                   email: str = Form(...),
                   avatar: UploadFile = File(None),
                   background_tasks: BackgroundTasks = BackgroundTasks()
                   ):
    if len(username) > MAX_USERNAME_LEN:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Username too long.")
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
        if User.get(name=username) is not None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="User name already exist.")
        elif User.get(email=email) is not None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="Email already registered.")
        user = User(
            name=username,
            password=password,
            email=email,
            verified=False,
            avatar=avatar_location
        )
        for robot in DEFAULT_ROBOTS:
            Robot(
                name=robot[0],
                code=robot[1],
                avatar="robotAvatars/defaultAvatarRobot.png",
                matches_num_won=0,
                matches_num_played=0,
                games_won=0,
                rounds_won=0,
                defective=False,
                user=user
            )
    background_tasks.add_task(send_verification_email, email)
    return {"new user created": username}

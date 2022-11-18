from fastapi import (APIRouter, HTTPException, Form, File, status,
                     UploadFile, Depends)
from db import *
from .functions_jwt import *

router = APIRouter()


@router.post("/user/profile/change_avatar",
             tags=['User Methods'],
             name='Change Profile Picture')
async def edit_profile_picture(user_id: int=Depends(authenticated_user),
                               new_profile: UploadFile=File(...)
                               ):
    ext = new_profile.filename.split(".")[-1]
    if ext not in ['png', 'jpg', 'jpeg', 'tiff', 'bmp']:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="File is not an image.")
    with db_session:
        username = Usuario.get(user_id=user_id).nombre_usuario
        avatar_location = f"avatars/{username}UserAvatar.{ext}"
        with open("userUploads/" + avatar_location, "wb+") as file_object:
            file_object.write(new_profile.file.read())
        Usuario[user_id].avatar = avatar_location
        return {"detail": "Profile picture succesfully changed."}

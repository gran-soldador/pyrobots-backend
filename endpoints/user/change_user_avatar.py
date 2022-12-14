from fastapi import (APIRouter, HTTPException, File, status,
                     UploadFile, Depends)
from db import *
from utils.tokens import *

router = APIRouter()


@router.post("/user/profile/change_avatar",
             tags=['User Methods'],
             name='Change Profile Picture')
async def change_user_avatar(user_id: int = Depends(authenticated_user),
                             new_profile: UploadFile = File(...)
                             ):
    ext = new_profile.filename.split(".")[-1]
    if ext not in ['png', 'jpg', 'jpeg', 'tiff', 'bmp']:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="File is not an image.")
    with db_session:
        user = User.get(id=user_id)
        avatar_location = f"avatars/{user.name}UserAvatar.{ext}"
        with open("userUploads/" + avatar_location, "wb+") as file_object:
            file_object.write(new_profile.file.read())
        user.avatar = avatar_location
        return {"detail": "Profile picture succesfully changed."}

from fastapi import (APIRouter, HTTPException, Form, File, status,
                     UploadFile, Depends)
from db import *
from utils.tokens import *

router = APIRouter()


@router.post("/robot/edit_implementation",
             tags=['Robot Methods'],
             name='Edit robot implementation')
async def change_robot_code(user_id: int = Depends(authenticated_user),
                            robot_id: int = Form(...),
                            new_code: UploadFile = File(...)
                            ):
    if not new_code.filename.lower().endswith('.py'):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="File must be a .py")
    with db_session:
        robot = Robot.get(id=robot_id, user=user_id)
        if robot is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="Invalid robot.")
        new_code_of_robot = new_code.file.read()
        encoding = 'utf-8'
        new_code_of_robot = str(new_code_of_robot, encoding)
        robot.code = new_code_of_robot
        return {"detail": "Robot code succesfully changed."}

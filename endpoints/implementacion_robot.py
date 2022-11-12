from fastapi import APIRouter, HTTPException, status, Depends
from db import *
from .functions_jwt import *

router = APIRouter()


@router.get('/robot/code/{robot_id}',
            tags=['Robot Methods'],
            name='Return robot code')
async def implementacion_robot(robot_id: int,
                               user_id: int = Depends(authenticated_user)):
    with db_session:
        robot = Robot.get(robot_id=robot_id)
        if robot is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail='El robot no existe')
        if robot.usuario.user_id != user_id:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail='El robot no pertenece al usuario')
        code = robot.implementacion
    print(code)
    return code

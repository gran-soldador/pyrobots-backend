from fastapi import APIRouter
from db import *
from .functions_jwt import *
from dataclasses import dataclass

router = APIRouter()


@dataclass(slots=True)
class ProfileResult:
    username: str
    mail: str
    avatar: str


@router.get('/user/profile',
            tags=['User Methods'],
            name='View User Profile',
            response_model=ProfileResult)
async def view_profile(user_id: int = Depends(authenticated_user)):
    with db_session:
        user = Usuario.get(user_id=user_id)
        return ProfileResult(
            username=user.nombre_usuario,
            mail=user.email,
            avatar="http://localhost:9000/" + user.avatar
        )

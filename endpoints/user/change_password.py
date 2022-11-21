from fastapi import APIRouter, HTTPException, status, Form, Depends
from db import *
from utils.password_validator import password_validator_generator
from utils.tokens import *

router = APIRouter()

MIN_PASSWORD_SIZE = 8

password_validator = password_validator_generator("new_password")


@router.post('/user/edit/password',
             tags=['User Methods'],
             name='Change user password')
async def change_password(user_id: int = Depends(authenticated_user),
                          old_password: str = Form(...),
                          new_password: str = Depends(password_validator)):
    if old_password == new_password:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="La contraseña debe ser distinta")
    with db_session:
        user = User[user_id]
        if user.password != old_password:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="contraseña incorrecta")
        user.password = new_password
        user.flush()

from fastapi import APIRouter, HTTPException, status, Form
from db import *
from .validation import *
from .functions_jwt import *

router = APIRouter()

MIN_PASSWORD_SIZE = 8


@router.post('/user/edit/password',
             tags=['User Methods'],
             name='Change user password')
async def change_password(user_id: int = Depends(authenticated_user),
                          old_password: str = Form(...),
                          new_password: str = Form(...)):
    if old_password == new_password:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="La contraseña debe ser distinta")
    if len(new_password) < MIN_PASSWORD_SIZE:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Password too Short.")
    elif (not password_is_correct(new_password)):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Password inválido, el password "
                                   "requiere al menos una mayuscula, una "
                                   "minusucula y un numero.")
    with db_session:
        user = Usuario.get(user_id=user_id)
        if user.contraseña != old_password:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="contraseña incorrecta")           
        user.contraseña = new_password
        user.flush()

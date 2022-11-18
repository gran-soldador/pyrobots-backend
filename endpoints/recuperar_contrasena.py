from fastapi import APIRouter, HTTPException, status, Form
from db import *
from .functions_jwt import *
from endpoints.validation import password_is_correct

router = APIRouter()


@router.post("/password_recover/{token}",
             tags=['User Methods'],
             name='Recover the password and set a new one.')
async def recover_password(token,
                           password: str = Form(...)
                           ):
    with db_session:
        token = check_verification_token(token)
        if token is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="Invalid Token.")
        myToken_user = token['email']
        user = Usuario.get(email=myToken_user)
        if user is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="User doesn't exist.")
        if not password_is_correct(password):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="Password inválido, el password "
                                       "requiere al menos una mayuscula, una "
                                       "minusucula y un numero.")
        user.contraseña = password
    return {'detail': "Password succesfully changed."}

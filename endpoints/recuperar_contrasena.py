from fastapi import APIRouter, HTTPException, status, Form
from db import *
from utils.tokens import *
from utils.validation import password_is_correct

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
        email = token['email']
        user = User.get(email=email)
        if user is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="User doesn't exist.")
        if not password_is_correct(password):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="Password inválido, el password "
                                       "requiere al menos una mayuscula, una "
                                       "minusucula y un numero.")
        user.password = password
    return {'detail': "Password succesfully changed."}

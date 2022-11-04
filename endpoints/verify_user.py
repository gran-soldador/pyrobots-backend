from fastapi import APIRouter, HTTPException, status
from db import *
from .functions_jwt import *

router = APIRouter()


@router.get('/verify/{token}',
            tags=['User Methods'],
            name='verificación de email')
async def verify_user(token):
    with db_session:
        token = check_verification_token(token)
        if token is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="Invalid token.")
        mytoken_email = token['email']
        user = Usuario.get(email=mytoken_email)
        if user is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="User doesn't exist.")
        elif user.verificado:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="User already verified.")
        user.verificado = True
        return {'detail': "user succesfully verified!"}

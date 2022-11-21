from fastapi import APIRouter, HTTPException, status, Depends
from db import *
from utils.tokens import *
from utils.password_validator import password_validator_generator

router = APIRouter()

password_validator = password_validator_generator("password")


@router.post("/password_recover/{token}",
             tags=['User Methods'],
             name='Recover the password and set a new one.')
async def recover_password(token,
                           password: str = Depends(password_validator)
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
        user.password = password
    return {'detail': "Password succesfully changed."}

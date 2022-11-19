from fastapi import APIRouter, HTTPException, status, Form
from pony.orm import *
from db import *
from utils.tokens import gen_session_token
from utils.validation import *


router = APIRouter()


@router.post("/login",
             tags=['User Methods'],
             name='Login')
async def login(username: str = Form(...),
                password: str = Form(...)):
    with db_session:
        user = User.get(name=username)
        if user is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="User doesn't exist.")
        elif user.password != password:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail="Wrong Password.")
        elif not user.verified:
            detail = "User isn't verified yet. Please verify your account."
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail=detail)
        return {'accessToken': gen_session_token({"user_id": user.id})}

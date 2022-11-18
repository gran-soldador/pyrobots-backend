from fastapi import APIRouter, HTTPException, status, Form
from db import *
from utils.tokens import *
from utils.validation import send_email_recover

router = APIRouter()


@router.post("/send_email_password_recover",
             tags=['User Methods'],
             name='Send an email for password recover.')
async def send_email_password(email: str = Form(...)):
    with db_session:
        if User.get(email=email) is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="Email doesn't exist in database")
        send_email_recover(email)
    return {'detail': "Checkout your email for password recover."}

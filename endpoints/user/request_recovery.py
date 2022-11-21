from fastapi import (APIRouter, HTTPException, status, Form,
                     BackgroundTasks)
from db import *
from utils.mailing import send_recovery_email

router = APIRouter()


@router.post("/send_email_password_recover",
             tags=['User Methods'],
             name='Send an email for password recover.')
async def request_recovery(
    email: str = Form(...),
    background_tasks: BackgroundTasks = BackgroundTasks()
):
    with db_session:
        if User.get(email=email) is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="Email doesn't exist in database")
        background_tasks.add_task(send_recovery_email, email)
    return {'detail': "Checkout your email for password recover."}

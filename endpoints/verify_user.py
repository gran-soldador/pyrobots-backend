from fastapi import APIRouter, HTTPException, status
from db import *
from .functions_jwt import *

router = APIRouter()

@router.get('/verify/{token}')
async def verify_user(token):
    with db_session:
        my_token = validate_token(token)
        mytoken_email = my_token['email']
        if Usuario.get(email=mytoken_email) is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                    detail="User doesn't exist.")
        
        myUser = Usuario.get(email=mytoken_email)
        myUser.verificado = True
        return {'detail': "user succesfully verified!"}

from jwt import encode, decode, exceptions
from datetime import datetime, timedelta
from os import getenv
from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

# Genera fecha de expiracion de token


def expire_date(days: int):
    date = datetime.now()
    new_date = date + timedelta(days)
    return new_date

# Genera token de acuerdo al usuario que quiera ingresar


def write_token(data: dict):
    token = encode(payload={**data, "exp": expire_date(2)},
                   key=getenv("SECRET"), algorithm="HS256")
    return {'accessToken': token}


async def authenticated_user(
        token: HTTPAuthorizationCredentials = Depends(HTTPBearer())):
    try:
        res = decode(token.credentials, key=getenv("SECRET"),
                     algorithms=["HS256"])
        return res["user_id"]
    except exceptions.DecodeError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Invalid Token")
    except exceptions.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Token Expired")

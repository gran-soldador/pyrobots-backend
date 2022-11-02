from jwt import encode, decode, exceptions
from datetime import datetime, timedelta
from os import getenv
from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials


def expire_date(days: int):
    date = datetime.now()
    new_date = date + timedelta(days)
    return new_date


def gen_session_token(data: dict):
    token = encode(payload={**data, "exp": expire_date(2), "kind": 1},
                   key=getenv("SECRET"), algorithm="HS256")
    return {'accessToken': token}


def gen_verification_token(data: dict):
    token = encode(payload={**data, "kind": 2},
                   key=getenv("SECRET"), algorithm="HS256")
    return token


async def authenticated_user(
        token: HTTPAuthorizationCredentials = Depends(HTTPBearer())):
    try:
        res = decode(token.credentials, key=getenv("SECRET"),
                     algorithms=["HS256"])
        if res["kind"] != 1:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail="Invalid Token")
        return res["user_id"]
    except exceptions.DecodeError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Invalid Token")
    except exceptions.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Token Expired")


def check_verification_token(token):
    try:
        data = decode(token, key=getenv("SECRET"), algorithms=["HS256"])
        if data["kind"] != 2:
            return None
    except exceptions.PyJWTError:
        return None

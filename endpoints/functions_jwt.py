from jwt import encode, decode, exceptions
from datetime import datetime, timedelta
from os import getenv
from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from enum import IntEnum
from typing import Optional, Dict, Any


class JWTKinds(IntEnum):
    SESSION = 1
    VERIFICATION = 2


def expire_date(days: int) -> datetime:
    date = datetime.now()
    new_date = date + timedelta(days)
    return new_date


def gen_session_token(data: Dict[str, Any]) -> str:
    payload = {**data, "exp": expire_date(2), "kind": JWTKinds.SESSION.value}
    token = encode(payload=payload, key=getenv("SECRET"), algorithm="HS256")
    return token


def gen_verification_token(data: Dict[str, Any]) -> str:
    payload = {**data, "kind": JWTKinds.VERIFICATION.value}
    token = encode(payload=payload, key=getenv("SECRET"), algorithm="HS256")
    return token


def check_verification_token(token: str) -> Optional[Dict[str, Any]]:
    try:
        data = decode(token, key=getenv("SECRET"), algorithms=["HS256"])
        if data["kind"] == JWTKinds.VERIFICATION:
            return data
    except exceptions.PyJWTError:
        return


def check_session_token(token: str) -> Optional[Dict[str, Any]]:
    try:
        data = decode(token, key=getenv("SECRET"), algorithms=["HS256"])
        if data["kind"] == JWTKinds.SESSION:
            return data
    except exceptions.PyJWTError:
        return


async def authenticated_user(
        token: HTTPAuthorizationCredentials = Depends(HTTPBearer())) -> int:
    user_id = check_session_token(token.credentials)
    if user_id is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Invalid Token")
    return user_id

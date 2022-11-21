from enum import IntEnum
from os import getenv
from typing import Any, Dict, Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jwt import decode, encode, exceptions


class JWTKinds(IntEnum):
    SESSION = 1
    VERIFICATION = 2


def _gen_token(kind: JWTKinds, data: Dict[str, Any]) -> str:
    payload = {**data, "kind": kind.value}
    token = encode(payload=payload, key=getenv("SECRET"), algorithm="HS256")
    return token


def gen_session_token(data: Dict[str, Any]) -> str:
    return _gen_token(JWTKinds.SESSION, data)


def gen_verification_token(data: Dict[str, Any]) -> str:
    return _gen_token(JWTKinds.VERIFICATION, data)


def _check_token(kind: JWTKinds, token: str) -> Optional[Dict[str, Any]]:
    try:
        data = decode(token, key=getenv("SECRET"), algorithms=["HS256"])
        if data["kind"] == kind:
            del data["kind"]
            return data
    except exceptions.PyJWTError:
        pass
    return None


def check_verification_token(token: str) -> Optional[Dict[str, Any]]:
    return _check_token(JWTKinds.VERIFICATION, token)


def check_session_token(token: str) -> Optional[Dict[str, Any]]:
    return _check_token(JWTKinds.SESSION, token)


def authenticated_user(
        token: HTTPAuthorizationCredentials = Depends(HTTPBearer())) -> int:
    data = check_session_token(token.credentials)
    if data is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Invalid Token")
    return data["user_id"]

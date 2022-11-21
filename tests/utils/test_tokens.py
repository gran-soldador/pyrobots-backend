import pytest
from fastapi.security import HTTPAuthorizationCredentials

from utils.tokens import *


def test_verification_token():
    data = {"testData": 42}
    token = gen_verification_token(data)
    decoded = check_verification_token(token)
    assert decoded == data


def test_session_token():
    data = {"testData": 42}
    token = gen_session_token(data)
    decoded = check_session_token(token)
    assert decoded == data


def test_mixed_tokens():
    data = {"testData": 42}
    token = gen_session_token(data)
    decoded = check_verification_token(token)  # Wrong checker!
    assert decoded is None
    token = gen_verification_token(data)
    decoded = check_session_token(token)  # Again
    assert decoded is None


def test_decode_trash():
    token = "NotAToken!"
    assert check_verification_token(token) is None
    assert check_session_token(token) is None


def test_authenticated_user_invalid():
    data = {"user_id": 42}
    token = gen_session_token(data) + "trash"
    with pytest.raises(HTTPException):
        authenticated_user(
            HTTPAuthorizationCredentials(scheme="Bearer", credentials=token))


def test_authenticated_user():
    data = {"user_id": 42}
    token = gen_session_token(data)
    result = authenticated_user(
        HTTPAuthorizationCredentials(scheme="Bearer", credentials=token))
    assert result == 42

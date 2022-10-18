from jwt import encode, decode, exceptions
from datetime import datetime, timedelta
from os import getenv
from fastapi.responses import JSONResponse

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

# Valida que el token ingresado sea válido


def validate_token(token):
    try:
        return decode(token, key=getenv("SECRET"), algorithms=["HS256"])
    except exceptions.DecodeError:
        return JSONResponse(content={'Message:': 'Invalid Token'},
                            status_code=401)
    except exceptions.ExpiredSignatureError:
        return JSONResponse(content={'Message:': 'Token Expired'},
                            status_code=401)

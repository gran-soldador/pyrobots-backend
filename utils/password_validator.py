from fastapi import Form, HTTPException, status

MIN_PASSWORD_SIZE = 8


def password_validator_generator(form_field_name: str):
    def validate_password(password: str = Form(..., alias=form_field_name)):
        if len(password) < MIN_PASSWORD_SIZE:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="Password too Short.")
        upper = any(c.isupper() for c in password)
        lower = any(c.islower() for c in password)
        digit = any(c.isdigit() for c in password)
        if not (upper and lower and digit):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="Password inválido, el password "
                                       "requiere al menos una mayuscula, una "
                                       "minusucula y un numero.")
        return password
    return validate_password

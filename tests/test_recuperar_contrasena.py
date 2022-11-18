from endpoints.functions_jwt import *
from db import *


def test_invalid_token(client):
    token = gen_session_token({'id': 1})
    response = client.post(
        f'/password_recover/{token}',
        data={'password': "asdASD123%"}
    )
    assert response.json() == {'detail': 'Invalid Token.'}
    assert response.status_code == 400


def test_invalid_user(client):
    token = gen_verification_token({'email': 'emailCualquiera@hotmail.com'})
    response = client.post(
        f'/password_recover/{token}',
        data={'password': "asdASD123%"}
    )
    assert response.status_code == 400
    assert response.json() == {'detail': "User doesn't exist."}


def test_change_invalid_password(client, user4):
    token = gen_verification_token({'email': 'test_gran_soldador@hotmail.com'})
    response = client.post(
        f'/password_recover/{token}',
        data={'password': "badpassword"}
    )
    assert response.status_code == 400
    assert response.json() == {'detail': "Password inválido, el password "
                                         "requiere al menos una mayuscula, "
                                         "una minusucula y un numero."}


def test_change_password_ok(client, user4):
    token = gen_verification_token({'email': 'test_gran_soldador@hotmail.com'})
    response = client.post(
        f'/password_recover/{token}',
        data={'password': "myNewPassword123$"}
    )
    assert response.status_code == 200
    assert response.json() == {'detail': "Password succesfully changed."}

from utils.tokens import *
from db import *


def test_verify_ok(client):
    with db_session:
        User(name='leandro',
             email='leandro.lopez@mi.unc.edu.ar',
             password='42787067', verified=False)
    token = gen_verification_token({'email': 'leandro.lopez@mi.unc.edu.ar'})
    response = client.get(
        f'/verify/{token}'
    )
    assert response.status_code == 200
    assert response.json() == {'detail': "user succesfully verified!"}


def test_already_verified(client, user1):
    token = gen_verification_token({'email': 'leandro.lopez@mi.unc.edu.ar'})
    response = client.get(
        f'/verify/{token}'
    )
    assert response.status_code == 400
    assert response.json() == {'detail': 'User already verified.'}


def test_user_not_exist(client):
    token = gen_verification_token({'email': 'leandro.lopez@mi.unc.edu.ar'})
    response = client.get(
        f'/verify/{token}'
    )
    assert response.status_code == 400
    assert response.json() == {'detail': "User doesn't exist."}


def test_invalid_token(client):
    token = gen_session_token({'id': 1})
    response = client.get(
        f'/verify/{token}'
    )
    assert response.status_code == 400
    assert response.json() == {'detail': 'Invalid token.'}

from db import *


def test_correct_edit(loggedin_client, user1):
    response = loggedin_client.post(
        '/user/edit/password',
        data={
            'old_password': '42787067',
            'new_password': '@Leandro013'
        }
    )
    assert response.status_code == 200
    with db_session:
        password = Usuario.get(user_id=user1).contraseña
    assert password == '@Leandro013'


def test_short_password(loggedin_client, user1):
    response = loggedin_client.post(
        '/user/edit/password',
        data={
            'old_password': '42787067',
            'new_password': 'abc'
        }
    )
    assert response.status_code == 400
    assert response.json() == {'detail': 'Password too Short.'}


def test_not_valid_password(loggedin_client, user1):
    response = loggedin_client.post(
        '/user/edit/password',
        data={
            'old_password': '42787067',
            'new_password': 'leandro013'
        }
    )
    assert response.status_code == 400
    assert response.json() == {'detail': 'Password inválido, el password '
                               'requiere al menos una mayuscula, '
                               'una minusucula y un numero.'}


def test_same_password(loggedin_client, user2):
    response = loggedin_client.post(
        '/user/edit/password',
        data={
            'old_password': '1234ABCDa!',
            'new_password': '1234ABCDa!'
        }
    )
    assert response.status_code == 400
    assert response.json() == {'detail': 'La contraseña debe ser distinta'}


def test_icorrect_password(loggedin_client, user2):
    response = loggedin_client.post(
        '/user/edit/password',
        data={
            'old_password': 'abc',
            'new_password': '1234ABCDa!'
        }
    )
    assert response.status_code == 400
    assert response.json() == {'detail': 'contraseña incorrecta'}

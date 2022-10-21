from fastapi.testclient import TestClient
from main import app
from db import *
import pytest

client = TestClient(app)


@pytest.fixture(autouse=True)
def reset_db():
    db.drop_all_tables(True)
    db.create_tables()


def test_correct_login():
    with db_session:
        Usuario(nombre_usuario="UsuarioDePrueba",
                email="emailDePrueba@hotmail.com",
                contraseña="contraseñaGenerica123",
                verificado=1
                )
    response = client.post(
        '/login',
        headers={'Content-type': 'application/x-www-form-urlencoded'},
        data={
            "username": "UsuarioDePrueba",
            "password": "contraseñaGenerica123"
        }
    )
    assert response.status_code == 200


def test_wrong_user_login():
    with db_session:
        Usuario(nombre_usuario="UsuarioNoExiste",
                email="emailDePruebaMalUser@hotmail.com",
                contraseña="contraseñaGenerica123",
                verificado=1
                )
    response = client.post(
        '/login',
        headers={'Content-type': 'application/x-www-form-urlencoded'},
        data={
            "username": "UsuarioQueNoExiste",
            "password": "contraseñaGenerica123"
        }
    )
    assert response.status_code == 400
    assert response.json() == {'detail': "User doesn't exist."}


def test_wrong_password_login():
    with db_session:
        Usuario(nombre_usuario="UsuarioPasswordMalo",
                email="emailDePruebaMalPassword@hotmail.com",
                contraseña="contraseñaGenerica123",
                verificado=1
                )
    response = client.post(
        '/login',
        headers={'Content-type': 'application/x-www-form-urlencoded'},
        data={
            "username": "UsuarioPasswordMalo",
            "password": "contraseñaGenericaNoExistente123"
        }

    )
    assert response.status_code == 401
    assert response.json() == {'detail': "Wrong Password."}

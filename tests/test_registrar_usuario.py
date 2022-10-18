from fastapi.testclient import TestClient
from main import app
from db import *
import pytest


client = TestClient(app)


@pytest.fixture(scope="module", autouse=True)
def reset_db():
    db.drop_all_tables(True)
    db.create_tables()


def test_correct_form_withdefaultavatar():
    response = client.post(
        'user/registro_de_usuario/',
        headers={'Content-type': 'application/x-www-form-urlencoded'},
        data={
            "username": "myUsuarioDeTestSinAvatar",
            "password": "myPasswordDeTest444",
            "useremail": "emailTest1SinAvatar@test.com",
            "userAvatar": None
        }
    )
    assert response.status_code == 200
    assert response.json() == {"new user created": "myUsuarioDeTestSinAvatar"}


def test_correct_form_with_avatar():
    with open("tests/archivosParaTests/DefaultAvatar.png", "rb") as f:
        response = client.post(
            'user/registro_de_usuario/',
            data={
                "username": "myUsuarioDeTestConAvatar",
                "password": "myPasswordDeTest444",
                "useremail": "emailTest1ConAvatar@test.com"
            },
            files={"avatar": f}
        )
        assert response.status_code == 200
        assert response.json() == {
            "new user created": "myUsuarioDeTestConAvatar"}


def test_name_too_long():
    response = client.post(
        'user/registro_de_usuario/',
        headers={'Content-type': 'application/x-www-form-urlencoded'},
        data={
            "username": "NombreDemasiadoLargoParaHacerLaPruebaDeNombre",
            "password": "myPasswordDeTest444",
            "useremail": "emailtest2@test.com",
            "userAvatar": None
        }
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "Username too long."}


def test_password_too_short():
    response = client.post(
        'user/registro_de_usuario/',
        headers={'Content-type': 'application/x-www-form-urlencoded'},
        data={
            "username": "usuarioPasswordCorto",
            "password": "hOl4",
            "useremail": "emailtest3@test.com",
            "userAvatar": None
        }
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "Password too Short."}


def test_password_without_lower():
    response = client.post(
        'user/registro_de_usuario/',
        headers={'Content-type': 'application/x-www-form-urlencoded'},
        data={
            "username": "usuarioPassword",
            "password": "PASSWORDSINLETRACHICA444",
            "useremail": "emailtest3@test.com",
            "userAvatar": None
        }
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "Password inválido, el password "
                               "requiere al menos una mayuscula, una "
                               "minusucula y un numero."}


def test_password_without_upper():
    response = client.post(
        'user/registro_de_usuario/',
        headers={'Content-type': 'application/x-www-form-urlencoded'},
        data={
            "username": "usuarioPassword",
            "password": "passwordsinmayuscula444",
            "useremail": "emailtest3@test.com",
            "userAvatar": None
        }
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "Password inválido, el password "
                               "requiere al menos una mayuscula, una "
                               "minusucula y un numero."}


def test_password_without_digit():
    response = client.post(
        'user/registro_de_usuario/',
        headers={'Content-type': 'application/x-www-form-urlencoded'},
        data={
            "username": "usuarioPassword",
            "password": "passwordSinNumeros",
            "useremail": "emailtest3@test.com",
            "userAvatar": None
        }
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "Password inválido, el password "
                               "requiere al menos una mayuscula, una "
                               "minusucula y un numero."}


def test_user_already_exist():
    with db_session:
        Usuario(nombre_usuario="usuarioQueExiste", contraseña="paSSw0rd444",
                email="emailtestUsuario@nose.com", verificado=1)

    response = client.post(
        'user/registro_de_usuario/',
        headers={'Content-type': 'application/x-www-form-urlencoded'},
        data={
            "username": "usuarioQueExiste",
            "password": "pasWordCualquiera4313",
            "useremail": "emailtestUsuarioExiste@test.com",
            "userAvatar": None
        }
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "User name already exist."}


def test_email_already_exist():
    with db_session:
        Usuario(nombre_usuario="usuarioASDK", contraseña="paSSw0rd444",
                email="emailtestEmailExiste@test.com", verificado=1)
    response = client.post(
        'user/registro_de_usuario/',
        headers={'Content-type': 'application/x-www-form-urlencoded'},
        data={
            "username": "usuarioCualquiera",
            "password": "pasWordCualquiera4313",
            "useremail": "emailtestEmailExiste@test.com",
            "userAvatar": None
        }
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "Email already registered."}


def test_invalid_email():
    response = client.post(
        'user/registro_de_usuario/',
        headers={'Content-type': 'application/x-www-form-urlencoded'},
        data={
            "username": "usuarioEmailChoto",
            "password": "passwordRandom444",
            "useremail": "emailNovalidotest",
            "userAvatar": None
        }
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "Email inválido."}


def test_invalid_avatar():
    with open("tests/archivosParaTests/notAnImage.txt", "rb") as f:
        response = client.post(
            'user/registro_de_usuario/',
            data={
                "username": "usuarioAvatarIncorrecto",
                "password": "myPasswordDeTest444",
                "useremail": "avatarincorrecto@test.com",
            },
            files={"userAvatar": f},
        )

    assert response.status_code == 400
    assert response.json() == {"detail": "File is not an image."}

import mock
from db import *


def test_correct_form_withdefaultavatar(client):
    with mock.patch("yagmail.SMTP"):
        response = client.post(
            '/user/register',
            data={
                "username": "myUsuarioDeTestSinAvatar",
                "password": "myPasswordDeTest444",
                "email": "emailTest1SinAvatar@test.com",
                "avatar": None
            }
        )
    assert response.json() == {"new user created": "myUsuarioDeTestSinAvatar"}
    assert response.status_code == 200


def test_correct_form_with_avatar(client):
    with open("tests/archivosParaTests/DefaultAvatar.png", "rb") as f:
        with mock.patch("yagmail.SMTP"):
            response = client.post(
                '/user/register',
                data={
                    "username": "myUsuarioDeTestConAvatar",
                    "password": "myPasswordDeTest444",
                    "email": "emailTest1ConAvatar@test.com"
                },
                files={"avatar": f}
            )
        assert response.status_code == 200
        assert response.json() == {
            "new user created": "myUsuarioDeTestConAvatar"}


def test_name_too_long(client):
    response = client.post(
        '/user/register',
        headers={'Content-type': 'application/x-www-form-urlencoded'},
        data={
            "username": "NombreDemasiadoLargoParaHacerLaPruebaDeNombre",
            "password": "myPasswordDeTest444",
            "email": "emailtest2@test.com",
            "avatar": None
        }
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "Username too long."}


def test_password_too_short(client):
    response = client.post(
        '/user/register',
        headers={'Content-type': 'application/x-www-form-urlencoded'},
        data={
            "username": "usuarioPasswordCorto",
            "password": "hOl4",
            "email": "emailtest3@test.com",
            "avatar": None
        }
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "Password too Short."}


def test_password_without_lower(client):
    response = client.post(
        '/user/register',
        headers={'Content-type': 'application/x-www-form-urlencoded'},
        data={
            "username": "usuarioPassword",
            "password": "PASSWORDSINLETRACHICA444",
            "email": "emailtest3@test.com",
            "avatar": None
        }
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "Password inválido, el password "
                               "requiere al menos una mayuscula, una "
                               "minusucula y un numero."}


def test_password_without_upper(client):
    response = client.post(
        '/user/register',
        headers={'Content-type': 'application/x-www-form-urlencoded'},
        data={
            "username": "usuarioPassword",
            "password": "passwordsinmayuscula444",
            "email": "emailtest3@test.com",
            "avatar": None
        }
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "Password inválido, el password "
                               "requiere al menos una mayuscula, una "
                               "minusucula y un numero."}


def test_password_without_digit(client):
    response = client.post(
        '/user/register',
        headers={'Content-type': 'application/x-www-form-urlencoded'},
        data={
            "username": "usuarioPassword",
            "password": "passwordSinNumeros",
            "email": "emailtest3@test.com",
            "avatar": None
        }
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "Password inválido, el password "
                               "requiere al menos una mayuscula, una "
                               "minusucula y un numero."}


def test_user_already_exist(client):
    with db_session:
        User(name="usuarioQueExiste", password="paSSw0rd444",
             email="emailtestUsuario@nose.com", verified=1)

    response = client.post(
        '/user/register',
        headers={'Content-type': 'application/x-www-form-urlencoded'},
        data={
            "username": "usuarioQueExiste",
            "password": "pasWordCualquiera4313",
            "email": "emailtestUsuarioExiste@test.com",
            "avatar": None
        }
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "User name already exist."}


def test_email_already_exist(client):
    with db_session:
        User(name="usuarioASDK", password="paSSw0rd444",
             email="emailtestEmailExiste@test.com", verified=1)
    response = client.post(
        '/user/register',
        headers={'Content-type': 'application/x-www-form-urlencoded'},
        data={
            "username": "usuarioCualquiera",
            "password": "pasWordCualquiera4313",
            "email": "emailtestEmailExiste@test.com",
            "avatar": None
        }
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "Email already registered."}


def test_invalid_email(client):
    response = client.post(
        '/user/register',
        headers={'Content-type': 'application/x-www-form-urlencoded'},
        data={
            "username": "usuarioEmailChoto",
            "password": "passwordRandom444",
            "email": "emailNovalidotest",
            "avatar": None
        }
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "Email inválido."}


def test_invalid_avatar(client):
    with open("tests/archivosParaTests/notAnImage.txt", "rb") as f:
        response = client.post(
            '/user/register',
            data={
                "username": "usuarioAvatarIncorrecto",
                "password": "myPasswordDeTest444",
                "email": "avatarincorrecto@test.com",
            },
            files={"avatar": f},
        )

    assert response.status_code == 400
    assert response.json() == {"detail": "File is not an image."}

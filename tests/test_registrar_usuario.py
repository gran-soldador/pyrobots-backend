from pathlib import Path
from fastapi.testclient import TestClient
from fastapi import File, UploadFile
from main import app
from db import *
import pytest

client = TestClient(app)

def test_correct_form():
    response = client.post(
        'user/registro_de_usuario/',
        headers={'Content-type': 'application/x-www-form-urlencoded'},
        data={
        "username": "myUsuarioDeTest",
        "password": "myPasswordDeTest444",
        "useremail": "emailTest1@test.com",
        "userAvatar": None
        }
    )
    assert response.status_code == 200
    assert response.json() == {"new user created": "myUsuarioDeTest"}

def test_name_too_long():
    response = client.post(
        'user/registro_de_usuario/',
        headers={'Content-type': 'application/x-www-form-urlencoded'},
        data={
        "username": "NombreDemasiadoLargoParaHacerLaPruebaDeNombreDemasiadoLargo",
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
        crear_usuario("usuarioQueExiste", "paSSw0rd444", "emailtestUsuario@nose.com")

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
        crear_usuario("usuarioASDK", "paSSw0rd444", "emailtestEmailExiste@test.com")
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


#  TODO: Hacer test para ver que se suba bien una imagen

# def test_invalid_image():
#     with db_session:
#          crear_usuario("usuarioCambioPerfil","passwOrdRandom1213","emailValido@hotmail.com")
#     response = client.post('/user/uploadavatar/', data={"username": 'usuarioCambioPerfil',
#                                                         'file': f"tests/archivosParaTests/notAnImage.txt"
#                                                         })
#     assert response.status_code == 400
#     assert response.json() == {"detail": "File is not an image."}
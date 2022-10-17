from fastapi.testclient import TestClient
from main import app
from db import *
import pytest

client = TestClient(app)


@pytest.fixture(scope="module", autouse=True)
def reset_db():
    db.drop_all_tables(True)
    db.create_tables()


def test_correct_form_subir_robot():
    with db_session:
        Usuario(
            nombre_usuario="usuarioRobotCorrectForm",
            contraseña="myPasswordDeTest444",
            email="emailTest1RObotCorrectFOmr@test.com",
            avatar="userUploads/avatars/DefaultAvatar.png",
            verificado=1
        )
    with open("tests/archivosParaTests/DefaultAvatar.png", "rb") as f:
        with open("tests/archivosParaTests/codeOfRobot.py", "rb") as c:
            response = client.post(
                '/user/creacion_de_robot/',
                data={
                    "username": "usuarioRobotCorrectForm",
                    "robotName": "nombreGenericoDeRobot"
                },
                files={"robotAvatar": f,
                       "robotCode": c
                       },
            )
            assert response.status_code == 200
            assert response.json() == {
                "new robot created": "nombreGenericoDeRobot"}


def test_user_doesnt_exist_robot():
    with open("tests/archivosParaTests/DefaultAvatar.png", "rb") as f:
        with open("tests/archivosParaTests/codeOfRobot.py", "rb") as c:
            response = client.post(
                '/user/creacion_de_robot/',
                data={
                    "username": "usuarioNoExisteRobot",
                    "robotName": "nombreGenericoDeRobot"
                },
                files={"robotAvatar": f,
                       "robotCode": c
                       },
            )
            assert response.status_code == 400
            assert response.json() == {'detail': "User doesn't exist."}


def test_user_robot_already_exist():
    with db_session:
        user = Usuario(
            nombre_usuario="usuarioRobotExist",
            contraseña="myPasswordDeTest444",
            email="emailTest1RObotExist@test.com",
            avatar="userUploads/avatars/DefaultAvatar.png",
            verificado=1
        )
        Robot(
            nombre="robotQueExiste",
            implementacion="codigo de robot aca",
            avatar="userUploads/robotAvatars/defaultAvatarRobot.png",
            partidas_ganadas=0,
            partidas_jugadas=0,
            defectuoso=False,
            usuario=user
        )
    with open("tests/archivosParaTests/DefaultAvatar.png", "rb") as f:
        with open("tests/archivosParaTests/codeOfRobot.py", "rb") as c:
            response = client.post(
                '/user/creacion_de_robot/',
                data={
                    "username": "usuarioRobotExist",
                    "robotName": "robotQueExiste"
                },
                files={"robotAvatar": f,
                       "robotCode": c
                       },
            )
            assert response.status_code == 400
            assert response.json() == {"detail": "You already have"
                                       "a robot with that name."}


def test_robot_file_not_an_image():
    with db_session:
        Usuario(
            nombre_usuario="usuarioRobotImagenMala",
            contraseña="myPasswordDeTest444",
            email="emailTestrobotMalaImagen@test.com",
            avatar="userUploads/avatars/DefaultAvatar.png",
            verificado=1
        )
    with open("tests/archivosParaTests/notAnImage.txt", "rb") as f:
        with open("tests/archivosParaTests/codeOfRobot.py", "rb") as c:
            response = client.post(
                '/user/creacion_de_robot/',
                data={
                    "username": "usuarioRobotImagenMala",
                    "robotName": "nombreGenericoDeRobotMalaImagen"
                },
                files={"robotAvatar": f,
                       "robotCode": c
                       },
            )
            assert response.status_code == 400
            assert response.json() == {'detail': "File is not an image."}


def test_robot_file_not_py():
    with db_session:
        Usuario(
            nombre_usuario="usuarioRobotNoPy",
            contraseña="myPasswordDeTest444",
            email="emailTestrobotNoPy@test.com",
            avatar="userUploads/avatars/DefaultAvatar.png",
            verificado=1
        )
    with open("tests/archivosParaTests/DefaultAvatar.png", "rb") as f:
        with open("tests/archivosParaTests/notAnImage.txt", "rb") as c:
            response = client.post(
                '/user/creacion_de_robot/',
                data={
                    "username": "usuarioRobotNoPy",
                    "robotName": "nombreGenericoDeRobotSinCOdigo"
                },
                files={"robotAvatar": f,
                       "robotCode": c
                       },
            )
            assert response.status_code == 400
            assert response.json() == {'detail': "File must be a .py"}

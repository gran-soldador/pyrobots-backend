from db import *


def test_correct_form_subir_robot(loggedin_client):
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
            response = loggedin_client.post(
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


def test_user_not_logged_in_exist_robot(client):
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
            assert response.status_code == 403
            assert response.json() == {'detail': "Not authenticated"}


def test_user_robot_already_exist(loggedin_client):
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
            response = loggedin_client.post(
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


def test_robot_file_not_an_image(loggedin_client):
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
            response = loggedin_client.post(
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


def test_robot_file_not_py(loggedin_client):
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
            response = loggedin_client.post(
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

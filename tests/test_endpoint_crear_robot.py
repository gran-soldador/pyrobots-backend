# from db import *


def test_correct_form_subir_robot(loggedin_client, user1):
    with open("tests/archivosParaTests/DefaultAvatar.png", "rb") as f:
        with open("tests/archivosParaTests/codeOfRobot.py", "rb") as c:
            response = loggedin_client.post(
                '/user/creacion_de_robot/',
                data={"robotName": "nombreGenericoDeRobot"},
                files={"robotAvatar": f, "robotCode": c},
            )
            assert response.status_code == 200
            assert response.json() == {
                "new robot created": "nombreGenericoDeRobot"}


def test_user_not_logged_in_exist_robot(client):
    with open("tests/archivosParaTests/DefaultAvatar.png", "rb") as f:
        with open("tests/archivosParaTests/codeOfRobot.py", "rb") as c:
            response = client.post(
                '/user/creacion_de_robot/',
                data={"robotName": "nombreGenericoDeRobot"},
                files={"robotAvatar": f, "robotCode": c},
            )
            assert response.status_code == 403
            assert response.json() == {'detail': "Not authenticated"}


def test_user_robot_already_exist(loggedin_client, user1, robot1):
    with open("tests/archivosParaTests/DefaultAvatar.png", "rb") as f:
        with open("tests/archivosParaTests/codeOfRobot.py", "rb") as c:
            response = loggedin_client.post(
                '/user/creacion_de_robot/',
                data={"robotName": "robocop"},
                files={"robotAvatar": f, "robotCode": c},
            )
            assert response.status_code == 400
            assert response.json() == {"detail": "You already have"
                                       "a robot with that name."}


def test_robot_file_not_an_image(loggedin_client, user1):
    with open("tests/archivosParaTests/notAnImage.txt", "rb") as f:
        with open("tests/archivosParaTests/codeOfRobot.py", "rb") as c:
            response = loggedin_client.post(
                '/user/creacion_de_robot/',
                data={"robotName": "nombreGenericoDeRobotMalaImagen"},
                files={"robotAvatar": f, "robotCode": c},
            )
            assert response.status_code == 400
            assert response.json() == {'detail': "File is not an image."}


def test_robot_file_not_py(loggedin_client, user1):
    with open("tests/archivosParaTests/DefaultAvatar.png", "rb") as f:
        with open("tests/archivosParaTests/notAnImage.txt", "rb") as c:
            response = loggedin_client.post(
                '/user/creacion_de_robot/',
                data={"robotName": "nombreGenericoDeRobotSinCOdigo"},
                files={"robotAvatar": f, "robotCode": c},
            )
            assert response.status_code == 400
            assert response.json() == {'detail': "File must be a .py"}

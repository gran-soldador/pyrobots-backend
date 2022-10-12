from fastapi.testclient import TestClient
from main import app
from db import *

client = TestClient(app)


def test_correct_form():
    with db_session:
        u1 = Usuario(nombre_usuario='leandro',
                     email='leandro.lopez@mi.unc.edu.ar',
                     contraseña='42787067', verificado=True)
        Robot(nombre='robocop', implementacion='super-robot.py',
              partidas_ganadas=0, partidas_jugadas=0,
              defectuoso=False, usuario=u1)
    response = client.post(
        'crear_partida',
        headers={'Content-type': 'application/x-www-form-urlencoded'},
        data={
            "nombre": "my-partida",
            "contraseña": None,
            "cant_jugadores": 3,
            "cant_juegos": 2,
            "cant_rondas": 3,
            "robot_id": 1
        }
    )
    assert response.status_code == 200
    assert response.json() == {'id_partida': 1}


def test_correct_form_password():
    response = client.post(
        '/crear_partida',
        headers={'Content-type': 'application/x-www-form-urlencoded'},
        data={
            "nombre": "my-partida",
            "contraseña": '42787067',
            "cant_jugadores": 3,
            "cant_juegos": 2,
            "cant_rondas": 3,
            "robot_id": 1
        }
    )
    assert response.status_code == 200
    assert response.json() == {'id_partida': 2}


def test_incorrect_form_name():
    response = client.post(
        '/crear_partida',
        headers={'Content-type': 'application/x-www-form-urlencoded'},
        data={
            "nombre": "sdlsjdldksldkdldskdslkdsldskldskdslkdslsdk",
            "cant_jugadores": 3,
            "cant_juegos": 2,
            "cant_rondas": 3,
            "robot_id": 1
        }
    )
    assert response.status_code == 400
    assert response.json() == {'detail': 'nombre invalido'}


def test_incorrect_form_name_character():
    response = client.post(
        '/crear_partida',
        headers={'Content-type': 'application/x-www-form-urlencoded'},
        data={
            "nombre": "my.partida",
            "cant_jugadores": 3,
            "cant_juegos": 2,
            "cant_rondas": 3,
            "robot_id": 1
        }
    )
    assert response.status_code == 400
    assert response.json() == {'detail': 'nombre invalido'}


def test_incorrect_pwd_name():
    response = client.post(
        '/crear_partida',
        headers={'Content-type': 'application/x-www-form-urlencoded'},
        data={
            "nombre": "my-partida",
            "contraseña": '444444444444444444444444444444444444',
            "cant_jugadores": 3,
            "cant_juegos": 2,
            "cant_rondas": 3,
            "robot_id": 1
        }
    )
    assert response.status_code == 400
    assert response.json() == {'detail': 'contraseña invalida'}


def test_incorrect_form_pwd_character():
    response = client.post(
        '/crear_partida',
        headers={'Content-type': 'application/x-www-form-urlencoded'},
        data={
            "nombre": "my-partida",
            "contraseña": "42.5",
            "cant_jugadores": 3,
            "cant_juegos": 2,
            "cant_rondas": 3,
            "robot_id": 1
        }
    )
    assert response.status_code == 400
    assert response.json() == {'detail': 'contraseña invalida'}


def test_incorrect_form_jugadores():
    response = client.post(
        '/crear_partida',
        headers={'Content-type': 'application/x-www-form-urlencoded'},
        data={
            "nombre": "my-partida",
            "contraseña": '42787067',
            "cant_jugadores": 1,
            "cant_juegos": 2,
            "cant_rondas": 3,
            "robot_id": 1
        }
    )
    assert response.status_code == 400
    assert response.json() == {'detail': 'número de jugadores invalido'}


def test_incorrect_form_jugadores_max():
    response = client.post(
        '/crear_partida',
        headers={'Content-type': 'application/x-www-form-urlencoded'},
        data={
            "nombre": "my-partida",
            "contraseña": '42787067',
            "cant_jugadores": 5,
            "cant_juegos": 2,
            "cant_rondas": 3,
            "robot_id": 1
        }
    )
    assert response.status_code == 400
    assert response.json() == {'detail': 'número de jugadores invalido'}


def test_incorrect_form_juegos():
    response = client.post(
        '/crear_partida',
        headers={'Content-type': 'application/x-www-form-urlencoded'},
        data={
            "nombre": "my-partida",
            "contraseña": '42787067',
            "cant_jugadores": 2,
            "cant_juegos": 0,
            "cant_rondas": 3,
            "robot_id": 1
        }
    )
    assert response.status_code == 400
    assert response.json() == {'detail': 'número de juegos invalido'}


def test_incorrect_form_juegos_max():
    response = client.post(
        '/crear_partida',
        headers={'Content-type': 'application/x-www-form-urlencoded'},
        data={
            "nombre": "my-partida",
            "contraseña": '42787067',
            "cant_jugadores": 2,
            "cant_juegos": 500,
            "cant_rondas": 3,
            "robot_id": 1
        }
    )
    assert response.status_code == 400
    assert response.json() == {'detail': 'número de juegos invalido'}


def test_incorrect_form_rondas():
    response = client.post(
        '/crear_partida',
        headers={'Content-type': 'application/x-www-form-urlencoded'},
        data={
            "nombre": "my-partida",
            "contraseña": '42787067',
            "cant_jugadores": 2,
            "cant_juegos": 1,
            "cant_rondas": 0,
            "robot_id": 1
        }
    )
    assert response.status_code == 400
    assert response.json() == {'detail': 'número de rondas invalido'}


def test_incorrect_form_rondas_max():
    response = client.post(
        '/crear_partida',
        headers={'Content-type': 'application/x-www-form-urlencoded'},
        data={
            "nombre": "my-partida",
            "contraseña": '42787067',
            "cant_jugadores": 2,
            "cant_juegos": 200,
            "cant_rondas": 1000000,
            "robot_id": 1
        }
    )
    assert response.status_code == 400
    assert response.json() == {'detail': 'número de rondas invalido'}


def test_incorrect_form_robot():
    response = client.post(
        '/crear_partida',
        headers={'Content-type': 'application/x-www-form-urlencoded'},
        data={
            "nombre": "my-partida",
            "contraseña": '42787067',
            "cant_jugadores": 2,
            "cant_juegos": 200,
            "cant_rondas": 3,
            "robot_id": 0
        }
    )
    assert response.status_code == 400
    assert response.json() == {'detail': 'robot no valido'}


def test_incorrect_form_robot_defect():
    with db_session:
        u1 = Usuario(nombre_usuario='leandr',
                     email='leandr.lopez@mi.unc.edu.ar',
                     contraseña='42787067', verificado=True)
        Robot(nombre='robocop', implementacion='super-robot.py',
              partidas_ganadas=0, partidas_jugadas=0,
              defectuoso=True, usuario=u1)
    response = client.post(
        '/crear_partida',
        headers={'Content-type': 'application/x-www-form-urlencoded'},
        data={
            "nombre": "my-partida",
            "contraseña": '42787067',
            "cant_jugadores": 2,
            "cant_juegos": 200,
            "cant_rondas": 3,
            "robot_id": 2
        }
    )
    assert response.status_code == 400
    assert response.json() == {'detail': 'robot defectuoso'}

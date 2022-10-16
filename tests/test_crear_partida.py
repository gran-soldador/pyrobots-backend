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
        'crear-partida',
        headers={'Content-type': 'application/x-www-form-urlencoded'},
        data={
            "namepartida": "my-partida",
            "password": None,
            "numplayers": 3,
            "numgames": 2,
            "numrondas": 3,
            "idrobot": 1
        }
    )
    assert response.status_code == 200
    assert response.json() == {'id_partida': 1}


def test_correct_form_password():
    response = client.post(
        'crear-partida',
        headers={'Content-type': 'application/x-www-form-urlencoded'},
        data={
            "namepartida": "my-partida",
            "password": '42787067',
            "numplayers": 3,
            "numgames": 2,
            "numrondas": 3,
            "idrobot": 1
        }
    )
    assert response.status_code == 200
    assert response.json() == {'id_partida': 2}


def test_incorrect_form_name():
    response = client.post(
        'crear-partida',
        headers={'Content-type': 'application/x-www-form-urlencoded'},
        data={
            "namepartida": "sdlsjdldksldkdldskdslkdsldskldskdslkdslsdk",
            "numplayers": 3,
            "numgames": 2,
            "numrondas": 3,
            "idrobot": 1
        }
    )
    assert response.status_code == 400
    assert response.json() == {'detail': 'namepartida invalido'}


def test_incorrect_form_name_character():
    response = client.post(
        'crear-partida',
        headers={'Content-type': 'application/x-www-form-urlencoded'},
        data={
            "namepartida": "my.partida",
            "numplayers": 3,
            "numgames": 2,
            "numrondas": 3,
            "idrobot": 1
        }
    )
    assert response.status_code == 400
    assert response.json() == {'detail': 'namepartida invalido'}


def test_incorrect_pwd_name():
    response = client.post(
        'crear-partida',
        headers={'Content-type': 'application/x-www-form-urlencoded'},
        data={
            "namepartida": "my-partida",
            "password": '444444444444444444444444444444444444',
            "numplayers": 3,
            "numgames": 2,
            "numrondas": 3,
            "idrobot": 1
        }
    )
    assert response.status_code == 400
    assert response.json() == {'detail': 'password invalida'}


def test_incorrect_form_pwd_character():
    response = client.post(
        'crear-partida',
        headers={'Content-type': 'application/x-www-form-urlencoded'},
        data={
            "namepartida": "my-partida",
            "password": "42.5",
            "numplayers": 3,
            "numgames": 2,
            "numrondas": 3,
            "idrobot": 1
        }
    )
    assert response.status_code == 400
    assert response.json() == {'detail': 'password invalida'}


def test_incorrect_form_jugadores():
    response = client.post(
        'crear-partida',
        headers={'Content-type': 'application/x-www-form-urlencoded'},
        data={
            "namepartida": "my-partida",
            "password": '42787067',
            "numplayers": 1,
            "numgames": 2,
            "numrondas": 3,
            "idrobot": 1
        }
    )
    assert response.status_code == 400
    assert response.json() == {'detail': 'numplayers invalido'}


def test_incorrect_form_jugadores_max():
    response = client.post(
        'crear-partida',
        headers={'Content-type': 'application/x-www-form-urlencoded'},
        data={
            "namepartida": "my-partida",
            "password": '42787067',
            "numplayers": 5,
            "numgames": 2,
            "numrondas": 3,
            "idrobot": 1
        }
    )
    assert response.status_code == 400
    assert response.json() == {'detail': 'numplayers invalido'}


def test_incorrect_form_juegos():
    response = client.post(
        'crear-partida',
        headers={'Content-type': 'application/x-www-form-urlencoded'},
        data={
            "namepartida": "my-partida",
            "password": '42787067',
            "numplayers": 2,
            "numgames": 0,
            "numrondas": 3,
            "idrobot": 1
        }
    )
    assert response.status_code == 400
    assert response.json() == {'detail': 'numgames invalido'}


def test_incorrect_form_juegos_max():
    response = client.post(
        'crear-partida',
        headers={'Content-type': 'application/x-www-form-urlencoded'},
        data={
            "namepartida": "my-partida",
            "password": '42787067',
            "numplayers": 2,
            "numgames": 500,
            "numrondas": 3,
            "idrobot": 1
        }
    )
    assert response.status_code == 400
    assert response.json() == {'detail': 'numgames invalido'}


def test_incorrect_form_rondas():
    response = client.post(
        'crear-partida',
        headers={'Content-type': 'application/x-www-form-urlencoded'},
        data={
            "namepartida": "my-partida",
            "password": '42787067',
            "numplayers": 2,
            "numgames": 1,
            "numrondas": 0,
            "idrobot": 1
        }
    )
    assert response.status_code == 400
    assert response.json() == {'detail': 'numrondas invalido'}


def test_incorrect_form_rondas_max():
    response = client.post(
        'crear-partida',
        headers={'Content-type': 'application/x-www-form-urlencoded'},
        data={
            "namepartida": "my-partida",
            "password": '42787067',
            "numplayers": 2,
            "numgames": 200,
            "numrondas": 1000000,
            "idrobot": 1
        }
    )
    assert response.status_code == 400
    assert response.json() == {'detail': 'numrondas invalido'}


def test_incorrect_form_robot():
    response = client.post(
        'crear-partida',
        headers={'Content-type': 'application/x-www-form-urlencoded'},
        data={
            "namepartida": "my-partida",
            "password": '42787067',
            "numplayers": 2,
            "numgames": 200,
            "numrondas": 3,
            "idrobot": 0
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
        'crear-partida',
        headers={'Content-type': 'application/x-www-form-urlencoded'},
        data={
            "namepartida": "my-partida",
            "password": '42787067',
            "numplayers": 2,
            "numgames": 200,
            "numrondas": 3,
            "idrobot": 2
        }
    )
    assert response.status_code == 400
    assert response.json() == {'detail': 'robot defectuoso'}
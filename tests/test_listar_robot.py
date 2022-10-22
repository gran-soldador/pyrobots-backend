from fastapi.testclient import TestClient
from db import *
from endpoints.functions_jwt import authenticated_user

from main import app
import pytest

client = TestClient(app)
app.dependency_overrides[authenticated_user] = lambda: 1


@pytest.fixture(autouse=True)
def reset_db():
    db.drop_all_tables(True)
    db.create_tables()


def test_empty_robot_list():
    with db_session:
        Usuario(nombre_usuario='pedro',
                email='pedro.lopez@mi.unc.edu.ar',
                contraseña='42787067', verificado=True)
    response = client.get('/lista-robots',
                           headers={'Content-type':
                                    'application/x-www-form-urlencoded'},
                           data={"username": "pedro"})
    assert response.status_code == 400
    assert response.json() == {'detail': 'No se encontraron robots'}


def test_non_empty_robot_list():
    with db_session:
        u = Usuario(nombre_usuario='pedro',
                    email='pedro.lopez@mi.unc.edu.ar',
                    contraseña='42787067', verificado=True)
        Robot(nombre='rob', implementacion='hola', partidas_ganadas=0,
              partidas_jugadas=0, defectuoso=False, usuario=u)
    response = client.get('/lista-robots', data={"username": "pedro"})
    assert response.status_code == 200
    assert response.json() == [{'id': 1, 'nombre': 'rob'}]

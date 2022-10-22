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


def test_empty_list():
    response = client.get('/lista-partidas')
    assert response.status_code == 400
    assert response.json() == {'detail': 'No se encontraron partidas'}


def test_non_empty_list():
    with db_session:
        u1 = Usuario(nombre_usuario='leandro',
                     email='leandro.lopez@mi.unc.edu.ar',
                     contraseña='42787067', verificado=True)
        Partida(namepartida='my_partida', status='disponible',
                minplayers=3, maxplayers=3, numgames=10, numrondas=10,
                creador=u1)
    response = client.get('/lista-partidas')
    assert response.status_code == 200
    assert response.json()[0]['password'] is False

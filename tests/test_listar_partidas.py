from fastapi.testclient import TestClient
from db import *
from main import app
import pytest

client = TestClient(app)


@pytest.fixture(scope="module", autouse=True)
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
                numplayers=3, numgames=10, numrondas=10,
                creador=u1)
    response = client.get('/lista-partidas')
    assert response.status_code == 200
    assert response.json()[0]['password'] is False

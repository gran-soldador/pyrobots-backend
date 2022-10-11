from fastapi.testclient import TestClient
from db import *
from main import app

client = TestClient(app)


def test_empty_list():
    response = client.get('/lista_partidas')
    assert response.status_code == 400
    assert response.json() == {'detail': 'No se encontraron partidas'}


def test_non_empty_list():
    with db_session:
        u1 = Usuario(nombre_usuario='leandro',
                     email='leandro.lopez@mi.unc.edu.ar',
                     contraseña='42787067', verificado=True)
        Partida(nombre='my_partida', status='disponible',
                cant_jugadores=3, cant_juegos=10, cant_rondas=10,
                creador=u1)
        response = client.get('/lista_partidas')
        assert response.status_code == 200
        assert response.json()[0]['partida_nombre'] == 'my_partida'

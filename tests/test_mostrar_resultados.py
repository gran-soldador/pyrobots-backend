from db import *


def test_correct_match(client, user1, robot1):
    with db_session:
        p = Partida(namepartida='partida', status='finalizada', minplayers=2,
                    maxplayers=2, numgames=10, numrondas=10,
                    creador=Usuario[user1], ganador=Robot[robot1])
        p.participante.add(Robot[robot1])
    response = client.get(
        '/match/results/1'
    )
    assert response.status_code == 200
    assert response.json() == [{
                               'id': 1,
                               'robot': 'RandomRobot',
                               'user': 'leandro'
                               }]


def test_unfinished_match(client, partida1):
    response = client.get(
        '/match/results/1'
    )
    assert response.status_code == 400
    assert response.json() == {'detail': 'la partida no tiene resultados'}


def test_nonexist_match(client):
    response = client.get(
        '/match/results/7'
    )
    assert response.status_code == 400
    assert response.json() == {'detail': 'la partida no existe'}

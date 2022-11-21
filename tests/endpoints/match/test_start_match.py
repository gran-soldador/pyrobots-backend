import mock

from db import *


def test_correct_start(loggedin_client, match5):
    with db_session:
        robot_ids = [r.id for r in Match[match5].players]
    res = (dict(zip(robot_ids, [0, 20])), dict(zip(robot_ids, [0, 1])))
    with mock.patch("utils.websocket.lobby_manager.broadcast",
                    return_value=None):
        with mock.patch("engine.GameManager.match", return_value=res):
            response = loggedin_client.post(
                '/match/start',
                data={'match_id': match5}
            )
    assert response.status_code == 200


def test_incorrect_user(loggedin_client2, match5):
    response = loggedin_client2.post(
        '/match/start',
        data={'match_id': match5}
    )
    assert response.status_code == 400
    assert response.json() == {'detail': 'permiso denegado'}


def test_incorrect_players(loggedin_client, match3):
    response = loggedin_client.post(
        '/match/start',
        data={'match_id': match3}
    )
    assert response.status_code == 400
    assert response.json() == {'detail': 'jugadores insuficientes'}


def test_incorrect_match(loggedin_client):
    response = loggedin_client.post(
        '/match/start',
        data={'match_id': 15}
    )
    assert response.status_code == 400
    assert response.json() == {'detail': 'la partida no existe'}


def test_incorrect_status(loggedin_client, match6):
    response = loggedin_client.post(
        '/match/start',
        data={'match_id': match6}
    )
    assert response.status_code == 400
    assert response.json() == {'detail': 'la partida ya fue iniciada'}

import pytest
from db import *
import mock


@pytest.fixture
def valid_form(robot1):
    return {
        "name": "my-partida",
        "password": None,
        "minplayers": 3,
        "maxplayers": 3,
        "numgames": 2,
        "numrounds": 3,
        "robot_id": robot1
    }


@pytest.mark.parametrize("password", [None, "42787067"])
def test_correct_form(loggedin_client, valid_form, user1, password):
    with mock.patch("utils.websocket.lobby_manager.broadcast"):
        response = loggedin_client.post(
            '/match/new',
            data={**valid_form, "password": password}
        )
    assert response.status_code == 200
    with db_session:
        assert Match.select().count() == 1
        assert Match[1].owner.id == user1
        assert Match[1].password == password


def test_logged_out(client, valid_form):
    response = client.post('/match/new', data=valid_form)
    assert response.status_code == 403
    assert response.json() == {'detail': 'Not authenticated'}
    with db_session:
        assert not Match.select().exists()


@pytest.mark.parametrize("invalid_params, expected_detail", [
    pytest.param(
        {"name": "sdlsjdldksldkdldskdslkdsldskldskdslkdslsdk"},
        'namepartida invalido',
        id="name_too_long"),
    pytest.param(
        {"name": "my.partida"},
        'namepartida invalido',
        id="name_with_invalid_char"),
    pytest.param(
        {"password": "444444444444444444444444444444444444"},
        'password invalida',
        id="password_too_long"),
    pytest.param(
        {"password": "42.5"},
        'password invalida',
        id="password_with_invalid_char"),
    pytest.param(
        {"minplayers": "1"},
        'minplayers o maxplayers invalido',
        id="minplayers_too_small"),
    pytest.param(
        {"maxplayers": "5"},
        'minplayers o maxplayers invalido',
        id="maxplayers_too_large"),
    pytest.param(
        {"minplayers": 4, "maxplayers": 2},
        'minplayers o maxplayers invalido',
        id="players_absurd"),
    pytest.param(
        {"numgames": 0},
        'numgames invalido',
        id="numgames_too_small"),
    pytest.param(
        {"numgames": 500},
        'numgames invalido',
        id="numgames_too_large"),
    pytest.param(
        {"numrounds": 0},
        'numrondas invalido',
        id="numrounds_too_small"),
    pytest.param(
        {"numrounds": 1000000},
        'numrondas invalido',
        id="numrounds_too_large"),
    pytest.param(
        {"robot_id": 27},
        'robot no valido',
        id="robot_not_existent"),
])
def test_incorrect_field(loggedin_client, valid_form, invalid_params,
                         expected_detail):
    response = loggedin_client.post(
        '/match/new',
        data={**valid_form, **invalid_params}
    )
    assert response.status_code == 400
    assert response.json() == {'detail': expected_detail}
    with db_session:
        assert not Match.select().exists()


def test_defective_robot(loggedin_client, valid_form, robot1):
    with db_session:
        Robot[robot1].defective = True
    response = loggedin_client.post(
        '/match/new',
        data=valid_form
    )
    assert response.status_code == 400
    assert response.json() == {'detail': 'robot defectuoso'}
    with db_session:
        assert not Match.select().exists()


def test_not_my_robot(loggedin_client, valid_form, robot1, user2):
    with db_session:
        Robot[robot1].user = User[user2]
    response = loggedin_client.post('/match/new', data=valid_form)
    assert response.status_code == 401
    assert response.json() == {'detail': 'robot no pertenece al usuario'}
    with db_session:
        assert not Match.select().exists()

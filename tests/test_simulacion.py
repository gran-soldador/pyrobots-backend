import mock
from dataclasses import asdict

from engine.outputmodels import SimulationResult


def test_simulation_wrong_robots(loggedin_client):
    response = loggedin_client.post(
        '/create_simulation',
        data={
            "rounds": 1,
            "robot_ids": 'asd'
        }
    )
    assert response.status_code == 400
    detail = 'invalid robot list'
    assert response.json() == {'detail': detail}


def test_simulation_less_robots(loggedin_client):
    response = loggedin_client.post(
        '/create_simulation',
        data={
            "rounds": 1,
            "robot_ids": '1'
        }
    )
    assert response.status_code == 400
    detail = 'not enough robots, at least 2 must be selected'
    assert response.json() == {'detail': detail}


def test_simulation_many_robots(loggedin_client):
    response = loggedin_client.post(
        '/create_simulation',
        data={
            "rounds": 1,
            "robot_ids": '1,2,3,4,5'
        }
    )
    assert response.status_code == 400
    assert response.json() == {'detail': 'too many robots'}


def test_simulation_bad_rounds(loggedin_client):
    response = loggedin_client.post(
        '/create_simulation',
        data={
            "rounds": 10000000,
            "robot_ids": '1,2,3,4'
        }
    )
    assert response.status_code == 400
    detail = 'the number of rounds must be between 1 and 10000'
    assert response.json() == {'detail': detail}


def test_simulation_bad_id(loggedin_client, robot1, robot2, robot3):
    response = loggedin_client.post(
        '/create_simulation',
        data={
            "rounds": 1,
            "robot_ids": f'{robot1},{robot2},{robot3}'
        }
    )
    assert response.status_code == 404
    assert response.json() == {'detail': 'Robot does not exist'}


def test_simulation_robot_not_mine(loggedin_client, robot1, robot2, robot3):
    response = loggedin_client.post(
        '/create_simulation',
        data={
            "rounds": 1,
            "robot_ids": f'{robot1},{robot2},{robot3}'
        }
    )
    assert response.status_code == 404
    assert response.json() == {'detail': 'Robot does not exist'}


def test_simulation_ok(loggedin_client, robot1, robot3, robot4):
    res = SimulationResult(rounds_played=10, players=[], winners=[],
                           maxrounds=10, rounds=[])
    with mock.patch("engine.Game.simulation", return_value=res):
        response = loggedin_client.post(
            '/create_simulation',
            data={
                "rounds": 1,
                "robot_ids": f'{robot1},{robot4},{robot3}'
            }
        )
    assert response.status_code == 200
    assert response.json() == asdict(res)


def test_simulation_fail(loggedin_client, robot1, robot3, robot4):
    with mock.patch("engine.Game.simulation", side_effect=ValueError()):
        response = loggedin_client.post(
            '/create_simulation',
            data={
                "rounds": 1,
                "robot_ids": f'{robot1},{robot4},{robot3}'
            }
        )
    assert response.status_code == 500
    assert response.json() == {'detail': 'Simulation error'}

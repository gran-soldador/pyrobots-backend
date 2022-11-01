import mock


def test_simulacion_less_robots(loggedin_client):
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


def test_simulacion_many_robots(loggedin_client):
    response = loggedin_client.post(
        '/create_simulation',
        data={
            "rounds": 1,
            "robot_ids": '1,2,3,4,5'
        }
    )
    assert response.status_code == 400
    assert response.json() == {'detail': 'too many robots'}


def test_simulacion_bad_rounds(loggedin_client):
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


def test_simulacion_bad_id(loggedin_client, robot1, robot2, robot3):
    response = loggedin_client.post(
        '/create_simulation',
        data={
            "rounds": 1,
            "robot_ids": '1,2,3,4'
        }
    )
    assert response.status_code == 404
    assert response.json() == {'detail': 'Robot does not exist'}


def test_simulacion_ok(loggedin_client, robot1, robot2, robot3, robot4):
    response = loggedin_client.post(
        '/create_simulation',
        data={
            "rounds": 1,
            "robot_ids": '1,2,3,4'
        }
    )
    assert response.status_code == 200


def test_simulacion_fail(loggedin_client, robot1, robot2, robot3, robot4):
    with mock.patch("engine.Game.simulation", side_effect=ValueError()):
        response = loggedin_client.post(
            '/create_simulation',
            data={
                "rounds": 1,
                "robot_ids": '1,2,3,4'
            }
        )
    assert response.status_code == 400
    assert response.json() == {'detail': 'error en la simulación'}

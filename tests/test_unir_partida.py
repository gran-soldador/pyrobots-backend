import mock


def test_correct_union(loggedin_client2, partida1, robot2):
    with mock.patch("websocket.lobby_manager.broadcast", return_value=None):
        response = loggedin_client2.post(
            '/match/join',
            data={
                'match_id': partida1,
                'robot_id': robot2
            }
        )
    assert response.status_code == 200


def test_correct_password_union(loggedin_client2, partida2, robot2):
    with mock.patch("websocket.lobby_manager.broadcast", return_value=None):
        response = loggedin_client2.post(
            '/match/join',
            data={
                'match_id': partida2,
                'password': 'leandro',
                'robot_id': robot2
            }
        )
    assert response.status_code == 200


def test_incorrect_password_union(loggedin_client2, partida2, robot2):
    response = loggedin_client2.post(
        '/match/join',
        data={
            'match_id': partida2,
            'password': 'leandr',
            'robot_id': robot2
        }
    )
    assert response.status_code == 400
    assert response.json() == {'detail': 'contraseña incorrecta'}


def test_creator_union(loggedin_client, partida2, robot2):
    response = loggedin_client.post(
        '/match/join',
        data={
            'match_id': partida2,
            'password': 'leandro',
            'robot_id': robot2
        }
    )
    assert response.status_code == 400
    assert response.json() == {'detail': 'no puede unirse a su propia partida'}


def test_incorrect_robot_union(loggedin_client2, partida2, user2, robot1):
    response = loggedin_client2.post(
        '/match/join',
        data={
            'match_id': partida2,
            'password': 'leandro',
            'robot_id': robot1
        }
    )
    assert response.status_code == 400
    assert response.json() == {'detail': 'el robot no pertenece al usuario'}


def test_inex_robot_union(loggedin_client2, partida2, user2):
    response = loggedin_client2.post(
        '/match/join',
        data={
            'match_id': partida2,
            'password': 'leandro',
            'robot_id': 15
        }
    )
    assert response.status_code == 400
    assert response.json() == {'detail': 'el robot no existe'}


def test_inex_match_union(loggedin_client2, robot2):
    response = loggedin_client2.post(
        '/match/join',
        data={
            'match_id': 15,
            'password': 'leandro',
            'robot_id': robot2
        }
    )
    assert response.status_code == 400
    assert response.json() == {'detail': 'la partida no existe'}


def test_non_disp_union(loggedin_client2, partida3, robot2):
    response = loggedin_client2.post(
        '/match/join',
        data={
            'match_id': partida3,
            'password': 'leandro',
            'robot_id': robot2
        }
    )
    assert response.status_code == 400
    assert response.json() == {'detail': 'partida no disponible'}


def test_same_user_union(loggedin_client2, partida4, robot2):
    response = loggedin_client2.post(
        '/match/join',
        data={
            'match_id': partida4,
            'password': 'leandro',
            'robot_id': robot2
        }
    )
    assert response.status_code == 400
    assert response.json() == {'detail': 'usuario ya unido'}


def test_full_user_union(loggedin_client2, partida5, robot2):
    with mock.patch("websocket.lobby_manager.broadcast", return_value=None):
        response = loggedin_client2.post(
            '/match/join',
            data={
                'match_id': partida5,
                'password': 'leandro',
                'robot_id': robot2
            }
        )
    assert response.status_code == 200

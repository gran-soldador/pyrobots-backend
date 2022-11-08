import mock


def test_correct_quit(loggedin_client2, partida4):
    with mock.patch("websocket.lobby_manager.broadcast", return_value=None):
        response = loggedin_client2.post(
            '/match/exit',
            data={'match_id': partida4}
        )
    assert response.status_code == 200


def test_creator_quit(loggedin_client, partida2):
    response = loggedin_client.post(
        '/match/exit',
        data={'match_id': partida2}
    )
    assert response.status_code == 400
    assert response.json() == {'detail': 'el creador no puede abandonar'}


def test_incorrect_match(loggedin_client):
    response = loggedin_client.post(
        '/match/exit',
        data={'match_id': 15}
    )
    assert response.status_code == 400
    assert response.json() == {'detail': 'la partida no existe'}


def test_inexistent_user(loggedin_client2, partida1):
    response = loggedin_client2.post(
        '/match/exit',
        data={'match_id': partida1}
    )
    assert response.status_code == 400
    assert response.json() == {'detail': 'no es un participante'}


def test_non_user(loggedin_client2, partida6):
    response = loggedin_client2.post(
        '/match/exit',
        data={'match_id': partida6}
    )
    assert response.status_code == 400
    assert response.json() == {'detail': 'ya no tiene permitido abandonar'}

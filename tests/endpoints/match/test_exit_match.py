import mock


def test_correct_quit(loggedin_client2, match4):
    with mock.patch("utils.websocket.lobby_manager.broadcast", return_value=None):
        response = loggedin_client2.post(
            '/match/exit',
            data={'match_id': match4}
        )
    assert response.status_code == 200


def test_creator_quit(loggedin_client, match2):
    response = loggedin_client.post(
        '/match/exit',
        data={'match_id': match2}
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


def test_inexistent_user(loggedin_client2, match1):
    response = loggedin_client2.post(
        '/match/exit',
        data={'match_id': match1}
    )
    assert response.status_code == 400
    assert response.json() == {'detail': 'no es un participante'}


def test_non_user(loggedin_client2, match6):
    response = loggedin_client2.post(
        '/match/exit',
        data={'match_id': match6}
    )
    assert response.status_code == 400
    assert response.json() == {'detail': 'ya no tiene permitido abandonar'}

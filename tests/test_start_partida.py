def test_correct_start(loggedin_client, partida5):
    response = loggedin_client.post(
        '/iniciar-partida',
        data={'partida_id': partida5}
    )
    assert response.status_code == 200
    assert response.json() == {'detail': 'iniciada'}


def test_incorrect_user(loggedin_client2, partida5):
    response = loggedin_client2.post(
        '/iniciar-partida',
        data={'partida_id': partida5}
    )
    assert response.status_code == 400
    assert response.json() == {'detail': 'permiso denegado'}


def test_incorrect_players(loggedin_client, partida3):
    response = loggedin_client.post(
        '/iniciar-partida',
        data={'partida_id': partida3}
    )
    assert response.status_code == 400
    assert response.json() == {'detail': 'jugadores insuficientes'}


def test_incorrect_match(loggedin_client):
    response = loggedin_client.post(
        '/iniciar-partida',
        data={'partida_id': 15}
    )
    assert response.status_code == 400
    assert response.json() == {'detail': 'la partida no existe'}


def test_incorrect_status(loggedin_client, partida6):
    response = loggedin_client.post(
        '/iniciar-partida',
        data={'partida_id': partida6}
    )
    assert response.status_code == 400
    assert response.json() == {'detail': 'la partida ya fue iniciada'}

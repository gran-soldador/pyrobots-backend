def test_empty_list(client):
    response = client.get('/lista-partidas')
    assert response.status_code == 400
    assert response.json() == {'detail': 'No se encontraron partidas'}


def test_non_empty_list(client, user1, partida1):
    response = client.get('/lista-partidas')
    assert response.status_code == 200
    assert response.json()[0]['password'] is False

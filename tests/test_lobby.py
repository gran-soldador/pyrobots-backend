def test_websocket(client, partida1, partida2):
    with client.websocket_connect("/ws/2") as websocket:
        data = websocket.receive_json()
        assert data == {'event': 'created',
                        'robots': [{'id': 1, 'nombre': 'robocop'}]
                        }


def test_websocket2(client, partida1):
    with client.websocket_connect("/ws/1") as websocket:
        data = websocket.receive_json()
        websocket.send_json({1: "a"})
        data = websocket.receive_json()
        assert data == {'1': 'a'}

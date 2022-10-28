def test_websocket(client, partida1):
    with client.websocket_connect("/ws/1") as websocket:
        data = websocket.receive_json()
        assert data == {'event': 'created',
                        'creador': 'leandro',
                        'robot': [{'id': 1, 'nombre': 'robocop',
                                   'usuario': 'leandro'}]
                        }


def test_websocket_incorrect(client):
    with client.websocket_connect("/ws/2") as websocket:
        data = websocket.receive_json()
        assert data == {'detail': 'room doesnt exist'}


def test_websocket_send(client, partida1):
    with client.websocket_connect("/ws/1") as websocket:
        data = websocket.receive_json()
        websocket.send_json({'deatil': 'hola'})
        data = websocket.receive_json()
        assert data == {'deatil': 'hola'}


def test_websocket_except(client, partida1, partida2):
    with client.websocket_connect("/ws/2") as websocket:
        data = websocket.receive_json()
        assert data == {'event': 'start',
                        'creador': 'leandro',
                        'robot': [{'id': 1, 'nombre': 'robocop',
                                  'usuario': 'leandro'}]
                        }

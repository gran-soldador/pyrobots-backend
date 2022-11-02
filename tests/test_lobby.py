from websocket import lobby_manager


def test_websocket(client, partida1):
    with client.websocket_connect("/ws/1") as websocket:
        data = websocket.receive_json()
        assert data == {'event': 'created',
                        'creador': 'leandro',
                        'contraseña': False,
                        'robot': [{'id': 1, 'nombre': 'RandomRobot',
                                   'usuario': 'leandro'}]
                        }


def test_websocket_incorrect(client):
    with client.websocket_connect("/ws/2") as websocket:
        data = websocket.receive_json()
        assert data == {'event': 'room not found',
                        'creador': None,
                        'contraseña': None,
                        'robot': None
                        }


def test_websocket_send(client, partida1):
    with client.websocket_connect("/ws/1") as websocket:
        data = websocket.receive_json()
        websocket.send_text("finish")
        data = websocket.receive_json()
        assert data == {'event': 'finish',
                        'creador': 'leandro',
                        'contraseña': False,
                        'robot': [{'id': 1, 'nombre': 'RandomRobot',
                                   'usuario': 'leandro'}]
                        }


def test_websocket_except(client, partida1):
    del lobby_manager.last_msg[partida1]
    with client.websocket_connect("/ws/1") as websocket:
        data = websocket.receive_json()
        assert data == {'event': 'start',
                        'creador': 'leandro',
                        'contraseña': False,
                        'robot': [{'id': 1, 'nombre': 'RandomRobot',
                                  'usuario': 'leandro'}]
                        }

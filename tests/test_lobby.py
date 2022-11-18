from db import *


def test_websocket(client, user1):
    with db_session:
        Partida(partida_id=-1, namepartida='my_partida', status='disponible',
                minplayers=3, maxplayers=3, numgames=10, numrondas=10,
                creador=Usuario[user1])
    with client.websocket_connect("/ws/-1") as websocket:
        data = websocket.receive_json()
    assert data == {'event': 'start',
                    'creator': 'leandro',
                    'password': False,
                    'robots': []
                    }


def test_websocket_incorrect(client):
    with client.websocket_connect("/ws/2") as websocket:
        data = websocket.receive_json()
    assert data == {'event': 'room not found',
                    'creator': None,
                    'password': None,
                    'robots': None
                    }


def test_websocket_send(client, user1):
    with db_session:
        Partida(partida_id=-2, namepartida='my_partida', status='disponible',
                minplayers=3, maxplayers=3, numgames=10, numrondas=10,
                creador=Usuario[user1])
    with client.websocket_connect("/ws/-2") as websocket:
        data = websocket.receive_json()
        websocket.send_text("finish")
        data = websocket.receive_json()
    assert data == {'event': 'finish',
                    'creator': 'leandro',
                    'password': False,
                    'robots': []
                    }


def test_websocket_last_msg(client, user1):
    with db_session:
        Partida(partida_id=-3, namepartida='my_partida', status='disponible',
                minplayers=3, maxplayers=3, numgames=10, numrondas=10,
                creador=Usuario[user1])
    with client.websocket_connect("/ws/-3") as websocket:
        data = websocket.send_text('test')
    with client.websocket_connect("/ws/-3") as websocket:
        data = websocket.receive_json()
    assert data == {'event': 'test',
                    'creator': 'leandro',
                    'password': False,
                    'robots': []
                    }

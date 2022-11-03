from db import *


def test_websocket(client, user1):
    with db_session:
        Partida(partida_id=-1, namepartida='my_partida', status='disponible',
                minplayers=3, maxplayers=3, numgames=10, numrondas=10,
                creador=Usuario[user1])
    with client.websocket_connect("/ws/-1") as websocket:
        data = websocket.receive_json()
    assert data == {'event': 'start',
                    'creador': 'leandro',
                    'contraseña': False,
                    'robot': []
                    }


def test_websocket_incorrect(client):
    with client.websocket_connect("/ws/2") as websocket:
        data = websocket.receive_json()
    assert data == {'event': 'room not found',
                    'creador': None,
                    'contraseña': None,
                    'robot': None
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
                    'creador': 'leandro',
                    'contraseña': False,
                    'robot': []
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
                    'creador': 'leandro',
                    'contraseña': False,
                    'robot': []
                    }

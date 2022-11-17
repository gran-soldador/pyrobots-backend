from db import *


def test_websocket(client, user1):
    with db_session:
        Match(id=-1, name='my_partida', status='disponible',
              min_players=3, max_players=3, num_games=10, num_rounds=10,
              owner=User[user1])
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
        Match(id=-2, name='my_partida', status='disponible',
              min_players=3, max_players=3, num_games=10, num_rounds=10,
              owner=User[user1])
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
        Match(id=-3, name='my_partida', status='disponible',
              min_players=3, max_players=3, num_games=10, num_rounds=10,
              owner=User[user1])
    with client.websocket_connect("/ws/-3") as websocket:
        data = websocket.send_text('test')
    with client.websocket_connect("/ws/-3") as websocket:
        data = websocket.receive_json()
    assert data == {'event': 'test',
                    'creator': 'leandro',
                    'password': False,
                    'robots': []
                    }

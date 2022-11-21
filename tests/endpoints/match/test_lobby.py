import pytest
from utils.websocket import lobby_manager


def test_websocket(client, match1):
    with client.websocket_connect(f"/ws/{match1}") as websocket:
        data = websocket.receive_json()
    assert data == {'event': 'start',
                    'creator': 'leandro',
                    'password': False,
                    'robots': [{'id': 1,
                                'name': 'RandomRobot',
                                'username': 'leandro'
                                }
                               ]
                    }


def test_websocket_incorrect(client):
    with client.websocket_connect("/ws/2") as websocket:
        data = websocket.receive_json()
    assert data == {'event': 'room not found',
                    'creator': None,
                    'password': None,
                    'robots': None
                    }


@pytest.mark.asyncio
async def test_empty_broadcast(client, match1):
    await lobby_manager.broadcast(match1, 'test')
    with client.websocket_connect(f"/ws/{match1}") as websocket:
        data = websocket.receive_json()
    assert data == {'event': 'test',
                    'creator': 'leandro',
                    'password': False,
                    'robots': [{'id': 1,
                                'name': 'RandomRobot',
                                'username': 'leandro'
                                }
                               ]
                    }


@pytest.mark.asyncio
async def test_non_empty_broadcast(client, match1):
    with client.websocket_connect(f"/ws/{match1}") as websocket:
        await lobby_manager.broadcast(match1, 'test')
        data = websocket.receive_json()
    assert data == {'event': 'test',
                    'creator': 'leandro',
                    'password': False,
                    'robots': [{'id': 1,
                                'name': 'RandomRobot',
                                'username': 'leandro'
                                }
                               ]
                    }

from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from utils.websocket import lobby_manager
from db import *

router = APIRouter()


@router.websocket('/ws/{match_id}')
async def websocket_manager(websocket: WebSocket, match_id: int):
    await lobby_manager.connect(websocket, match_id)
    with db_session:
        partida = Match.get(id=match_id) is not None
    if partida is True:
        msg = lobby_manager.last_msg.get(match_id)
        if msg is not None:
            await lobby_manager.send_msg(match_id, websocket, msg)
        else:
            await lobby_manager.send_msg(match_id, websocket, 'start')
        try:
            while True:
                await websocket.receive_text()
        except WebSocketDisconnect:
            lobby_manager.disconnect(websocket, match_id)
    else:
        lobby_manager.disconnect(websocket, match_id)
        await lobby_manager.send_msg(match_id, websocket, 'error')
        await websocket.close()

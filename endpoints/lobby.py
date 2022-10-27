from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from websocket import lobby_manager
from db import *

router = APIRouter()


@router.websocket('/ws/{partida_id}')
async def websocket_manager(websocket: WebSocket, partida_id: int):
    await lobby_manager.connect(websocket, partida_id)
    msg = lobby_manager.last_msg[partida_id]
    await websocket.send_json(msg)
    try:
        while True:
            data = await websocket.receive_json()
            await lobby_manager.broadcast(partida_id, data)
    except WebSocketDisconnect:
        lobby_manager.disconnect(websocket, partida_id)

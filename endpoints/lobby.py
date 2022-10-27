from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from websocket import lobby_manager
from db import *

router = APIRouter()


@router.websocket('/ws/{partida_id}')
async def websocket_manager(websocket: WebSocket, partida_id: int):
    await lobby_manager.connect(websocket, partida_id)
    try:
        msg = lobby_manager.last_msg[partida_id]
    except Exception:
        with db_session:
            msg = {
                "event": 'created',
                "robots": [{"id": r.robot_id, "nombre": r.nombre}
                           for r in list(Partida[partida_id].participante)]
            }
    await websocket.send_json(msg)
    try:
        while True:
            data = await websocket.receive_json()
            await lobby_manager.broadcast(partida_id, data)
    except WebSocketDisconnect:
        lobby_manager.disconnect(websocket, partida_id)

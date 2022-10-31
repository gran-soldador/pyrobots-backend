from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from websocket import lobby_manager
from db import *

router = APIRouter()


@router.websocket('/ws/{partida_id}')
async def websocket_manager(websocket: WebSocket, partida_id: int):
    await lobby_manager.connect(websocket, partida_id)
    with db_session:
        partida = Partida.get(partida_id=partida_id) is not None
    if partida is True:
        try:
            msg = lobby_manager.last_msg[partida_id]
            await lobby_manager.send_msg(partida_id, websocket, msg)
        except Exception:
            await lobby_manager.send_msg(partida_id, websocket, 'start')
        try:
            while True:
                data = await websocket.receive_text()
                await lobby_manager.broadcast(partida_id, data)
        except WebSocketDisconnect:
            lobby_manager.disconnect(websocket, partida_id)
    else:
        lobby_manager.disconnect(websocket, partida_id)
        await lobby_manager.send_msg(partida_id, websocket, 'error')
        await websocket.close()

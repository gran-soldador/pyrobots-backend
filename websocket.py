from typing import Dict, List
from fastapi import WebSocket
from db import *


class LobbyManager:
    def __init__(self):
        self.room: Dict[int, List[WebSocket]] = {}
        self.last_msg: Dict[int, str] = {}

    async def connect(self, websocket: WebSocket, partida_id: int):
        await websocket.accept()
        if self.room.get(partida_id) is None:
            self.room[partida_id] = []
        self.room[partida_id].append(websocket)

    def disconnect(self, websocket: WebSocket, partida_id: int):
        room = self.room.get(partida_id)
        if room is not None and websocket in room:
            self.room[partida_id].remove(websocket)

    def create_msg(self, partida_id: int, msg: str):
        if msg == 'error':
            return {
                "event": 'room not found',
                "creator": None,
                "password": None,
                "robots": None
            }
        with db_session:
            msg = {
                "event": msg,
                "creator": Partida[partida_id].creador.nombre_usuario,
                "password": Partida[partida_id].password is not None,
                "robots": [{"id": r.robot_id, "name": r.nombre,
                           "username": r.usuario.nombre_usuario} for r in
                           list(Partida[partida_id].participante)]
            }
        return msg

    async def broadcast(self, partida_id: int, msg: str):
        self.last_msg[partida_id] = msg
        room = self.room.get(partida_id)
        if room is not None:
            msg = self.create_msg(partida_id, msg)
            for connection in room:
                await connection.send_json(msg)

    async def send_msg(self, partida_id: int, websocket: WebSocket, msg: str):
        if msg != 'error':
            self.last_msg[partida_id] = msg
        msg = self.create_msg(partida_id, msg)
        await websocket.send_json(msg)


lobby_manager = LobbyManager()

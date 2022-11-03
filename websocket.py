from typing import Dict, List
from fastapi import WebSocket
from db import *


class LobbyManager:
    def __init__(self):
        self.room: Dict[int, List[WebSocket]] = {}
        self.last_msg: Dict[int, str] = {}

    async def connect(self, websocket: WebSocket, partida_id: int):
        await websocket.accept()
        try:
            self.room[partida_id]
        except Exception:
            self.room[partida_id] = []
        self.room[partida_id].append(websocket)

    def disconnect(self, websocket: WebSocket, partida_id: int):
        self.room[partida_id].remove(websocket)

    async def broadcast(self, partida_id: int, msg: str):
        self.last_msg[partida_id] = msg
        with db_session:
            msg = (
                {
                    "event": msg,
                    "creador": Partida[partida_id].creador.nombre_usuario,
                    "contraseña": Partida[partida_id].password is not None,
                    "robot": [{"id": r.robot_id, "nombre": r.nombre,
                               "usuario": r.usuario.nombre_usuario} for r in
                              list(Partida[partida_id].participante)]
                }
            )
        try:
            room = self.room[partida_id]
            for connection in room:
                if room != []:
                    await connection.send_json(msg)
        except Exception:  # pragma: no cover
            pass

    async def send_msg(self, partida_id: int, websocket: WebSocket, msg: str):
        with db_session:
            try:
                self.last_msg[partida_id] = msg
                msg = (
                    {
                        "event": msg,
                        "creador": Partida[partida_id].creador.nombre_usuario,
                        "contraseña": Partida[partida_id].password is not None,
                        "robot": [{"id": r.robot_id, "nombre": r.nombre,
                                   "usuario": r.usuario.nombre_usuario}
                                  for r in
                                  list(Partida[partida_id].participante)]
                    }
                )
            except Exception:
                msg = (
                    {
                        "event": 'room not found',
                        "creador": None,
                        "contraseña": None,
                        "robot": None
                    }
                )
        await websocket.send_json(msg)


lobby_manager = LobbyManager()

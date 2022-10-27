from typing import Dict, List
from fastapi import WebSocket
import json


class LobbyManager:
    def __init__(self):
        self.room: Dict[int, List[WebSocket]] = {}
        self.last_msg: Dict[int, json] = {}

    async def connect(self, websocket: WebSocket, partida_id: int):
        await websocket.accept()
        try:
            self.room[partida_id]
        except Exception:
            self.room[partida_id] = []
        self.room[partida_id].append(websocket)

    def disconnect(self, websocket: WebSocket, partida_id: int):
        self.room[partida_id].remove(websocket)

    async def broadcast(self, partida_id: int, msg: json):
        self.last_msg[partida_id] = msg
        try:
            room = self.room[partida_id]
            if room != []:
                for connection in room:
                    await connection.send_json(msg)
        except Exception:
            pass


lobby_manager = LobbyManager()

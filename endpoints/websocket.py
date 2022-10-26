from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from typing import Dict, List

router = APIRouter()


class ConnectionManager:
	def __init__(self):
		self.room: Dict[int, List[WebSocket]]  = {}

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
		for connection in self.room[partida_id]:
			await connect.send_text(msg)


manager = ConnectionManager()


@router.websocket('/ws/{partida_id}')
async def websocket_manager(websocket: WebSocket, partida_id: int):
	await manager.connect(websocket, partida_id)
	await websocket.send_text("Connection established!")
	try:
		while True:
			data = await websocket.receive_text()
			await manager.broadcast(data)
	except WebSocketDisconnect:
		await manager.disconnect(websocket, partida_id)

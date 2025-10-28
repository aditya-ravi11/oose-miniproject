from typing import Dict, List

from fastapi import WebSocket


class NotificationManager:
    def __init__(self) -> None:
        self.connections: Dict[str, List[WebSocket]] = {}

    async def connect(self, user_id: str, websocket: WebSocket) -> None:
        await websocket.accept()
        self.connections.setdefault(user_id, []).append(websocket)

    def disconnect(self, user_id: str, websocket: WebSocket) -> None:
        conns = self.connections.get(user_id, [])
        if websocket in conns:
            conns.remove(websocket)
        if not conns and user_id in self.connections:
            del self.connections[user_id]

    async def send(self, user_id: str, payload: dict) -> None:
        for ws in self.connections.get(user_id, []):
            await ws.send_json(payload)


manager = NotificationManager()
from typing import Dict, Set
from fastapi import WebSocket


class RoomManager:
    def __init__(self):
        # Структура: {room_id: {username: websocket}}
        self.rooms: Dict[str, Dict[str, WebSocket]] = {}

    async def connect(self, room_id: str, username: str, websocket: WebSocket):
        await websocket.accept()
        if room_id not in self.rooms:
            self.rooms[room_id] = {}
        self.rooms[room_id][username] = websocket
        # Уведомить всех о подключении
        await self.broadcast(
            room_id,
            {
                "type": "system",
                "username": username,
                "text": f"{username} joined the room"
            }
        )

    async def disconnect(self, room_id: str, username: str):
        if room_id in self.rooms:
            if username in self.rooms[room_id]:
                del self.rooms[room_id][username]
            # Уведомить всех об отключении
            await self.broadcast(
                room_id,
                {
                    "type": "system",
                    "username": username,
                    "text": f"{username} left the room"
                }
            )
            # Если комната пуста, удалить её
            if not self.rooms[room_id]:
                del self.rooms[room_id]

    async def broadcast(self, room_id: str, payload: dict):
        if room_id in self.rooms:
            for username, websocket in self.rooms[room_id].items():
                try:
                    await websocket.send_json(payload)
                except Exception:
                    pass

    def get_users(self, room_id: str) -> list:
        if room_id in self.rooms:
            return list(self.rooms[room_id].keys())
        return []

    async def send_to_user(self, room_id: str, username: str, payload: dict):
        if room_id in self.rooms and username in self.rooms[room_id]:
            await self.rooms[room_id][username].send_json(payload)


# Глобальный экземпляр
room_manager = RoomManager()
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException, Query
from typing import Optional
from app.room_manager import room_manager

app = FastAPI(title="WebSocket Chat")


@app.websocket("/ws/rooms/{room_id}")
async def websocket_chat(
    websocket: WebSocket,
    room_id: str,
    username: Optional[str] = Query(None)
):
    # Проверка username
    if not username or not username.strip() or username.strip() == "":
        await websocket.close(code=1008)
        return

    username = username.strip()
    await room_manager.connect(room_id, username, websocket)

    try:
        while True:
            data = await websocket.receive_json()
            message_type = data.get("type")
            text = data.get("text", "")

            if message_type == "message":
                # Проверка длины сообщения
                if len(text) > 300:
                    await room_manager.send_to_user(
                        room_id, username,
                        {"type": "error", "detail": "Message is too long"}
                    )
                else:
                    # Рассылка всем в комнате
                    await room_manager.broadcast(
                        room_id,
                        {
                            "type": "message",
                            "room_id": room_id,
                            "username": username,
                            "text": text
                        }
                    )
    except WebSocketDisconnect:
        await room_manager.disconnect(room_id, username)


@app.get("/rooms/{room_id}/users")
async def get_room_users(room_id: str):
    users = room_manager.get_users(room_id)
    return {"room_id": room_id, "users": users}
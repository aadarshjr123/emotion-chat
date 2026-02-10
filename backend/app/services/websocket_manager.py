import json
from datetime import datetime
from typing import Dict
from fastapi import WebSocket
from sqlalchemy.future import select
from app.models.user import User
from app.core.database import get_db_context
from app.core.redis_client import redis_client


class ConnectionManager:
    def __init__(self):
        self.active_users: Dict[int, WebSocket] = {}

    async def connect(self, websocket: WebSocket, user_id: int | str):
        user_id = int(user_id)
        await websocket.accept()
        self.active_users[user_id] = websocket
        print(
            f"🟢 Connected user {user_id}. Total active users: {len(self.active_users)}"
        )
        await self.broadcast_users()

    def disconnect(self, user_id: int):
        print(f"🔴 Disconnected user {user_id}")
        ws = self.active_users.pop(user_id, None)
        if ws:
            try:
                # Avoid sending close frame if already closed
                if not ws.client_state.name == "DISCONNECTED":
                    import asyncio

                    asyncio.create_task(ws.close())
            except Exception as e:
                print(f"⚠️ Error while closing WS for {user_id}: {e}")

    async def broadcast_users(self):
        user_ids = list(self.active_users.keys())
        if not user_ids:
            return

        async with get_db_context() as db:
            result = await db.execute(
                select(User.id, User.username).where(User.id.in_(user_ids))
            )
            users = [{"id": uid, "username": uname} for uid, uname in result.all()]
            message = json.dumps({"type": "users", "users": users})

        disconnected = []
        for uid, ws in self.active_users.items():
            try:
                await ws.send_text(message)
            except Exception:
                disconnected.append(uid)

        for uid in disconnected:
            self.disconnect(uid)

    # ✅ FIXED: Now inside the class
    async def send_private(self, sender_id: int, receiver_id: int, message: dict):
        """Deliver message to sender + receiver, store if offline."""
        text = json.dumps({"type": "message", **message})

        # --- Always send back to sender
        sender_ws = self.active_users.get(sender_id)
        if sender_ws:
            try:
                await sender_ws.send_text(text)
            except Exception as e:
                print(f"⚠️ Failed to send to sender {sender_id}: {e}")

        # --- Try to send to receiver
        receiver_ws = self.active_users.get(receiver_id)
        if receiver_ws:
            try:
                await receiver_ws.send_text(text)
                print(f"📤 Delivered to receiver {receiver_id}")
            except Exception as e:
                print(f"⚠️ Failed to send to receiver {receiver_id}: {e}")
        else:
            # --- Receiver offline → save notification
            print(f"💾 Storing message for offline user {receiver_id}")
            await redis_client.lpush(
                f"notifications:{receiver_id}",
                json.dumps(
                    {
                        "type": "notification",
                        "sender_id": message["sender_id"],
                        "sender_name": message.get(
                            "sender_name", f"User {message['sender_id']}"
                        ),
                        "text": message["text"],
                        "timestamp": message.get("timestamp")
                        or datetime.utcnow().isoformat(),
                        "emotion": message.get("emotion"),
                    }
                ),
            )
            await redis_client.ltrim(f"notifications:{receiver_id}", 0, 50)


# Global instance
manager = ConnectionManager()

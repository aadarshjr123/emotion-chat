import json
from jose import jwt, JWTError
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Query
from app.services.websocket_manager import manager
from app.core.config import settings
from app.core.database import get_db_context
from app.services.emotion_analyzer import analyze_emotion
from app.core.redis_client import redis_client
from app.models.user import User

router = APIRouter()


@router.websocket("/ws")
async def websocket_endpoint(ws: WebSocket, token: str = Query(...)):
    from app.models.message import Message  # Avoid circular import

    # --- Decode JWT and extract user info ---
    try:
        payload = jwt.decode(
            token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM]
        )
        user_id = int(payload.get("sub"))
        username = payload.get("username", f"User_{user_id}")
        if not user_id:
            print("❌ JWT payload missing 'sub' (user_id)")
            await ws.close(code=1008, reason="Missing user ID in token")
            return
    except JWTError as e:
        print(f"❌ JWT decode error: {e}")
        await ws.close(code=1008, reason="Invalid or expired token")
        return

    print(f"✅ WebSocket connected: user_id={user_id}, username={username}")

    # --- Connect user to WebSocket manager
    await manager.connect(ws, user_id)

    # --- Send missed notifications if any
    missed = await redis_client.lrange(f"notifications:{user_id}", 0, -1)
    if missed:
        print(f"📨 Delivering {len(missed)} missed notifications to user {user_id}")
        for item in missed:
            await ws.send_text(item)
        await redis_client.delete(f"notifications:{user_id}")

    try:
        while True:
            data = await ws.receive_text()
            msg = json.loads(data)
            text = msg.get("text", "")
            receiver_id = msg.get("receiver_id")

            if not receiver_id or not text:
                print("⚠️ Invalid message payload:", msg)
                continue

            # --- Analyze emotion
            emotion = await analyze_emotion(text)

            msg_out = {
                "sender_id": user_id,
                "sender_name": username,
                "receiver_id": receiver_id,
                "text": text,
                "emotion": emotion,
            }

            # --- Save to database
            async with get_db_context() as db:
                new_msg = Message(
                    sender_id=user_id,
                    receiver_id=receiver_id,
                    text=text,
                    emotion=emotion,
                )
                db.add(new_msg)
                await db.commit()

            # --- Send message to both users
            await manager.send_private(user_id, int(receiver_id), msg_out)

    except WebSocketDisconnect:
        print(f"🔌 WebSocket disconnected: user_id={user_id}")
        manager.disconnect(user_id)
        await manager.broadcast_users()

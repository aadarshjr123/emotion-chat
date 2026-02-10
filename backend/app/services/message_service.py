import json
from app.core.redis_client import redis_client
from app.core.config import settings
from app.core.metrics import messages_total
from app.services.websocket_manager import manager
from app.services.emotion_analyzer import analyze_emotion


async def handle_message(msg: dict, sender_id: int):
    """Process and dispatch a chat message (global or private)."""
    text = msg.get("text", "")
    receiver_id = msg.get("receiver_id")

    # 🧠 Emotion detection
    emotion = await analyze_emotion(text)

    msg_out = {
        "sender_id": sender_id,
        "receiver_id": receiver_id,
        "user": msg.get("user", f"user_{sender_id}"),
        "text": text,
        "emotion": emotion,
    }

    # 📊 Metrics
    messages_total.inc()

    # 💾 Store in Redis history (optional per receiver)
    history_key = (
        f"{settings.HISTORY_KEY}:{sender_id}:{receiver_id}"
        if receiver_id
        else settings.HISTORY_KEY
    )

    await redis_client.lpush(history_key, json.dumps(msg_out))
    await redis_client.ltrim(history_key, 0, settings.HISTORY_LIMIT - 1)

    # 💬 Dispatch message
    if receiver_id:
        await manager.send_private(sender_id, receiver_id, msg_out)
    else:
        await manager.broadcast(msg_out)

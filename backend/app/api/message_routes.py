from fastapi import APIRouter, Depends
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.models.message import Message
from app.models.user import User
from app.core.auth import get_current_user

router = APIRouter(prefix="/messages", tags=["messages"])


@router.get("/history/{other_user_id}")
async def get_chat_history(
    other_user_id: int,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    # Get all messages between current and other user
    q = (
        select(Message)
        .where(
            (
                (Message.sender_id == current_user.id)
                & (Message.receiver_id == other_user_id)
            )
            | (
                (Message.sender_id == other_user_id)
                & (Message.receiver_id == current_user.id)
            )
        )
        .order_by(Message.timestamp.asc())
    )
    result = await db.execute(q)
    messages = result.scalars().all()

    return [
        {
            "id": m.id,
            "sender_id": m.sender_id,
            "receiver_id": m.receiver_id,
            "text": m.text,
            "emotion": m.emotion,
            "timestamp": m.timestamp.isoformat(),
        }
        for m in messages
    ]

from fastapi import APIRouter, Depends, Query, UploadFile, File, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import select, or_, union_all, distinct
from app.models.user import User
from app.models.message import Message
from app.core.database import get_db
from app.core.redis_client import redis_client
from app.core.auth import get_current_user
import json
import shutil, uuid
from app.models.user import User
from app.core.auth import get_current_user
from app.core.database import get_db_context
from sqlalchemy import select, func, and_

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/search")
async def search_users(
    q: str = Query(..., min_length=1),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Search users by partial username (cached 10 min, exclude current user)."""
    cache_key = f"user_search:{q.lower()}"

    # ✅ Try Redis cache first
    cached = await redis_client.get(cache_key)
    if cached:
        results = json.loads(cached)
    else:
        # ✅ Include profile_picture in query
        stmt = (
            select(User.id, User.username, User.profile_picture)
            .where(User.username.ilike(f"%{q}%"))
            .where(User.id != current_user.id)
        )
        res = await db.execute(stmt)
        rows = res.all()

        # ✅ Prepend backend URL for each profile picture
        results = [
            {
                "id": uid,
                "username": uname,
                "profile_picture": (
                    f"http://localhost:8000/{pic.lstrip('/')}" if pic else None
                ),
            }
            for uid, uname, pic in rows
        ]

        # ✅ Cache for 10 min
        await redis_client.set(cache_key, json.dumps(results), ex=600)

    return {"results": results}


@router.get("/recent")
async def get_recent_chat_users(
    current_user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    cache_key = f"recent_users:{current_user.id}"
    cached = await redis_client.get(cache_key)
    if cached:
        print("✅ Cache hit for recent users")
        return json.loads(cached)

    # ✅ Combine all users this user has talked to (sent or received)
    sent_to = select(Message.receiver_id).where(Message.sender_id == current_user.id)
    received_from = select(Message.sender_id).where(
        Message.receiver_id == current_user.id
    )

    # ✅ Combine unique IDs
    combined = sent_to.union(received_from).subquery()

    # ✅ Fetch User details
    result = await db.execute(
        select(User.id, User.username, User.profile_picture).where(
            User.id.in_(select(combined.c.receiver_id))
        )
    )
    rows = result.all()

    users = [
        {
            "id": row.id,
            "username": row.username,
            "profile_picture": row.profile_picture,
        }
        for row in rows
    ]

    # ✅ Cache for 10 mins
    await redis_client.setex(cache_key, 600, json.dumps(users))
    return users


@router.post("/profile-picture")
async def upload_profile_picture(
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    filename = f"{uuid.uuid4()}.jpg"
    filepath = f"static/uploads/{filename}"

    # Save file
    with open(filepath, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # ✅ Update and persist
    current_user.profile_picture = filepath
    db.add(current_user)  # mark object as updated
    await db.commit()  # <-- ✅ async commit
    await db.refresh(current_user)  # reload from DB

    return {"url": f"/{filepath}"}


@router.get("/emotion-stats")
async def emotion_stats(
    current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)
):
    # Count happy messages
    happy_stmt = (
        select(func.count())
        .select_from(Message)
        .where(
            and_(
                Message.sender_id == current_user.id,
                func.lower(Message.emotion) == "positive",
            )
        )
    )
    happy_result = await db.execute(happy_stmt)
    happy_count = happy_result.scalar()

    # Count sad messages
    sad_stmt = (
        select(func.count())
        .select_from(Message)
        .where(
            and_(
                Message.sender_id == current_user.id,
                func.lower(Message.emotion) == "negative",
            )
        )
    )
    sad_result = await db.execute(sad_stmt)
    sad_count = sad_result.scalar()

    return {"happy": happy_count, "sad": sad_count}

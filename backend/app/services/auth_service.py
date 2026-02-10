from sqlalchemy.future import select
from fastapi import HTTPException, status
from app.models.user import User
from app.core.security import hash_password, verify_password, create_access_token
from app.core.database import AsyncSession


async def signup_user(db: AsyncSession, username: str, password: str):
    existing = await db.scalar(select(User).where(User.username == username))
    if existing:
        raise HTTPException(status_code=400, detail="Username already exists")

    user = User(username=username, password_hash=hash_password(password))
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user


async def login_user(db: AsyncSession, username: str, password: str):
    user = await db.scalar(select(User).where(User.username == username))
    if not user or not verify_password(password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
        )

    print("✅ profile_picture", user.profile_picture)
    token = create_access_token(
        {
            "sub": str(user.id),
            "username": user.username,
            "profile_picture": user.profile_picture,
        }
    )
    return {"access_token": token, "token_type": "bearer"}

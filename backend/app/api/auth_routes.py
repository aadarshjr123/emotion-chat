from fastapi import APIRouter, Depends
from app.core.database import get_db
from app.schemas.user import UserCreate, UserLogin
from app.services.auth_service import signup_user, login_user
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/signup")
async def signup(data: UserCreate, db: AsyncSession = Depends(get_db)):
    user = await signup_user(db, data.username, data.password)
    return {"id": user.id, "username": user.username}


@router.post("/login")
async def login(data: UserLogin, db: AsyncSession = Depends(get_db)):
    return await login_user(db, data.username, data.password)

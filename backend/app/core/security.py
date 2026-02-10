from datetime import datetime, timedelta

from fastapi import HTTPException, status
from jose import jwt
from passlib.context import CryptContext

from app.core.config import settings

# bcrypt_sha256 hashes the password with SHA-256 first — avoids 72-byte limit
_pwd_context = CryptContext(
    schemes=["bcrypt_sha256"], bcrypt_sha256__default_rounds=12, deprecated="auto"
)


def validate_password_strength(password: str):
    """Ensure password meets minimal security rules."""
    if len(password) < 8:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password too short (min 8 characters required).",
        )
    if len(password.encode("utf-8")) > 256:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password too long (max 256 bytes allowed).",
        )


def hash_password(password: str) -> str:
    """Hash a plaintext password after validating its strength."""
    validate_password_strength(password)
    return _pwd_context.hash(password)


def verify_password(plain: str, hashed: str) -> bool:
    """Verify a plaintext password against a stored hash."""
    return _pwd_context.verify(plain, hashed)


def create_access_token(data: dict, expires_minutes: int = 60):
    """Generate a signed JWT access token."""
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=expires_minutes)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)

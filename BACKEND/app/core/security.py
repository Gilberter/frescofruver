
from datetime import UTC, datetime, timedelta
from typing import Any

import bcrypt
from fastapi.security import (
    OAuth2PasswordBearer,
)
from jose import JWTError, jwt
from pydantic import BaseModel

from app.core.config import get_settings

settings = get_settings()


class Hasher:
    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        try:
            # bcrypt needs bytes, max 72 bytes
            return bcrypt.checkpw(
                plain_password.encode("utf-8")[:72], hashed_password.encode("utf-8")
            )
        except Exception:
            return False

    @staticmethod
    def get_password_hash(password: str) -> str:
        # bcrypt needs bytes, returns bytes, max 72 bytes
        password_bytes = password.encode("utf-8")[:72]
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password_bytes, salt)
        return hashed.decode("utf-8")


class TokenService:
    oauth2_scheme = OAuth2PasswordBearer(
        tokenUrl="token",
        scopes={
            "me": "Read information about the current user.",
            "items": "Read items.",
        },
    )

    @staticmethod
    def create_access_token(
        subject: str | Any,
        extra_claims: dict | None = None,
    ) -> str:
        now = datetime.now(UTC)

        expire = now + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

        to_encode = {
            "sub": str(subject),
            "exp": expire,
            "iat": now,
            "nbf": now,
            "type": "access"
        }
    
        return jwt.encode(
            to_encode,
            settings.SECRET_KEY,
            algorithm=settings.ALGORITHM,
        )

    @staticmethod
    def create_refresh_token(user_id: str | Any) -> str:
        now = datetime.now(UTC)

        expire = now + (timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS))

        to_encode = {"sub": str(user_id), "type": "refresh", "exp": expire}

        return jwt.encode(
            to_encode,
            settings.SECRET_KEY,
            algorithm=settings.ALGORITHM,
        )

    @staticmethod
    def create_verification_token(user_id: str | Any) -> str:
        """Create a token for email verification (24h)."""
        now = datetime.now(UTC)
        expire = now + timedelta(hours=24)
        to_encode = {"sub": str(user_id), "type": "verification", "exp": expire}
        return jwt.encode(
            to_encode,
            settings.SECRET_KEY,
            algorithm=settings.ALGORITHM,
        )

    @staticmethod
    def verify_token(token: str) -> dict:
        try:
            return jwt.decode(
                token,
                settings.SECRET_KEY,
                algorithms=[settings.ALGORITHM],
            )
        except JWTError:
            raise ValueError("Invalid or expired token") from None

    @staticmethod
    def verify_access_token(token: str) -> dict:
        payload = TokenService.verify_token(token)
        if payload.get("type") != "access":
            raise ValueError("Invalid Token type")

        return payload

    @staticmethod
    def get_token_subject(token: str) -> str | None:
        payload = TokenService.verify_token(token)
        return payload.get("sub")


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class RefreshRequest(BaseModel):
    refresh_token: str


class TokenPayload(BaseModel):
    sub: str
    exp: int
    iat: int
    nbf: int
    type: str
    role: str | None = None
    scopes: list[str] = []
from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import decode_access_token
from app.models.usuario import Usuario, RolUsuario

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

# ── Type aliases ─────────────────────────────────────────────────────────────

DBSession = Annotated[Session, Depends(get_db)]
TokenDep = Annotated[str, Depends(oauth2_scheme)]


# ── Auth dependencies ─────────────────────────────────────────────────────────

def get_current_user(token: TokenDep, db: DBSession) -> Usuario:
    """Decode the JWT and return the matching active user."""
    credentials_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Credenciales inválidas",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = decode_access_token(token)
        user_id: str | None = payload.get("sub")
        if user_id is None:
            raise credentials_exc
    except JWTError:
        raise credentials_exc

    user = db.get(Usuario, int(user_id))
    if user is None or user.estado == "inactivo":
        raise credentials_exc
    return user


CurrentUser = Annotated[Usuario, Depends(get_current_user)]


# ── Role guards ───────────────────────────────────────────────────────────────

def require_roles(*roles: RolUsuario):
    """Dependency factory that restricts access to the given roles."""

    def _check(current_user: CurrentUser) -> Usuario:
        if current_user.rol not in roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No tienes permiso para acceder a este módulo",
            )
        return current_user

    return Depends(_check)


# Convenience shorthands
AdminOrOwner = require_roles(RolUsuario.administrador, RolUsuario.dueno)
AnyRole = require_roles(
    RolUsuario.vendedor, RolUsuario.administrador, RolUsuario.dueno
)

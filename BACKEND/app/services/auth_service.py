from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.crud import usuario as crud_usuario
from app.crud import auditoria as crud_auditoria
from app.core.security import verify_password, create_access_token
from app.schemas.usuario import TokenOut


def login(db: Session, username: str, password: str) -> TokenOut:
    user = crud_usuario.get_by_username(db, username)

    if not user or not verify_password(password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales inválidas",
        )

    if user.estado == "inactivo":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Cuenta desactivada. Contacte al administrador.",
        )

    token = create_access_token(
        subject=user.id,
        extra_claims={"rol": user.rol.value, "username": user.username},
    )

    crud_auditoria.registrar(
        db,
        accion="inicio_sesion",
        descripcion=f"Usuario '{username}' inició sesión",
        usuario_id=user.id,
    )

    return TokenOut(access_token=token, rol=user.rol, username=user.username)

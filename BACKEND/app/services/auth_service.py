from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime, timedelta, timezone

from app.crud import usuario as crud_usuario
from app.crud import auditoria as crud_auditoria
from app.models.usuario import RolUsuario
from app.core.security import verify_password, create_access_token
from app.core.user_estado import estado_indica_inactivo
from app.schemas.usuario import TokenOut, UsuarioCreate, UsuarioOut

MAX_FAILED_ATTEMPTS = 5
LOCKOUT_MINUTES = 15
_failed_login_state: dict[str, dict[str, int | datetime | None]] = {}


def _username_key(username: str) -> str:
    return username.strip().lower()


def _raise_temporary_lock(username: str, lock_seconds: int) -> None:
    raise HTTPException(
        status_code=status.HTTP_429_TOO_MANY_REQUESTS,
        detail={
            "message": (
                f"El usuario '{username}' está bloqueado temporalmente por demasiados "
                f"intentos fallidos. Intenta nuevamente en {LOCKOUT_MINUTES} minutos."
            ),
            "lock_seconds": lock_seconds,
        },
    )


def login(db: Session, username: str, password: str) -> TokenOut:
    now = datetime.now(timezone.utc)
    key = _username_key(username)
    state = _failed_login_state.get(key)
    if state and isinstance(state.get("locked_until"), datetime):
        locked_until = state["locked_until"]
        if locked_until and locked_until > now:
            remaining = int((locked_until - now).total_seconds())
            _raise_temporary_lock(username, max(remaining, 1))
        _failed_login_state.pop(key, None)

    user = crud_usuario.get_by_username(db, username)

    if not user or not verify_password(password, user.password):
        attempts = 1
        if state and isinstance(state.get("attempts"), int):
            attempts = int(state["attempts"]) + 1

        if attempts >= MAX_FAILED_ATTEMPTS:
            locked_until = now + timedelta(minutes=LOCKOUT_MINUTES)
            _failed_login_state[key] = {"attempts": 0, "locked_until": locked_until}
            _raise_temporary_lock(username, LOCKOUT_MINUTES * 60)

        _failed_login_state[key] = {"attempts": attempts, "locked_until": None}
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales inválidas",
        )

    _failed_login_state.pop(key, None)

    if estado_indica_inactivo(user.estado):
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


def register(
    db: Session,
    nombre_completo: str,
    no_documento: str,
    username: str,
    password: str,
    telefono: str,
    correo: str,
) -> UsuarioOut:
    if crud_usuario.get_by_username(db, username):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="El nombre de usuario ya existe",
        )

    if crud_usuario.get_by_documento(db, no_documento):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="El número de documento ya está registrado",
        )

    new_user = crud_usuario.create(
        db,
        UsuarioCreate(
            nombre_completo=nombre_completo,
            no_documento=no_documento,
            username=username,
            password=password,
            telefono=telefono,
            correo=correo,
            rol=RolUsuario.vendedor,
            estado="Activo",
        ),
    )
    return UsuarioOut.model_validate(new_user)

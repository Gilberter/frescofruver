from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.crud import usuario as crud_usuario
from app.crud import auditoria as crud_auditoria
from app.models.usuario import Usuario
from app.schemas.usuario import UsuarioCreate, UsuarioUpdate


def crear_usuario(db: Session, data: UsuarioCreate, actor_id: int) -> Usuario:
    if crud_usuario.get_by_username(db, data.username):
        raise HTTPException(status.HTTP_409_CONFLICT, detail="Usuario ya existe")

    if crud_usuario.get_by_documento(db, data.no_documento):
        raise HTTPException(status.HTTP_409_CONFLICT, detail="Número de documento ya registrado")

    user = crud_usuario.create(db, data)
    crud_auditoria.registrar(
        db,
        accion="crear_usuario",
        descripcion=f"Usuario '{data.username}' creado con rol {data.rol}",
        usuario_id=actor_id,
    )
    return user


def actualizar_usuario(db: Session, user_id: int, data: UsuarioUpdate, actor_id: int) -> Usuario:
    user = crud_usuario.get_by_id(db, user_id)
    if not user:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado")

    updated = crud_usuario.update(db, user, data)
    crud_auditoria.registrar(
        db,
        accion="actualizar_usuario",
        descripcion=f"Usuario id={user_id} actualizado",
        usuario_id=actor_id,
    )
    return updated


def desactivar_usuario(db: Session, user_id: int, actor_id: int) -> Usuario:
    user = crud_usuario.get_by_id(db, user_id)
    if not user:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado")

    updated = crud_usuario.deactivate(db, user)
    crud_auditoria.registrar(
        db,
        accion="desactivar_usuario",
        descripcion=f"Usuario id={user_id} desactivado",
        usuario_id=actor_id,
    )
    return updated

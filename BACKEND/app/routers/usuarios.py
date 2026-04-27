from fastapi import APIRouter, HTTPException, status

from app.core.deps import DBSession, CurrentUser, AdminOrOwner
from app.crud import usuario as crud_usuario
from app.schemas.usuario import UsuarioCreate, UsuarioUpdate, UsuarioOut
from app.services import usuario_service

router = APIRouter(prefix="/usuarios", tags=["Usuarios"])


@router.get("/", response_model=list[UsuarioOut], dependencies=[AdminOrOwner])
def listar_usuarios(db: DBSession):
    """Listar todos los usuarios (solo Admin/Dueño)."""
    return crud_usuario.list_all(db)


@router.post("/", response_model=UsuarioOut, status_code=status.HTTP_201_CREATED, dependencies=[AdminOrOwner])
def crear_usuario(data: UsuarioCreate, db: DBSession, current_user: CurrentUser):
    """Registrar un nuevo usuario (solo Admin/Dueño)."""
    return usuario_service.crear_usuario(db, data, current_user.id)


@router.get("/me", response_model=UsuarioOut)
def perfil_propio(current_user: CurrentUser):
    """Obtener datos del usuario autenticado."""
    return current_user


@router.get("/{user_id}", response_model=UsuarioOut, dependencies=[AdminOrOwner])
def obtener_usuario(user_id: int, db: DBSession):
    user = crud_usuario.get_by_id(db, user_id)
    if not user:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado")
    return user


@router.patch("/{user_id}", response_model=UsuarioOut, dependencies=[AdminOrOwner])
def actualizar_usuario(user_id: int, data: UsuarioUpdate, db: DBSession, current_user: CurrentUser):
    return usuario_service.actualizar_usuario(db, user_id, data, current_user.id)


@router.delete("/{user_id}/desactivar", response_model=UsuarioOut, dependencies=[AdminOrOwner])
def desactivar_usuario(user_id: int, db: DBSession, current_user: CurrentUser):
    """Desactivar cuenta sin eliminar historial (RF-01.4)."""
    return usuario_service.desactivar_usuario(db, user_id, current_user.id)

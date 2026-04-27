from fastapi import APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field

from app.core.database import get_db
from app.schemas.usuario import TokenOut, UsuarioOut
from app.services import auth_service

router = APIRouter(prefix="/auth", tags=["Autenticación"])


class RegisterInput(BaseModel):
    nombre_completo: str = Field(..., max_length=150)
    no_documento: str = Field(..., max_length=50)
    username: str = Field(..., max_length=60)
    password: str = Field(..., min_length=6)
    telefono: str = Field(..., max_length=20)
    correo: str = Field(..., max_length=100)

    model_config = {"extra": "forbid"}


@router.post("/login", response_model=TokenOut)
def login(
    form: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    """Autenticar usuario y obtener JWT."""
    return auth_service.login(db, form.username, form.password)


@router.post("/register", response_model=UsuarioOut, status_code=201)
def register(payload: RegisterInput, db: Session = Depends(get_db)):
    """Registrar un nuevo usuario (rol por defecto: vendedor)."""
    return auth_service.register(
        db,
        nombre_completo=payload.nombre_completo,
        no_documento=payload.no_documento,
        username=payload.username,
        password=payload.password,
        telefono=payload.telefono,
        correo=payload.correo,
    )

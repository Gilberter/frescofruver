from fastapi import APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.usuario import TokenOut
from app.services import auth_service

router = APIRouter(prefix="/auth", tags=["Autenticación"])


@router.post("/login", response_model=TokenOut)
def login(
    form: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    """Autenticar usuario y obtener JWT."""
    return auth_service.login(db, form.username, form.password)

from sqlalchemy.orm import Session

from app.models.usuario import Usuario
from app.schemas.usuario import UsuarioCreate, UsuarioUpdate
from app.core.security import hash_password


def get_by_id(db: Session, user_id: int) -> Usuario | None:
    return db.get(Usuario, user_id)


def get_by_username(db: Session, username: str) -> Usuario | None:
    return db.query(Usuario).filter(Usuario.username == username).first()


def get_by_documento(db: Session, no_documento: str) -> Usuario | None:
    return db.query(Usuario).filter(Usuario.no_documento == no_documento).first()


def list_all(db: Session) -> list[Usuario]:
    return db.query(Usuario).all()


def create(db: Session, data: UsuarioCreate) -> Usuario:
    user = Usuario(
        nombre_completo=data.nombre_completo,
        no_documento=data.no_documento,
        username=data.username,
        password=hash_password(data.password),
        rol=data.rol,
        estado=data.estado,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def update(db: Session, user: Usuario, data: UsuarioUpdate) -> Usuario:
    for field, value in data.model_dump(exclude_none=True).items():
        setattr(user, field, value)
    db.commit()
    db.refresh(user)
    return user


def deactivate(db: Session, user: Usuario) -> Usuario:
    user.estado = "inactivo"
    db.commit()
    db.refresh(user)
    return user

"""Seed the database with initial data (roles, admin user, sample products)."""
from sqlalchemy.orm import Session

from app.core.security import Hasher
from app.models.usuario import Usuario, RolUsuario


def seed_usuarios(db: Session) -> None:
    """Create a default admin user if none exists."""
    exists = db.query(Usuario).filter_by(username="admin").first()
    if exists:
        return

    admin = Usuario(
        nombre_completo="Administrador",
        no_documento="0000000000",
        username="admin",
        password=Hasher.get_password_hash("admin123"),
        rol=RolUsuario.administrador,
        estado="Activo",
    )
    db.add(admin)
    db.commit()
    print("✅  Usuario admin creado  (user: admin / pass: admin123)")


def run_all_seeds(db: Session) -> None:
    seed_usuarios(db)
    # Add more seed functions here as modules are built

from sqlalchemy.orm import Session

from app.models.cliente import Cliente
from app.schemas.cliente import ClienteCreate, ClienteUpdate


def get_by_id(db: Session, cliente_id: int) -> Cliente | None:
    return db.get(Cliente, cliente_id)


def get_by_documento(db: Session, no_documento: str) -> Cliente | None:
    return db.query(Cliente).filter(Cliente.no_documento == no_documento).first()


def list_all(db: Session) -> list[Cliente]:
    return db.query(Cliente).all()


def create(db: Session, data: ClienteCreate) -> Cliente:
    cliente = Cliente(**data.model_dump())
    db.add(cliente)
    db.commit()
    db.refresh(cliente)
    return cliente


def update(db: Session, cliente: Cliente, data: ClienteUpdate) -> Cliente:
    for field, value in data.model_dump(exclude_none=True).items():
        setattr(cliente, field, value)
    db.commit()
    db.refresh(cliente)
    return cliente

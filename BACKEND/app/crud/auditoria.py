from sqlalchemy.orm import Session

from app.models.auditoria import Auditoria


def registrar(
    db: Session,
    accion: str,
    descripcion: str | None = None,
    usuario_id: int | None = None,
) -> Auditoria:
    entry = Auditoria(usuario_id=usuario_id, accion=accion, descripcion=descripcion)
    db.add(entry)
    db.commit()
    db.refresh(entry)
    return entry


def list_all(db: Session, limit: int = 200) -> list[Auditoria]:
    return (
        db.query(Auditoria)
        .order_by(Auditoria.fecha_auditoria.desc())
        .limit(limit)
        .all()
    )

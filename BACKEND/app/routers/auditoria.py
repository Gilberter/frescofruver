from fastapi import APIRouter, Query

from app.core.deps import DBSession, AdminOrOwner
from app.crud import auditoria as crud_auditoria
from app.schemas.auditoria import AuditoriaOut

router = APIRouter(prefix="/auditoria", tags=["Auditoría"])


@router.get("/", response_model=list[AuditoriaOut], dependencies=[AdminOrOwner])
def log_auditoria(db: DBSession, limit: int = Query(default=100, le=500)):
    """Log de auditoría (RF-08): inicios de sesión, cambios, cancelaciones."""
    return crud_auditoria.list_all(db, limit)

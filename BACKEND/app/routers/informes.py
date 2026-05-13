# app/routers/dashboard.py

from fastapi import APIRouter

from app.core.deps import DBSession, AnyRole
from app.services import informe_service
from app.schemas.informe import DashboardResponse

router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"]
)


@router.get(
    "/ultimo-mes",
    response_model=DashboardResponse,
    dependencies=[AnyRole]
)
def dashboard_ultimo_mes(db: DBSession):

    return informe_service.obtener_dashboard_ultimo_mes(db)
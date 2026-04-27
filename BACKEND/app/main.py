from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import compras
from app.core.config import settings
from app.core.database import validate_database_connection
from app.routers import (
    auth,
    usuarios,
    clientes,
    productos,
    ventas,
    proveedores,
    inventario,
    auditoria,
    informes
)

# ── App ───────────────────────────────────────────────────────────────────────

app = FastAPI(
    title=settings.APP_TITLE,
    version=settings.APP_VERSION,
    docs_url="/docs",
    redoc_url="/redoc",
)

# ── CORS ──────────────────────────────────────────────────────────────────────
# Adjust origins for production
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Routers ───────────────────────────────────────────────────────────────────
API_PREFIX = "/api/v1"

app.include_router(auth.router,        prefix=API_PREFIX)
app.include_router(usuarios.router,    prefix=API_PREFIX)
app.include_router(clientes.router,    prefix=API_PREFIX)
app.include_router(productos.router,   prefix=API_PREFIX)
app.include_router(ventas.router,      prefix=API_PREFIX)
app.include_router(proveedores.router, prefix=API_PREFIX)
app.include_router(compras.router,     prefix=API_PREFIX)
app.include_router(inventario.router,  prefix=API_PREFIX)
app.include_router(auditoria.router,   prefix=API_PREFIX)
app.include_router(informes.router, prefix=API_PREFIX)


@app.on_event("startup")
def startup_check_database():
    validate_database_connection()


# ── Root route ────────────────────────────────────────────────────────────────
@app.get("/", tags=["Root"])
def root():
    return {"message": "FrescoExpress API activa"}


# ── Health check ──────────────────────────────────────────────────────────────
@app.get("/health", tags=["Health"])
def health():
    return {"status": "ok", "version": settings.APP_VERSION}

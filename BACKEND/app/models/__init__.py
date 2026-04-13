# Import all models so SQLAlchemy metadata is populated
# and Alembic can auto-generate migrations.
from app.models.usuario import Usuario, RolUsuario          # noqa: F401
from app.models.cliente import Cliente                      # noqa: F401
from app.models.producto import Producto                    # noqa: F401
from app.models.venta import Venta, DetalleVenta            # noqa: F401
from app.models.proveedor import Proveedor, OrdenCompra, DetalleCompra  # noqa: F401
from app.models.inventario import MovimientoInventario      # noqa: F401
from app.models.auditoria import Auditoria                  # noqa: F401

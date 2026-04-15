# Import all models so SQLAlchemy metadata is populated
# and Alembic can auto-generate migrations.
from app.models.usuario import Usuario, RolUsuario         
from app.models.cliente import Cliente                      
from app.models.producto import Producto                  
from app.models.venta import Venta, DetalleVenta           
from app.models.proveedor import Proveedor, OrdenCompra, DetalleCompra  
from app.models.inventario import MovimientoInventario   
from app.models.auditoria import Auditoria                
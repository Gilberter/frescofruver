import React, { useState, useEffect } from 'react';
import { products, auth } from '../api';
import Modal from '../components/Modal';

const Inventory = () => {
  const [productList, setProductList] = useState([]);
  const [filterCategory, setFilterCategory] = useState('Todas');
  const [loading, setLoading] = useState(true);
  
  const [isCreateModalOpen, setIsCreateModalOpen] = useState(false);
  const [isAdjustModalOpen, setIsAdjustModalOpen] = useState(false);
  const [selectedProduct, setSelectedProduct] = useState(null);
  const currentUser = auth.getCurrentUser();
  const isAdminOrOwner = currentUser?.rol === 'Administrador' || currentUser?.rol === 'Dueño';

  const [formData, setFormData] = useState({
    nombre: '',
    categoria: 'fruta',
    unidad_medida: 'kg',
    precio_compra: '',
    precio_venta: '',
    stock_actual: '',
  });

  // const [adjustData, setAdjustData] = useState({
  //   cantidad_ajuste: '',
  //   motivo: ''
  // });

  const [movementData, setMovementData] = useState({
    tipo_movimiento: 'Entrada',
    cantidad: '',
    motivo: 'No Motivo',
    observacion: 'No Observacion'
  });

  useEffect(() => {
    loadProducts();
  }, []);

  const loadProducts = async () => {
    setLoading(true);
    try {
      const data = await products.getProducts();
      setProductList(data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleCreate = async (e) => {
    e.preventDefault();
    
    // Frontend validation to prevent backend error
    if (parseFloat(formData.precio_venta) <= parseFloat(formData.precio_compra)) {
      alert('Error: El precio de venta debe ser mayor al precio de compra.');
      return;
    }

    try {
      const payload = {
        ...formData,
        precio_compra: parseFloat(formData.precio_compra),
        precio_venta: parseFloat(formData.precio_venta),
        stock_actual: parseInt(formData.stock_actual) || 0,
      };

      await products.createProduct(payload);
      setIsCreateModalOpen(false);
      setFormData({
        nombre: '', categoria: 'fruta', unidad_medida: 'kg',
        precio_compra: '', precio_venta: '', stock_actual: '',
      });
      loadProducts();
    } catch (err) {
      alert('Error al crear producto: ' + (err.response?.data?.detail?.[0]?.msg || err.response?.data?.detail || err.message));
    }
  };

  // const handleAdjust = async (e) => {
  //   e.preventDefault();
  //   try {
  //     // Correct field name for openapi.json: 'cantidad' instead of 'cantidad_ajuste'
  //     await products.dataMovement(selectedProduct.id, {
  //       tipo: movementData.tipo_movimiento,
  //       cantidad: parseInt(movementData.cantidad),
  //       motivo: movementData.motivo,
  //       observacion: movementData.observacion
  //     });
  //     setIsAdjustModalOpen(false);
  //     setMovementData({ cantidad: '', motivo: '' });
  //     loadProducts();
  //   } catch (err) {
  //     alert('Error al ajustar inventario: ' + (err.response?.data?.detail?.[0]?.msg || err.response?.data?.detail || err.message));
  //   }
  // };

  const handleAdjust = async (e) => {
    e.preventDefault();

    try {

      const payload = {
        tipo: movementData.tipo,
        cantidad: parseInt(movementData.cantidad),
        motivo: movementData.motivo,
        observacion: movementData.observacion
      };

      console.log("MOVEMENT PAYLOAD:");
      console.log(payload);

      await products.dataMovement(selectedProduct.id, payload);

      setIsAdjustModalOpen(false);

      setMovementData({
        tipo: 'Entrada',
        cantidad: '',
        motivo: 'No Motivo',
        observacion: 'No Observacion'
      });

      loadProducts();

    } catch (err) {

      console.error(err.response?.data);

      alert(
        'Error al ajustar inventario: ' +
        (
          err.response?.data?.detail?.[0]?.msg ||
          err.response?.data?.detail ||
          err.message
        )
      );
    }
  };

  const filteredProducts = productList.filter(p => 
    filterCategory === 'Todas' || p.categoria.toLowerCase() === filterCategory.toLowerCase()
  );

  return (
    <div className="space-y-10">
      <div className="flex justify-between items-end">
        <div>
          <h2 className="text-4xl font-extrabold text-[#1a1c23] mb-2">Inventario en Tiempo Real</h2>
          <p className="text-lg text-gray-500">Gestione el stock, precios y categorías de sus productos.</p>
        </div>
        <div className="flex gap-4">
          <select 
            value={filterCategory}
            onChange={(e) => setFilterCategory(e.target.value)}
            className="bg-white px-6 py-4 rounded-2xl shadow-sm border border-gray-100 font-bold text-gray-600 outline-none focus:ring-2 focus:ring-[#4263eb]"
          >
            <option>Todas</option>
            <option>Fruta</option>
            <option>Verdura</option>
          </select>
          {isAdminOrOwner && (
            <button 
              onClick={() => setIsCreateModalOpen(true)}
              className="bg-[#4263eb] text-white px-8 py-4 rounded-2xl font-bold shadow-xl hover:bg-[#364fc7] transition-all transform hover:scale-105 active:scale-95"
            >
              + Nuevo Producto
            </button>
          )}
        </div>
      </div>

      <div className="bg-white p-10 rounded-[32px] shadow-sm border border-gray-100">
        <div className="overflow-hidden rounded-xl">
          <table className="w-full text-left">
            <thead className="bg-[#f8f9fa] border-b border-gray-100">
              <tr>
                <th className="px-6 py-5 font-bold text-[#343a40]">Nombre</th>
                <th className="px-6 py-5 font-bold text-[#343a40]">Categoría</th>
                <th className="px-6 py-5 font-bold text-[#343a40]">Stock Actual</th>
                <th className="px-6 py-5 font-bold text-[#343a40]">Precio Venta</th>
                <th className="px-6 py-5 font-bold text-[#343a40]">Estado</th>
                <th className="px-6 py-5 font-bold text-[#343a40]">Acciones</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-100">
              {loading ? (
                <tr><td colSpan="6" className="px-6 py-20 text-center text-gray-400 font-medium">Sincronizando inventario...</td></tr>
              ) : filteredProducts.map((product) => (
                <tr key={product.id} className="hover:bg-gray-50 transition-colors">
                  <td className="px-6 py-4 font-bold text-[#1a1c23]">{product.nombre}</td>
                  <td className="px-6 py-4"><span className="bg-blue-50 text-blue-600 px-4 py-1.5 rounded-full text-xs font-black uppercase tracking-wider">{product.categoria}</span></td>
                  <td className="px-6 py-4">
                    <span className={`font-black text-lg ${product.bajo_stock ? 'text-red-500' : 'text-green-600'}`}>
                      {product.stock_actual} <span className="text-xs uppercase opacity-60">{product.unidad_medida}</span>
                    </span>
                    {product.stock_actual <= product.stock_minimo && (
                      <div className="text-[10px] font-black text-red-500 uppercase tracking-tighter mt-1">Stock Crítico</div>
                    )}
                  </td>
                  <td className="px-6 py-4 font-black text-[#1a1c23]">${product.precio_venta.toLocaleString()}</td>
                  <td className="px-6 py-4">
                    <div className="flex items-center">
                      <div className={`w-2 h-2 rounded-full mr-2 ${product.estado === 'Activo' ? 'bg-green-500' : 'bg-red-500'}`}></div>
                      <span className="text-sm font-bold capitalize text-gray-600">{product.estado}</span>
                    </div>
                  </td>
                  <td className="px-6 py-4">
                    {isAdminOrOwner && (
                      <button 
                        onClick={() => { setSelectedProduct(product); setIsAdjustModalOpen(true); }}
                        className="bg-[#f1f3f5] text-[#4263eb] px-4 py-2 rounded-lg font-black text-xs uppercase tracking-wider hover:bg-[#4263eb] hover:text-white transition-all shadow-sm"
                      >
                        Ajustar
                      </button>
                    )}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* Create Product Modal */}
      <Modal isOpen={isCreateModalOpen} onClose={() => setIsCreateModalOpen(false)} title="Registrar Nuevo Producto">
        <form onSubmit={handleCreate} className="space-y-6">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div className="space-y-2 md:col-span-2">
              <label className="text-[13px] font-black text-gray-400 uppercase tracking-widest">Nombre del Producto</label>
              <input 
                type="text" required
                value={formData.nombre}
                onChange={(e) => setFormData({...formData, nombre: e.target.value})}
                className="w-full px-6 py-4 rounded-xl border border-gray-100 bg-[#f8f9fa] outline-none focus:ring-2 focus:ring-[#4263eb]"
                placeholder="Ej. Tomate Chonto"
              />
            </div>
            <div className="space-y-2">
              <label className="text-[13px] font-black text-gray-400 uppercase tracking-widest">Categoría</label>
              <select 
                value={formData.categoria}
                onChange={(e) => setFormData({...formData, categoria: e.target.value})}
                className="w-full px-6 py-4 rounded-xl border border-gray-100 bg-[#f8f9fa] outline-none focus:ring-2 focus:ring-[#4263eb] font-bold"
              >
                <option value="fruta">Fruta</option>
                <option value="verdura">Verdura</option>
              </select>
            </div>
            <div className="space-y-2">
              <label className="text-[13px] font-black text-gray-400 uppercase tracking-widest">Unidad Medida</label>
              <select 
                value={formData.unidad_medida}
                onChange={(e) => setFormData({...formData, unidad_medida: e.target.value})}
                className="w-full px-6 py-4 rounded-xl border border-gray-100 bg-[#f8f9fa] outline-none focus:ring-2 focus:ring-[#4263eb] font-bold"
              >
                <option value="kg">Kilogramo (kg)</option>
                <option value="libra">Libra</option>
                <option value="unidad">Unidad</option>
              </select>
            </div>
            <div className="space-y-2">
              <label className="text-[13px] font-black text-gray-400 uppercase tracking-widest">Precio Compra ($)</label>
              <input 
                type="number" required
                value={formData.precio_compra}
                onChange={(e) => setFormData({...formData, precio_compra: e.target.value})}
                className="w-full px-6 py-4 rounded-xl border border-gray-100 bg-[#f8f9fa] outline-none focus:ring-2 focus:ring-[#4263eb]"
              />
            </div>
            <div className="space-y-2">
              <label className="text-[13px] font-black text-gray-400 uppercase tracking-widest">Precio Venta ($)</label>
              <input 
                type="number" required
                value={formData.precio_venta}
                onChange={(e) => setFormData({...formData, precio_venta: e.target.value})}
                className="w-full px-6 py-4 rounded-xl border border-gray-100 bg-[#f8f9fa] outline-none focus:ring-2 focus:ring-[#4263eb]"
              />
            </div>
            <div className="space-y-2">
              <label className="text-[13px] font-black text-gray-400 uppercase tracking-widest">Stock Inicial</label>
              <input 
                type="number" required
                value={formData.stock_actual}
                onChange={(e) => setFormData({...formData, stock_actual: e.target.value})}
                className="w-full px-6 py-4 rounded-xl border border-gray-100 bg-[#f8f9fa] outline-none focus:ring-2 focus:ring-[#4263eb]"
              />
            </div>
   
          </div>
          <button type="submit" className="w-full bg-[#4263eb] text-white py-5 rounded-2xl font-black text-lg shadow-xl hover:bg-[#364fc7] transition-all">
            Registrar Producto
          </button>
        </form>
      </Modal>
      {/* Inventory Movement Modal */}
      <Modal
        isOpen={isAdjustModalOpen}
        onClose={() => setIsAdjustModalOpen(false)}
        title={`Movimiento Inventario: ${selectedProduct?.nombre}`}
      >
        <form onSubmit={handleAdjust} className="space-y-8">

          {/* Current Stock Card */}
          <div className="bg-blue-50 p-6 rounded-2xl border border-blue-100">
            <div className="flex justify-between items-center">
              <div>
                <p className="text-sm font-black uppercase tracking-widest text-blue-500">
                  Stock Actual
                </p>

                <h3 className="text-3xl font-black text-blue-900 mt-1">
                  {selectedProduct?.stock_actual}

                  <span className="text-sm ml-2 uppercase opacity-60">
                    {selectedProduct?.unidad_medida}
                  </span>
                </h3>
              </div>

              {selectedProduct?.bajo_stock && (
                <div className="bg-red-100 text-red-600 px-4 py-2 rounded-xl text-xs font-black uppercase tracking-wider">
                  Bajo Stock
                </div>
              )}
            </div>
          </div>

          {/* Tipo Movimiento */}
          <div className="space-y-2">
            <label className="text-[13px] font-black text-gray-400 uppercase tracking-widest">
              Tipo Movimiento
            </label>
              <select
                value={movementData.tipo}
                onChange={(e) => {
                  console.log("SELECT VALUE:", e.target.value);

                  setMovementData({
                    ...movementData,
                    tipo: e.target.value
                  });
                }}
                className="w-full px-6 py-4 rounded-xl border border-gray-100 bg-[#f8f9fa] outline-none focus:ring-2 focus:ring-[#4263eb] font-bold"
              >
                <option value="Entrada">Entrada</option>
                <option value="Salida">Salida</option>
                <option value="Ajuste">Ajuste</option>
              </select>
          </div>

          {/* Cantidad */}
          <div className="space-y-2">
            <label className="text-[13px] font-black text-gray-400 uppercase tracking-widest">
              Cantidad
            </label>

            <input
              type="number"
              required
              min="1"
              value={movementData.cantidad}
              onChange={(e) =>
                setMovementData({
                  ...movementData,
                  cantidad: e.target.value
                })
              }
              className="w-full px-6 py-5 rounded-xl border border-gray-100 bg-[#f8f9fa] outline-none focus:ring-2 focus:ring-[#4263eb] text-2xl font-black"
              placeholder="Ej. 10"
            />

            <p className="text-xs text-gray-400 font-medium">
              La cantidad siempre debe ser positiva.
            </p>
          </div>

          {/* Motivo */}
          <div className="space-y-2">
            <label className="text-[13px] font-black text-gray-400 uppercase tracking-widest">
              Motivo
            </label>

            <input
              type="text"
              value={movementData.motivo}
              onChange={(e) =>
                setMovementData({
                  ...movementData,
                  motivo: e.target.value
                })
              }
              className="w-full px-6 py-4 rounded-xl border border-gray-100 bg-[#f8f9fa] outline-none focus:ring-2 focus:ring-[#4263eb]"
              placeholder="No motivo"
            />

            <p className="text-xs text-gray-400">
              Si se deja vacío, se registrará como:
              <span className="font-bold"> "No motivo"</span>
            </p>
          </div>

          {/* Observacion */}
          <div className="space-y-2">
            <label className="text-[13px] font-black text-gray-400 uppercase tracking-widest">
              Observación (Opcional)
            </label>

            <textarea
              value={movementData.observacion || ''}
              onChange={(e) =>
                setMovementData({
                  ...movementData,
                  observacion: e.target.value
                })
              }
              className="w-full px-6 py-4 rounded-xl border border-gray-100 bg-[#f8f9fa] outline-none focus:ring-2 focus:ring-[#4263eb] min-h-[120px]"
              placeholder="Información adicional..."
            />
          </div>

          {/* Action Preview */}
          <div className="bg-[#f8f9fa] border border-gray-100 rounded-2xl p-5">
            <p className="text-xs font-black uppercase tracking-widest text-gray-400 mb-2">
              Resumen Movimiento
            </p>

            <div className="flex justify-between items-center">
              <div>
                <p className="font-black text-[#1a1c23]">
                  {movementData.tipo}
                </p>

                <p className="text-sm text-gray-500">
                  {movementData.cantidad || 0} {selectedProduct?.unidad_medida}
                </p>
              </div>

              <div
                className={`px-4 py-2 rounded-xl text-xs font-black uppercase tracking-wider
                  ${
                    movementData.tipo === 'Entrada'
                      ? 'bg-green-100 text-green-600'
                      : movementData.tipo === 'Salida'
                      ? 'bg-red-100 text-red-600'
                      : movementData.tipo === 'Merma'
                      ? 'bg-orange-100 text-orange-600'
                      : 'bg-blue-100 text-blue-600'
                  }
                `}
              >
                {movementData.tipo}
              </div>
            </div>
          </div>

          {/* Submit */}
          <button
            type="submit"
            className="w-full bg-[#1a1c23] text-white py-5 rounded-2xl font-black text-lg shadow-xl hover:bg-black transition-all active:scale-95"
          >
            Registrar Movimiento
          </button>

        </form>
      </Modal>
    </div>
  );
};

export default Inventory;

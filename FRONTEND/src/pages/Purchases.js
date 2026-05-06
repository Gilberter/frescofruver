import React, { useState, useEffect } from 'react';
import { purchases, providers, products } from '../api';
import Modal from '../components/Modal';

const Purchases = () => {
  const [purchaseList, setPurchaseList] = useState([]);
  const [providerList, setProviderList] = useState([]);
  const [productList, setProductList] = useState([]);
  const [loading, setLoading] = useState(true);
  
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [selectedProviderId, setSelectedProviderId] = useState('');
  const [cart, setCart] = useState([]); // { product_id, cantidad, precio_costo }
  const [searchTerm, setSearchTerm] = useState('');

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    setLoading(true);
    try {
      const [ordData, provData, prodData] = await Promise.all([
        purchases.getPurchases(),
        providers.getProviders(),
        products.getProducts()
      ]);
      setPurchaseList(ordData);
      setProviderList(provData);
      setProductList(prodData);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const addToCart = () => {
    const product = productList.find(p => p.nombre.toLowerCase().includes(searchTerm.toLowerCase()));
    if (product) {
      const existing = cart.find(item => item.producto_id === product.id);
      if (existing) {
        setCart(cart.map(item => item.producto_id === product.id ? { ...item, cantidad: item.cantidad + 1 } : item));
      } else {
        setCart([...cart, { producto_id: product.id, nombre: product.nombre, cantidad: 1, precio_costo: product.precio_compra }]);
      }
      setSearchTerm('');
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!selectedProviderId) return alert('Seleccione un proveedor');
    if (cart.length === 0) return alert('La orden está vacía');

    try {
      await purchases.createPurchase({
        proveedor_id: parseInt(selectedProviderId),
        detalles: cart.map(item => ({
          producto_id: item.producto_id,
          cantidad: item.cantidad,
          precio_costo: item.precio_costo
        }))
      });
      setIsModalOpen(false);
      setCart([]);
      setSelectedProviderId('');
      loadData();
    } catch (err) {
      alert('Error al crear orden: ' + (err.response?.data?.detail || err.message));
    }
  };

  const handleReceive = async (id) => {
    try {
      await purchases.receivePurchase(id);
      loadData();
    } catch (err) {
      alert('Error: ' + (err.response?.data?.detail || err.message));
    }
  };

  return (
    <div className="space-y-10">
      <div className="flex justify-between items-end">
        <div>
          <h2 className="text-4xl font-extrabold text-[#1a1c23] mb-2">Abastecimiento</h2>
          <p className="text-lg text-gray-500">Gestione las órdenes de compra y el ingreso de mercancía de proveedores.</p>
        </div>
        <button 
          onClick={() => setIsModalOpen(true)}
          className="bg-[#4263eb] text-white px-8 py-4 rounded-2xl font-bold shadow-xl hover:bg-[#364fc7] transition-all transform hover:scale-105"
        >
          + Nueva Orden de Compra
        </button>
      </div>

      <div className="bg-white p-10 rounded-[32px] shadow-sm border border-gray-100">
        <div className="overflow-hidden rounded-xl">
          <table className="w-full text-left">
            <thead className="bg-[#f8f9fa] border-b border-gray-100">
              <tr>
                <th className="px-6 py-5 font-bold text-[#343a40]">ID Orden</th>
                <th className="px-6 py-5 font-bold text-[#343a40]">Proveedor</th>
                <th className="px-6 py-5 font-bold text-[#343a40]">Fecha</th>
                <th className="px-6 py-5 font-bold text-[#343a40]">Total</th>
                <th className="px-6 py-5 font-bold text-[#343a40]">Estado</th>
                <th className="px-6 py-5 font-bold text-[#343a40]">Acciones</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-100">
              {loading ? (
                <tr><td colSpan="6" className="px-6 py-20 text-center text-gray-400 font-medium">Cargando historial de compras...</td></tr>
              ) : purchaseList.map((ord) => (
                <tr key={ord.id} className="hover:bg-gray-50 transition-colors">
                  <td className="px-6 py-4 font-bold text-[#1a1c23]">#OC-{ord.id}</td>
                  <td className="px-6 py-4 text-gray-600">{ord.proveedor}</td>
                  <td className="px-6 py-4 text-gray-500 text-sm">{new Date(ord.fecha_orden).toLocaleDateString()}</td>
                  <td className="px-6 py-4 font-black text-[#1a1c23]">${ord.total_orden.toLocaleString()}</td>
                  <td className="px-6 py-4">
                    <span className={`px-3 py-1 rounded-full text-xs font-black uppercase tracking-wider ${
                      ord.estado === 'pendiente' ? 'bg-yellow-50 text-yellow-600' :
                      ord.estado === 'recibida' ? 'bg-green-50 text-green-600' : 'bg-red-50 text-red-600'
                    }`}>
                      {ord.estado}
                    </span>
                  </td>
                  <td className="px-6 py-4">
                    {ord.estado === 'pendiente' && (
                      <button 
                        onClick={() => handleReceive(ord.id)}
                        className="bg-green-600 text-white px-4 py-2 rounded-lg font-black text-xs uppercase tracking-wider hover:bg-green-700 transition-all shadow-sm"
                      >
                        Marcar Recibida
                      </button>
                    )}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      <Modal isOpen={isModalOpen} onClose={() => setIsModalOpen(false)} title="Nueva Orden de Compra">
        <form onSubmit={handleSubmit} className="space-y-8">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
            <div className="space-y-2">
              <label className="text-[13px] font-black text-gray-400 uppercase tracking-widest">Proveedor</label>
              <select 
                value={selectedProviderId}
                onChange={(e) => setSelectedProviderId(e.target.value)}
                className="w-full px-6 py-4 rounded-xl border border-gray-100 bg-[#f8f9fa] outline-none focus:ring-2 focus:ring-[#4263eb] font-bold"
              >
                <option value="">Seleccione proveedor...</option>
                {providerList.map(p => (
                  <option key={p.id} value={p.id}>{p.nombre}</option>
                ))}
              </select>
            </div>
            <div className="space-y-2">
              <label className="text-[13px] font-black text-gray-400 uppercase tracking-widest">Buscar Producto</label>
              <div className="flex gap-4">
                <input 
                  type="text" 
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  className="w-full px-6 py-4 rounded-xl border border-gray-100 bg-[#f8f9fa] outline-none focus:ring-2 focus:ring-[#4263eb]"
                />
                <button type="button" onClick={addToCart} className="bg-[#1a1c23] text-white px-6 py-4 rounded-xl font-black shadow-lg hover:bg-black transition-all">
                  +
                </button>
              </div>
            </div>
          </div>

          <div className="border-t border-gray-100 pt-8">
            <h4 className="text-[15px] font-black text-[#343a40] uppercase tracking-widest mb-4">Productos en la Orden</h4>
            <div className="space-y-3">
              {cart.map((item, idx) => (
                <div key={idx} className="flex justify-between items-center bg-[#f8f9fa] p-4 rounded-xl border border-gray-100">
                  <div>
                    <p className="font-bold text-[#1a1c23]">{item.nombre}</p>
                    <p className="text-xs text-gray-500 uppercase font-black tracking-tighter">Costo Unit: ${item.precio_costo}</p>
                  </div>
                  <div className="flex items-center gap-6">
                    <input 
                      type="number"
                      value={item.cantidad}
                      onChange={(e) => setCart(cart.map((c, i) => i === idx ? { ...c, cantidad: parseInt(e.target.value) } : c))}
                      className="w-20 px-3 py-2 rounded-lg border border-gray-200 bg-white outline-none focus:ring-2 focus:ring-[#4263eb] font-bold text-center"
                    />
                    <button type="button" onClick={() => setCart(cart.filter((_, i) => i !== idx))} className="text-red-500 font-black text-xs uppercase hover:underline">Eliminar</button>
                  </div>
                </div>
              ))}
              {cart.length === 0 && <p className="text-center py-8 text-gray-400 italic">No hay productos agregados.</p>}
            </div>
          </div>

          <div className="pt-6">
            <button type="submit" className="w-full bg-[#4263eb] text-white py-5 rounded-2xl font-black text-lg shadow-xl hover:bg-[#364fc7] transition-all">
              Generar Orden de Compra
            </button>
          </div>
        </form>
      </Modal>
    </div>
  );
};

export default Purchases;

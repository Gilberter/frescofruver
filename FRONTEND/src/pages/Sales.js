import React, { useMemo, useState, useEffect } from 'react';
import { products, clients, sales } from '../api';

import Modal from '../components/Modal';

const Sales = () => {
  const [searchTerm, setSearchTerm] = useState('');
  const [cart, setCart] = useState([]);
  const [productList, setProductList] = useState([]);
  const [clientList, setClientList] = useState([]);
  const [clientSearch, setClientSearch] = useState('');
  const [selectedClientId, setSelectedClientId] = useState('');
  const [loading, setLoading] = useState(false);
  
  // Quick Client State
  const [isClientModalOpen, setIsClientModalOpen] = useState(false);
  const [clientFormData, setClientFormData] = useState({
    nombre_completo: '',
    no_documento: '',
    telefono: '',
    direccion: ''
  });

  useEffect(() => {
    loadInitialData();
  }, []);

  const loadInitialData = async () => {
    try {
      const [prodData, cliData] = await Promise.all([
        products.getProducts(),
        clients.getClients()
      ]);
      setProductList(prodData);
      setClientList(cliData);
    } catch (err) {
      console.error(err);
    }
  };

  const addToCart = (product) => {
    if (!product) return;

    if (product.stock_actual <= 0) {
      return;
    }

    const existing = cart.find(item => item.id === product.id);

    if (existing) {
      if (existing.cantidad >= product.stock_actual) {
        return;
      }

      setCart(prev =>
        prev.map(item =>
          item.id === product.id
            ? { ...item, cantidad: item.cantidad + 1 }
            : item
        )
      );
    } else {
      setCart(prev => [
        ...prev,
        {
          id: product.id,
          nombre: product.nombre,
          precio_venta: product.precio_venta,
          unidad_medida: product.unidad_medida,
          stock_actual: product.stock_actual,
          cantidad: 1
        }
      ]);
    }
  };

  const filteredProducts = useMemo(() => {
    if (!searchTerm.trim()) return [];

    return productList.filter(product =>
      product.nombre
        .toLowerCase()
        .includes(searchTerm.toLowerCase())
    );
  }, [searchTerm, productList]);


  const filteredClients = useMemo(() => {
    if (!clientSearch.trim()) return [];

    return clientList.filter(client =>
      client.no_documento
        .toLowerCase()
        .includes(clientSearch.toLowerCase())
    );
  }, [clientSearch, clientList]);

  const handleQuickClientRegister = async (e) => {
    e.preventDefault();
    try {
      const newClient = await clients.createClient(clientFormData);
      setClientList([...clientList, newClient]);
      setSelectedClientId(newClient.id.toString());
      setIsClientModalOpen(false);
      setClientFormData({ nombre_completo: '', no_documento: '', telefono: '', direccion: '' });
    } catch (err) {
      alert('Error al registrar cliente: ' + (err.response?.data?.detail || err.message));
    }
  };

  const confirmSale = async () => {
    if (!selectedClientId) return alert('Seleccione un cliente');
    if (cart.length === 0) return alert('El carrito está vacío');

    setLoading(true);
    try {
      const saleData = {
        cliente_id: parseInt(selectedClientId),
        detalles: cart.map(item => ({
          producto_id: item.id,
          cantidad: item.cantidad
        }))
      };
      await sales.createSale(saleData);
      alert('Venta confirmada exitosamente');
      setCart([]);
      setSelectedClientId('');
      loadInitialData();
    } catch (err) {
      alert('Error al confirmar venta: ' + (err.response?.data?.detail || err.message));
    } finally {
      setLoading(false);
    }
  };

  const subtotal = cart.reduce((acc, item) => acc + (item.precio_venta * item.cantidad), 0);
  const iva = subtotal * 0.19;
  const total = subtotal + iva;

  return (
    <div className="flex flex-col lg:flex-row gap-8">
      <div className="flex-1 bg-white p-10 rounded-[40px] shadow-sm border border-gray-100">
        <h2 className="text-4xl font-black text-[#1a1c23] mb-10 tracking-tighter">Módulo de Ventas</h2>
        
        <div className="grid grid-cols-1 md:grid-cols-2 gap-8 mb-10">
          {/* <div className="space-y-3">
            <div className="flex justify-between items-center">
              <label className="text-[13px] font-black text-gray-400 uppercase tracking-widest">Cliente</label>
              <button 
                onClick={() => setIsClientModalOpen(true)}
                className="text-[#4263eb] text-xs font-black uppercase tracking-tighter hover:underline"
              >
                + Registro Rápido
              </button>
            </div>
            <select 
              value={selectedClientId}
              onChange={(e) => setSelectedClientId(e.target.value)}
              className="w-full px-6 py-4 rounded-2xl border border-gray-100 bg-[#f8f9fa] outline-none focus:ring-2 focus:ring-[#4263eb] font-bold text-[#1a1c23]"
            >
              <option value="">Seleccione un cliente...</option>
              {clientList.map(c => (
                <option key={c.id} value={c.id}>{c.nombre_completo} (CC: {c.no_documento})</option>
              ))}
            </select>
          </div> */}



          <div className="space-y-3 relative">
            <div className="flex justify-between items-center">
              <label className="text-[13px] font-black text-gray-400 uppercase tracking-widest">
                Cliente
              </label>

              <button
                onClick={() => setIsClientModalOpen(true)}
                className="text-[#4263eb] text-xs font-black uppercase tracking-tighter hover:underline"
              >
                + Registro Rápido
              </button>
            </div>

            <input
              type="text"
              value={clientSearch}
              onChange={(e) => setClientSearch(e.target.value)}
              placeholder="Buscar por cédula..."
              className="w-full px-6 py-4 rounded-2xl border border-gray-100 bg-[#f8f9fa] outline-none focus:ring-2 focus:ring-[#4263eb] font-bold text-[#1a1c23]"
            />

            {/* Dropdown Clientes */}
            {clientSearch.trim() && filteredClients.length > 0 && (
              <div className="absolute z-50 w-full mt-2 bg-white border border-gray-100 rounded-2xl shadow-2xl overflow-hidden max-h-80 overflow-y-auto">
                {filteredClients.map((client) => (
                  <button
                    key={client.id}
                    type="button"
                    onClick={() => {
                      setSelectedClientId(client.id.toString());
                      setClientSearch(
                        `${client.nombre_completo} - ${client.no_documento}`
                      );
                    }}
                    className="w-full px-6 py-4 text-left hover:bg-gray-50 transition-all border-b border-gray-50 last:border-b-0"
                  >
                    <div className="flex justify-between items-center">
                      <div>
                        <p className="font-bold text-[#1a1c23]">
                          {client.nombre_completo}
                        </p>

                        <p className="text-sm text-gray-400">
                          CC: {client.no_documento}
                        </p>
                      </div>

                      <div className="text-right">
                        <p className="text-sm font-medium text-gray-500">
                          {client.telefono}
                        </p>
                      </div>
                    </div>
                  </button>
                ))}
              </div>
            )}

            {/* Sin resultados */}
            {clientSearch.trim() && filteredClients.length === 0 && (
              <div className="absolute z-50 w-full mt-2 bg-white border border-gray-100 rounded-2xl shadow-lg p-4 text-gray-400 text-sm">
                No se encontraron clientes
              </div>
            )}
          </div>
          

          <div className="space-y-3 relative">
            <label className="text-[13px] font-black text-gray-400 uppercase tracking-widest">
              Buscar Producto
            </label>

            <div className="flex gap-4">
              <input
                type="text"
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                placeholder="Nombre del producto..."
                className="flex-1 px-6 py-4 rounded-2xl border border-gray-100 bg-[#f8f9fa] outline-none focus:ring-2 focus:ring-[#4263eb]"
              />

              <button
                onClick={addToCart}
                className="bg-[#1a1c23] text-white px-8 py-4 rounded-2xl font-black shadow-lg hover:bg-black transition-all"
              >
                +
              </button>
            </div>

            {/* Dropdown Productos */}
            {searchTerm.trim() && filteredProducts.length > 0 && (
              <div className="absolute z-50 w-full mt-2 bg-white border border-gray-100 rounded-2xl shadow-2xl overflow-hidden max-h-80 overflow-y-auto">
                {filteredProducts.map((product) => (
                  <button
                    key={product.id}
                    type="button"
                    onClick={() => {
                      addToCart(product);
                      setSearchTerm('');
                    }}
                    className="w-full px-6 py-4 text-left hover:bg-gray-50 transition-all border-b border-gray-50 last:border-b-0"
                  >
                    <div className="flex justify-between items-center">
                      <div>
                        <p className="font-bold text-[#1a1c23]">
                          {product.nombre}
                        </p>

                        <p className="text-sm text-gray-400">
                          Stock: {product.stock_actual} {product.unidad_medida}
                        </p>
                      </div>

                      <div className="text-right">
                        <p className="font-black text-[#4263eb]">
                          ${product.precio_venta.toLocaleString()}
                        </p>
                      </div>
                    </div>
                  </button>
                ))}
              </div>
            )}

            {/* Sin resultados */}
            {searchTerm.trim() && filteredProducts.length === 0 && (
              <div className="absolute z-50 w-full mt-2 bg-white border border-gray-100 rounded-2xl shadow-lg p-4 text-gray-400 text-sm">
                No se encontraron productos
              </div>
            )}
          </div>




          
        </div>

        <div>
          <h3 className="text-xl font-bold text-[#343a40] mb-6">Detalle de Venta</h3>
          <div className="overflow-hidden rounded-2xl border border-gray-100">
            <table className="w-full text-left">
              <thead className="bg-[#f8f9fa]">
                <tr>
                  <th className="px-6 py-5 font-bold text-[#343a40]">Producto</th>
                  <th className="px-6 py-5 font-bold text-[#343a40]">Cantidad</th>
                  <th className="px-6 py-5 font-bold text-[#343a40]">Precio</th>
                  <th className="px-6 py-5 font-bold text-[#343a40]">Subtotal</th>
                  <th className="px-6 py-5 font-bold text-[#343a40]">Acciones</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-100">
                {cart.length > 0 ? cart.map((item) => (
                  <tr key={item.id} className="hover:bg-gray-50 transition-colors">
                    <td className="px-6 py-5 font-bold text-[#1a1c23]">{item.nombre}</td>
                    <td className="px-6 py-5 text-[#343a40] font-medium">{item.cantidad} {item.unidad_medida}</td>
                    <td className="px-6 py-5 text-[#343a40]">${item.precio_venta.toLocaleString()}</td>
                    <td className="px-6 py-5 text-[#343a40] font-black">${(item.precio_venta * item.cantidad).toLocaleString()}</td>
                    <td className="px-6 py-5">
                      <button 
                        onClick={() => setCart(cart.filter(i => i.id !== item.id))} 
                        className="text-red-500 font-black text-xs uppercase hover:underline"
                      >
                        Quitar
                      </button>
                    </td>
                  </tr>
                )) : (
                  <tr>
                    <td colSpan="5" className="px-6 py-20 text-center text-gray-400 font-medium italic">Agregue productos para iniciar la venta.</td>
                  </tr>
                )}
              </tbody>
            </table>
          </div>
        </div>
      </div>

      <div className="w-full lg:w-[450px] flex flex-col gap-8">
        <div className="bg-white p-10 rounded-[40px] shadow-sm border border-gray-100">
          <h3 className="text-2xl font-black text-[#1a1c23] mb-8 tracking-tight">Resumen de Pago</h3>
          
          <div className="space-y-5 mb-10">
            <div className="flex justify-between items-center text-gray-500 font-medium">
              <span className="text-lg">Subtotal:</span>
              <span className="text-xl font-bold">${subtotal.toLocaleString()}</span>
            </div>
            <div className="flex justify-between items-center text-gray-500 font-medium">
              <span className="text-lg">IVA (19%):</span>
              <span className="text-xl font-bold">${iva.toLocaleString()}</span>
            </div>
            <div className="border-t-2 border-dashed border-gray-100 pt-6 mt-6 flex justify-between items-center">
              <span className="text-2xl font-black text-[#4263eb] uppercase tracking-tighter">Total a Pagar</span>
              <span className="text-4xl font-black text-[#4263eb] tracking-tighter">${total.toLocaleString()}</span>
            </div>
          </div>

          <button 
            disabled={loading || cart.length === 0}
            onClick={confirmSale}
            className={`w-full py-6 rounded-2xl font-black text-xl shadow-2xl transition-all mb-4 active:scale-95 ${loading ? 'bg-gray-400 cursor-not-allowed' : 'bg-[#4263eb] text-white hover:bg-[#364fc7]'}`}
          >
            {loading ? 'Confirmando...' : 'Confirmar Venta'}
          </button>
          <button 
            onClick={() => setCart([])}
            className="w-full bg-[#f8f9fa] text-gray-400 py-4 rounded-2xl font-black text-sm border border-gray-100 hover:bg-gray-100 transition-all uppercase tracking-widest"
          >
            Vaciár Carrito
          </button>
        </div>
      </div>

      {/* Quick Client Modal */}
      <Modal isOpen={isClientModalOpen} onClose={() => setIsClientModalOpen(false)} title="Registro Rápido de Cliente">
        <form onSubmit={handleQuickClientRegister} className="space-y-6">
          <div className="space-y-4">
            <div className="space-y-2">
              <label className="text-[13px] font-black text-gray-400 uppercase tracking-widest">Nombre Completo</label>
              <input 
                type="text" required
                value={clientFormData.nombre_completo}
                onChange={(e) => setClientFormData({...clientFormData, nombre_completo: e.target.value})}
                className="w-full px-6 py-4 rounded-xl border border-gray-100 bg-[#f8f9fa] outline-none focus:ring-2 focus:ring-[#4263eb]"
              />
            </div>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div className="space-y-2">
                <label className="text-[13px] font-black text-gray-400 uppercase tracking-widest">Documento (CC)</label>
                <input 
                  type="text" required
                  value={clientFormData.no_documento}
                  onChange={(e) => setClientFormData({...clientFormData, no_documento: e.target.value})}
                  className="w-full px-6 py-4 rounded-xl border border-gray-100 bg-[#f8f9fa] outline-none focus:ring-2 focus:ring-[#4263eb]"
                />
              </div>
              <div className="space-y-2">
                <label className="text-[13px] font-black text-gray-400 uppercase tracking-widest">Teléfono</label>
                <input 
                  type="text" required
                  value={clientFormData.telefono}
                  onChange={(e) => setClientFormData({...clientFormData, telefono: e.target.value})}
                  className="w-full px-6 py-4 rounded-xl border border-gray-100 bg-[#f8f9fa] outline-none focus:ring-2 focus:ring-[#4263eb]"
                />
              </div>
            </div>
            <div className="space-y-2">
              <label className="text-[13px] font-black text-gray-400 uppercase tracking-widest">Dirección</label>
              <input 
                type="text" required
                value={clientFormData.direccion}
                onChange={(e) => setClientFormData({...clientFormData, direccion: e.target.value})}
                className="w-full px-6 py-4 rounded-xl border border-gray-100 bg-[#f8f9fa] outline-none focus:ring-2 focus:ring-[#4263eb]"
              />
            </div>
          </div>
          <button type="submit" className="w-full bg-[#1a1c23] text-white py-5 rounded-2xl font-black text-lg shadow-xl hover:bg-black transition-all">
            Registrar y Continuar Pedido
          </button>
        </form>
      </Modal>
    </div>
  );
};

export default Sales;

import React, { useState, useEffect } from 'react';
import { providers, auth } from '../api';
import Modal from '../components/Modal';

const Providers = () => {
  const [providerList, setProviderList] = useState([]);
  const [loading, setLoading] = useState(true);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [modalMode, setModalMode] = useState('create'); // 'create' or 'edit'
  const [selectedId, setSelectedId] = useState(null);
  const currentUser = auth.getCurrentUser();
  const isAdminOrOwner = currentUser?.rol === 'Administrador' || currentUser?.rol === 'Dueño';

  const [formData, setFormData] = useState({
    nombre: '',
    contacto: '',
    telefono: '',
    correo: '',
    direccion: ''
  });

  useEffect(() => {
    loadProviders();
  }, []);

  const loadProviders = async () => {
    setLoading(true);
    try {
      const data = await providers.getProviders();
      setProviderList(data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const openCreateModal = () => {
    setModalMode('create');
    setFormData({ nombre: '', contacto: '', telefono: '', correo: '', direccion: '' });
    setIsModalOpen(true);
  };

  const openEditModal = (p) => {
    setModalMode('edit');
    setSelectedId(p.id);
    setFormData({
      nombre: p.nombre,
      contacto: p.contacto || '',
      telefono: p.telefono || '',
      correo: p.correo || '',
      direccion: p.direccion || ''
    });
    setIsModalOpen(true);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      if (modalMode === 'create') {
        await providers.createProvider(formData);
      } else {
        await providers.updateProvider(selectedId, formData);
      }
      setIsModalOpen(false);
      loadProviders();
    } catch (err) {
      alert('Error en la operación: ' + (err.response?.data?.detail?.[0]?.msg || err.response?.data?.detail || err.message));
    }
  };

  const toggleStatus = async (p) => {
    const newStatus = p.estado === 'activo' ? 'inactivo' : 'activo';
    if (!window.confirm(`¿Está seguro de cambiar el estado de ${p.nombre} a ${newStatus}?`)) return;
    
    try {
      await providers.updateProvider(p.id, { estado: newStatus });
      loadProviders();
    } catch (err) {
      alert('Error al cambiar estado: ' + err.message);
    }
  };

  return (
    <div className="space-y-10">
      <div className="flex justify-between items-end">
        <div>
          <h2 className="text-4xl font-black text-[#1a1c23] tracking-tight">Proveedores Estratégicos</h2>
          <p className="text-lg text-gray-500 mt-2">Administre su red de suministros y contactos de confianza.</p>
        </div>
        {isAdminOrOwner && (
          <button 
            onClick={openCreateModal}
            className="bg-[#4263eb] text-white px-8 py-4 rounded-2xl font-black shadow-xl hover:bg-[#364fc7] transition-all transform hover:scale-105 active:scale-95"
          >
            + Nuevo Proveedor
          </button>
        )}
      </div>

      <div className="bg-white p-10 rounded-[40px] shadow-sm border border-gray-100">
        <div className="overflow-hidden rounded-2xl">
          <table className="w-full text-left">
            <thead className="bg-[#f8f9fa] border-b border-gray-100">
              <tr>
                <th className="px-6 py-6 font-black text-[#343a40] text-xs uppercase tracking-widest">Nombre / Empresa</th>
                <th className="px-6 py-6 font-black text-[#343a40] text-xs uppercase tracking-widest">Contacto Directo</th>
                <th className="px-6 py-6 font-black text-[#343a40] text-xs uppercase tracking-widest text-center">Estado</th>
                <th className="px-6 py-6 font-black text-[#343a40] text-xs uppercase tracking-widest">Comunicación</th>
                <th className="px-6 py-6 font-black text-[#343a40] text-xs uppercase tracking-widest">Acciones</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-100">
              {loading ? (
                <tr><td colSpan="5" className="px-6 py-20 text-center text-gray-400 font-medium italic">Sincronizando red de proveedores...</td></tr>
              ) : providerList.map((p) => (
                <tr key={p.id} className="hover:bg-gray-50 transition-colors">
                  <td className="px-6 py-5">
                    <div className="flex flex-col">
                      <span className="font-black text-[#1a1c23] text-lg">{p.nombre}</span>
                      <span className="text-xs text-gray-400 font-bold uppercase">{p.direccion || 'Sin dirección registrada'}</span>
                    </div>
                  </td>
                  <td className="px-6 py-5">
                    <div className="flex flex-col">
                      <span className="font-bold text-gray-700">{p.contacto || 'N/A'}</span>
                      <span className="text-xs text-[#4263eb] font-black">{p.telefono}</span>
                    </div>
                  </td>
                  <td className="px-6 py-5 text-center">
                    <span className={`px-4 py-1.5 rounded-full text-[10px] font-black uppercase tracking-widest ${p.estado === 'activo' ? 'bg-green-50 text-green-600' : 'bg-red-50 text-red-600'}`}>
                      {p.estado}
                    </span>
                  </td>
                  <td className="px-6 py-5">
                    <div className="flex items-center gap-2">
                      <div className="w-8 h-8 rounded-lg bg-blue-50 flex items-center justify-center">
                        <svg className="w-4 h-4 text-[#4263eb]" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="3" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"></path></svg>
                      </div>
                      <span className="text-sm font-bold text-gray-600">{p.correo}</span>
                    </div>
                  </td>
                  <td className="px-6 py-5">
                    {isAdminOrOwner && (
                      <div className="flex items-center gap-2">
                        <button 
                          onClick={() => openEditModal(p)}
                          className="p-2 text-gray-400 hover:text-[#4263eb] hover:bg-blue-50 rounded-lg transition-all"
                          title="Editar"
                        >
                          <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"></path></svg>
                        </button>
                        <button 
                          onClick={() => toggleStatus(p)}
                          className={`p-2 rounded-lg transition-all ${p.estado === 'activo' ? 'text-gray-400 hover:text-red-500 hover:bg-red-50' : 'text-gray-400 hover:text-green-500 hover:bg-green-50'}`}
                          title={p.estado === 'activo' ? 'Desactivar' : 'Activar'}
                        >
                          {p.estado === 'activo' ? (
                            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M18.364 18.364A9 9 0 005.636 5.636m12.728 12.728A9 9 0 015.636 5.636m12.728 12.728L5.636 5.636"></path></svg>
                          ) : (
                            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
                          )}
                        </button>
                      </div>
                    )}
                  </td>
                </tr>
              ))}
              {providerList.length === 0 && !loading && (
                <tr><td colSpan="5" className="px-6 py-20 text-center text-gray-400 italic">No se han registrado proveedores aún.</td></tr>
              )}
            </tbody>
          </table>
        </div>
      </div>

      {/* Provider Modal */}
      <Modal isOpen={isModalOpen} onClose={() => setIsModalOpen(false)} title={modalMode === 'create' ? 'Registrar Proveedor' : 'Editar Proveedor'}>
        <form onSubmit={handleSubmit} className="space-y-8">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div className="space-y-2 md:col-span-2">
              <label className="text-[11px] font-black text-gray-400 uppercase tracking-widest ml-1">Razón Social / Nombre Comercial</label>
              <input 
                type="text" required
                value={formData.nombre}
                onChange={(e) => setFormData({...formData, nombre: e.target.value})}
                className="w-full px-6 py-4 rounded-2xl border border-gray-100 bg-[#f8f9fa] outline-none focus:ring-2 focus:ring-[#4263eb] font-bold"
                placeholder="Ej. Distribuidora del Campo SAS"
              />
            </div>
            <div className="space-y-2">
              <label className="text-[11px] font-black text-gray-400 uppercase tracking-widest ml-1">Persona de Contacto</label>
              <input 
                type="text"
                value={formData.contacto}
                onChange={(e) => setFormData({...formData, contacto: e.target.value})}
                className="w-full px-6 py-4 rounded-2xl border border-gray-100 bg-[#f8f9fa] outline-none focus:ring-2 focus:ring-[#4263eb]"
                placeholder="Ej. Juan Pérez"
              />
            </div>
            <div className="space-y-2">
              <label className="text-[11px] font-black text-gray-400 uppercase tracking-widest ml-1">Teléfono Principal</label>
              <input 
                type="text"
                value={formData.telefono}
                onChange={(e) => setFormData({...formData, telefono: e.target.value})}
                className="w-full px-6 py-4 rounded-2xl border border-gray-100 bg-[#f8f9fa] outline-none focus:ring-2 focus:ring-[#4263eb]"
                placeholder="+57 300..."
              />
            </div>
            <div className="space-y-2">
              <label className="text-[11px] font-black text-gray-400 uppercase tracking-widest ml-1">Correo Corporativo</label>
              <input 
                type="email"
                value={formData.correo}
                onChange={(e) => setFormData({...formData, correo: e.target.value})}
                className="w-full px-6 py-4 rounded-2xl border border-gray-100 bg-[#f8f9fa] outline-none focus:ring-2 focus:ring-[#4263eb]"
                placeholder="proveedor@empresa.com"
              />
            </div>
            <div className="space-y-2">
              <label className="text-[11px] font-black text-gray-400 uppercase tracking-widest ml-1">Dirección Física</label>
              <input 
                type="text"
                value={formData.direccion}
                onChange={(e) => setFormData({...formData, direccion: e.target.value})}
                className="w-full px-6 py-4 rounded-2xl border border-gray-100 bg-[#f8f9fa] outline-none focus:ring-2 focus:ring-[#4263eb]"
                placeholder="Carrera 10 #..."
              />
            </div>
          </div>
          <button type="submit" className="w-full bg-[#4263eb] text-white py-6 rounded-[24px] font-black text-lg shadow-2xl hover:bg-[#364fc7] transition-all transform active:scale-95">
            {modalMode === 'create' ? 'Crear Proveedor' : 'Guardar Cambios'}
          </button>
        </form>
      </Modal>
    </div>
  );
};

export default Providers;

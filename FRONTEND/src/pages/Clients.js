import React, { useState, useEffect } from 'react';
import { clients } from '../api';
import Modal from '../components/Modal';

const Clients = () => {
  const [clientList, setClientList] = useState([]);
  const [loading, setLoading] = useState(true);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [formData, setFormData] = useState({
    nombre_completo: '',
    no_documento: '',
    telefono: '',
    direccion: ''
  });

  useEffect(() => {
    loadClients();
  }, []);

  const loadClients = async () => {
    try {
      const data = await clients.getClients();
      setClientList(data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await clients.createClient(formData);
      setIsModalOpen(false);
      setFormData({ nombre_completo: '', no_documento: '', telefono: '', direccion: '' });
      loadClients();
    } catch (err) {
      alert('Error al registrar cliente: ' + (err.response?.data?.detail || err.message));
    }
  };

  return (
    <div className="space-y-10">
      <div className="flex justify-between items-end">
        <div>
          <h2 className="text-4xl font-extrabold text-[#1a1c23] mb-2">Cartera de Clientes</h2>
          <p className="text-lg text-gray-500">Gestione la información y contacto de sus clientes habituales.</p>
        </div>
        <button 
          onClick={() => setIsModalOpen(true)}
          className="bg-[#4263eb] text-white px-8 py-4 rounded-2xl font-bold shadow-xl hover:bg-[#364fc7] transition-all transform hover:scale-105 active:scale-95"
        >
          + Registrar Cliente
        </button>
      </div>

      <div className="bg-white p-10 rounded-[32px] shadow-sm border border-gray-100">
        <div className="overflow-hidden rounded-xl">
          <table className="w-full text-left">
            <thead className="bg-[#f8f9fa] border-b border-gray-100">
              <tr>
                <th className="px-6 py-5 font-bold text-[#343a40]">Nombre Completo</th>
                <th className="px-6 py-5 font-bold text-[#343a40]">Documento (CC)</th>
                <th className="px-6 py-5 font-bold text-[#343a40]">Teléfono</th>
                <th className="px-6 py-5 font-bold text-[#343a40]">Dirección</th>
                <th className="px-6 py-5 font-bold text-[#343a40]">Estado</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-100">
              {loading ? (
                <tr><td colSpan="5" className="px-6 py-20 text-center text-gray-400 font-medium">Consultando base de clientes...</td></tr>
              ) : clientList.map((c) => (
                <tr key={c.id} className="hover:bg-gray-50 transition-colors">
                  <td className="px-6 py-4 font-bold text-[#1a1c23]">{c.nombre_completo}</td>
                  <td className="px-6 py-4 text-gray-600">{c.no_documento}</td>
                  <td className="px-6 py-4 text-gray-600">{c.telefono}</td>
                  <td className="px-6 py-4 text-gray-600 text-sm">{c.direccion}</td>
                  <td className="px-6 py-4">
                    <span className="bg-green-50 text-green-600 px-3 py-1 rounded-full text-xs font-black uppercase">Activo</span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      <Modal isOpen={isModalOpen} onClose={() => setIsModalOpen(false)} title="Registrar Cliente">
        <form onSubmit={handleSubmit} className="space-y-6">
          <div className="space-y-4">
            <div className="space-y-2">
              <label className="text-[13px] font-black text-gray-400 uppercase tracking-widest">Nombre Completo</label>
              <input 
                type="text" required
                value={formData.nombre_completo}
                onChange={(e) => setFormData({...formData, nombre_completo: e.target.value})}
                className="w-full px-6 py-4 rounded-xl border border-gray-100 bg-[#f8f9fa] outline-none focus:ring-2 focus:ring-[#4263eb]"
              />
            </div>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div className="space-y-2">
                <label className="text-[13px] font-black text-gray-400 uppercase tracking-widest">No. Documento</label>
                <input 
                  type="text" required
                  value={formData.no_documento}
                  onChange={(e) => setFormData({...formData, no_documento: e.target.value})}
                  className="w-full px-6 py-4 rounded-xl border border-gray-100 bg-[#f8f9fa] outline-none focus:ring-2 focus:ring-[#4263eb]"
                />
              </div>
              <div className="space-y-2">
                <label className="text-[13px] font-black text-gray-400 uppercase tracking-widest">Teléfono</label>
                <input 
                  type="text" required
                  value={formData.telefono}
                  onChange={(e) => setFormData({...formData, telefono: e.target.value})}
                  className="w-full px-6 py-4 rounded-xl border border-gray-100 bg-[#f8f9fa] outline-none focus:ring-2 focus:ring-[#4263eb]"
                />
              </div>
            </div>
            <div className="space-y-2">
              <label className="text-[13px] font-black text-gray-400 uppercase tracking-widest">Dirección</label>
              <input 
                type="text" required
                value={formData.direccion}
                onChange={(e) => setFormData({...formData, direccion: e.target.value})}
                className="w-full px-6 py-4 rounded-xl border border-gray-100 bg-[#f8f9fa] outline-none focus:ring-2 focus:ring-[#4263eb]"
              />
            </div>
          </div>
          <button type="submit" className="w-full bg-[#4263eb] text-white py-5 rounded-2xl font-black text-lg shadow-xl hover:bg-[#364fc7] transition-all">
            Crear Registro de Cliente
          </button>
        </form>
      </Modal>
    </div>
  );
};

export default Clients;

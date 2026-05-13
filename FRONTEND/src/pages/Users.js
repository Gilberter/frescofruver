import React, { useState, useEffect } from 'react';
import { users } from '../api';
import Modal from '../components/Modal';

const Users = () => {
  const [userList, setUserList] = useState([]);
  const [loading, setLoading] = useState(true);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [formData, setFormData] = useState({
    nombre_completo: '',
    no_documento: '',
    username: '',
    password: '',
    correo: '',
    telefono: '',
    rol: 'Vendedor',
    estado: 'Activo'
  });

  useEffect(() => {
    loadUsers();
  }, []);

  const loadUsers = async () => {
    try {
      const data = await users.getUsers();
      setUserList(data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {

      if (formData.password.length < 6) {
        alert("La contraseña debe tener mínimo 6 caracteres");
        return;
      }
      await users.createUser(formData);
      setIsModalOpen(false);
      setFormData({
        nombre_completo: '',
        no_documento: '',
        username: '',
        password: '',
        correo: '',
        telefono: '',
        rol: 'Vendedor',
        estado: 'Activo'
      });

      loadUsers();

    } catch (err) {
      alert('Error al crear usuario: ' + (err.response?.data?.detail || err.message));
    }
  };

  const toggleStatus = async (user) => {
    try {
      if (user.estado === 'Activo') {
        // Use the specific DELETE endpoint for deactivation (RF-01.4)
        await users.deactivateUser(user.id);
      } else {
        // Use PATCH for re-activation
        await users.updateUser(user.id, { estado: 'Activo' });
      }
      loadUsers();
    } catch (err) {
      alert('Error al cambiar estado: ' + (err.response?.data?.detail || err.message));
    }
  };

  return (
    <div className="space-y-10">
      <div className="flex justify-between items-end">
        <div>
          <h2 className="text-4xl font-extrabold text-[#1a1c23] mb-2">Gestión de Usuarios</h2>
          <p className="text-lg text-gray-500">Administre los accesos y roles del personal.</p>
        </div>
        <button 
          onClick={() => setIsModalOpen(true)}
          className="bg-[#4263eb] text-white px-8 py-4 rounded-2xl font-bold shadow-xl hover:bg-[#364fc7] transition-all transform hover:scale-105 active:scale-95"
        >
          + Nuevo Usuario
        </button>
      </div>

      <div className="bg-white p-10 rounded-[32px] shadow-sm border border-gray-100">
        <div className="overflow-hidden rounded-xl">
          <table className="w-full text-left">
            <thead className="bg-[#f8f9fa] border-b border-gray-100">
              <tr>
                <th className="px-6 py-5 font-bold text-[#343a40]">Nombre Completo</th>
                <th className="px-6 py-5 font-bold text-[#343a40]">Usuario</th>
                <th className="px-6 py-5 font-bold text-[#343a40]">Rol</th>
                <th className="px-6 py-5 font-bold text-[#343a40]">Estado</th>
                <th className="px-6 py-5 font-bold text-[#343a40]">Acciones</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-100">
              {loading ? (
                <tr><td colSpan="5" className="px-6 py-20 text-center text-gray-400 font-medium">Sincronizando base de datos de usuarios...</td></tr>
              ) : userList.map((u) => (
                <tr key={u.id} className="hover:bg-gray-50 transition-colors">
                  <td className="px-6 py-4 font-bold text-[#1a1c23]">{u.nombre_completo}</td>
                  <td className="px-6 py-4 text-gray-600">{u.username}</td>
                  <td className="px-6 py-4">
                    <span className="bg-blue-50 text-blue-600 px-4 py-1.5 rounded-full text-xs font-black uppercase tracking-wider">{u.rol}</span>
                  </td>
                  <td className="px-6 py-4">
                    <div className="flex items-center">
                      <div className={`w-2.5 h-2.5 rounded-full mr-2 ${u.estado === 'Activo' ? 'bg-green-500' : 'bg-red-500'}`}></div>
                      <span className={`font-bold capitalize ${u.estado === 'Activo' ? 'text-green-600' : 'text-red-500'}`}>
                        {u.estado}
                      </span>
                    </div>
                  </td>
                  <td className="px-6 py-4">
                    <button 
                      onClick={() => toggleStatus(u)}
                      className={`font-black text-sm uppercase tracking-tighter hover:underline ${u.estado === 'Activo' ? 'text-red-500' : 'text-green-600'}`}
                    >
                      {u.estado === 'Activo' ? 'Desactivar' : 'Activar'}
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      <Modal isOpen={isModalOpen} onClose={() => setIsModalOpen(false)} title="Registrar Nuevo Usuario">
        <form onSubmit={handleSubmit} className="space-y-6">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div className="space-y-2">
              <label className="text-[14px] font-black text-[#343a40] uppercase tracking-wider">Nombre Completo</label>
              <input 
                type="text" required
                value={formData.nombre_completo}
                onChange={(e) => setFormData({...formData, nombre_completo: e.target.value})}
                className="w-full px-6 py-4 rounded-xl border border-gray-100 bg-[#f8f9fa] outline-none focus:ring-2 focus:ring-[#4263eb] transition-all"
                placeholder="Ej. Juan Perez"
              />
            </div>
            <div className="space-y-2">
              <label className="text-[14px] font-black text-[#343a40] uppercase tracking-wider">No. Identificación</label>
              <input 
                type="text" required
                value={formData.no_documento}
                onChange={(e) => setFormData({...formData, no_documento: e.target.value})}
                className="w-full px-6 py-4 rounded-xl border border-gray-100 bg-[#f8f9fa] outline-none focus:ring-2 focus:ring-[#4263eb] transition-all"
                placeholder="Cédula de ciudadanía"
              />
            </div>
            <div className="space-y-2">
              <label className="text-[14px] font-black text-[#343a40] uppercase tracking-wider">Nombre de Usuario</label>
              <input 
                type="text" required
                value={formData.username}
                onChange={(e) => setFormData({...formData, username: e.target.value})}
                className="w-full px-6 py-4 rounded-xl border border-gray-100 bg-[#f8f9fa] outline-none focus:ring-2 focus:ring-[#4263eb] transition-all"
                placeholder="user123"
              />
            </div>
            <div className="space-y-2">
              <label className="text-[14px] font-black text-[#343a40] uppercase tracking-wider">Contraseña</label>
              <input 
                type="password" required
                minLength={6}
                value={formData.password}
                onChange={(e) => setFormData({...formData, password: e.target.value})}
                className="w-full px-6 py-4 rounded-xl border border-gray-100 bg-[#f8f9fa] outline-none focus:ring-2 focus:ring-[#4263eb] transition-all"
                placeholder="••••••••"
              />
            </div>
            <div className="space-y-2">
              <label className="text-[14px] font-black text-[#343a40] uppercase tracking-wider">
                Correo Electrónico
              </label>

              <input
                type="email"
                required
                value={formData.correo || ''}
                onChange={(e) =>
                  setFormData({
                    ...formData,
                    correo: e.target.value
                  })
                }
                className="w-full px-6 py-4 rounded-xl border border-gray-100 bg-[#f8f9fa] outline-none focus:ring-2 focus:ring-[#4263eb] transition-all"
                placeholder="usuario@email.com"
              />
            </div>

            <div className="space-y-2">
              <label className="text-[14px] font-black text-[#343a40] uppercase tracking-wider">
                Teléfono
              </label>

              <input
                type="tel"
                required
                value={formData.telefono || ''}
                onChange={(e) =>
                  setFormData({
                    ...formData,
                    telefono: e.target.value
                  })
                }
                className="w-full px-6 py-4 rounded-xl border border-gray-100 bg-[#f8f9fa] outline-none focus:ring-2 focus:ring-[#4263eb] transition-all"
                placeholder="Ej. 3001234567"
              />
            </div>


            <div className="space-y-2">
              <label className="text-[14px] font-black text-[#343a40] uppercase tracking-wider">Rol de Usuario</label>
              <select 
                value={formData.rol}
                onChange={(e) => setFormData({...formData, rol: e.target.value})}
                className="w-full px-6 py-4 rounded-xl border border-gray-100 bg-[#f8f9fa] outline-none focus:ring-2 focus:ring-[#4263eb] transition-all font-bold"
              >
                <option value="Vendedor">Vendedor (Cajero)</option>
                <option value="Administrador">Administrador</option>
                <option value="Dueño">Dueño</option>
              </select>
            </div>
          </div>
          <div className="pt-6">
            <button 
              type="submit"
              className="w-full bg-[#4263eb] text-white py-5 rounded-2xl font-black text-lg shadow-xl hover:bg-[#364fc7] transition-all active:scale-95"
            >
              Crear Cuenta de Usuario
            </button>
          </div>
        </form>
      </Modal>
    </div>
  );
};

export default Users;

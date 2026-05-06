import React, { useState, useEffect } from 'react';
import { auditoria } from '../api';

const Audit = () => {
  const [logs, setLogs] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadLogs();
  }, []);

  const loadLogs = async () => {
    try {
      const data = await auditoria.getLogs();
      setLogs(data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const getActionColor = (action) => {
    const a = action.toLowerCase();
    if (a.includes('inicio') || a.includes('login')) return 'text-blue-600';
    if (a.includes('cambio') || a.includes('ajuste')) return 'text-yellow-600';
    if (a.includes('cancelar')) return 'text-red-600';
    if (a.includes('crear')) return 'text-green-600';
    return 'text-gray-600';
  };

  return (
    <div className="space-y-10">
      <div>
        <h2 className="text-4xl font-extrabold text-[#1a1c23] mb-2">Registro de Auditoría</h2>
        <p className="text-lg text-gray-500">Trazabilidad completa de acciones, cambios y eventos críticos del sistema.</p>
      </div>

      <div className="bg-white p-10 rounded-[32px] shadow-sm border border-gray-100">
        <div className="overflow-hidden rounded-xl">
          <table className="w-full text-left">
            <thead className="bg-[#f8f9fa] border-b border-gray-100">
              <tr>
                <th className="px-6 py-5 font-bold text-[#343a40]">Fecha y Hora</th>
                <th className="px-6 py-5 font-bold text-[#343a40]">ID Usuario</th>
                <th className="px-6 py-5 font-bold text-[#343a40]">Acción</th>
                <th className="px-6 py-5 font-bold text-[#343a40]">Descripción / Detalle</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-100">
              {loading ? (
                <tr><td colSpan="4" className="px-6 py-20 text-center text-gray-400 font-medium">Consultando bitácora de auditoría...</td></tr>
              ) : logs.map((log) => (
                <tr key={log.id} className="hover:bg-gray-50 transition-colors text-sm">
                  <td className="px-6 py-4 font-medium text-gray-500">{new Date(log.fecha_auditoria).toLocaleString()}</td>
                  <td className="px-6 py-4 font-black text-[#1a1c23]">ID: {log.usuario_id || 'Sistema'}</td>
                  <td className={`px-6 py-4 font-black uppercase tracking-tighter ${getActionColor(log.accion)}`}>
                    {log.accion}
                  </td>
                  <td className="px-6 py-4 text-gray-600 max-w-xs truncate">{log.descripcion}</td>
                </tr>
              ))}
              {logs.length === 0 && !loading && (
                <tr><td colSpan="4" className="px-6 py-20 text-center text-gray-400 italic">No hay registros de auditoría aún.</td></tr>
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};

export default Audit;

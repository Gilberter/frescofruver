import React, { useState, useEffect } from 'react';
import { auth, reports, products } from '../api';

const Dashboard = () => {
  const [stats, setStats] = useState(null);
  const [lowStockCount, setLowStockCount] = useState(0);
  const [loading, setLoading] = useState(true);
  const currentUser = auth.getCurrentUser();
  const role = currentUser?.rol;
  const isAdmin = role === 'Administrador' || role === 'Dueño';

  useEffect(() => {
    loadDashboardData();
  }, []);

  const loadDashboardData = async () => {
    setLoading(true);
    try {
      // Correct call to openapi.json: reports.getLastMonth() returns a InformeConsolidado object
      const [reportData, allProducts] = await Promise.all([
        reports.getLastMonth(),
        products.getProducts()
      ]);
      setStats(reportData);
      setLowStockCount(allProducts.filter(p => p.stock_actual <= p.stock_minimo).length);
    } catch (err) {
      console.error('Error loading dashboard stats:', err);
    } finally {
      setLoading(false);
    }
  };

  if (loading) return (
    <div className="p-20 flex flex-col items-center justify-center space-y-4">
      <div className="w-12 h-12 border-4 border-[#4263eb] border-t-transparent rounded-full animate-spin"></div>
      <p className="text-gray-400 font-black uppercase tracking-widest text-xs">Sincronizando Inteligencia de Negocio...</p>
    </div>
  );

  const resumen = stats?.resumen;
  const topProducts = stats?.detalles_productos_top_5 || [];

  return (
    <div className="space-y-10">
      <div className="flex justify-between items-end">
        <div>
          <h2 className="text-4xl font-black text-[#1a1c23] tracking-tight">
            {isAdmin ? 'Análisis de Rendimiento' : 'Mi Actividad'}
          </h2>
          <p className="text-gray-500 mt-2">Bienvenido de nuevo, <span className="font-bold text-[#4263eb]">{currentUser?.username}</span>. Estos son los resultados del último mes.</p>
        </div>
        <div className="bg-white px-6 py-3 rounded-2xl shadow-sm border border-gray-100 flex items-center gap-3">
          <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
          <span className="text-xs font-black text-gray-400 uppercase tracking-widest">Servidor en Línea</span>
        </div>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
        {isAdmin ? (
          <>
            <StatCard label="Ventas Totales" value={`${Math.round(resumen?.total_ingresos || 0).toLocaleString()}`} color="bg-blue-600" />
            <StatCard label="Stock Crítico" value={`${lowStockCount}`} color="bg-red-500" />
            <StatCard label="Ganancia Bruta" value={`$${resumen?.ganancia_bruta?.toLocaleString() || 0}`} color="bg-green-600" />
            <StatCard label="Margen Operativo" value={`${resumen?.margen_porcentaje?.toFixed(1) || 0}%`} color="bg-purple-600" />
          </>
        ) : (
          <>
            <StatCard label="Ventas Realizadas" value={`${resumen?.total_ventas || 0}`} color="bg-blue-600" />
            <StatCard label="Mi Rendimiento" value={`$${Math.round(resumen?.total_ingresos || 0).toLocaleString()}`} color="bg-green-600" />
          </>
        )}
      </div>

      {isAdmin && (
        <div className="grid grid-cols-1 gap-8">
          {/* Top Products Table */}
          <div className="bg-white p-10 rounded-[40px] shadow-sm border border-gray-100">
            <div className="flex justify-between items-center mb-8">
              <h3 className="text-2xl font-black text-[#1a1c23] tracking-tight">Top 5 Productos por Ganancia</h3>
              <span className="text-xs font-black text-[#4263eb] bg-blue-50 px-4 py-2 rounded-full uppercase tracking-widest">Optimización de Inventario</span>
            </div>
            
            <div className="overflow-hidden rounded-2xl">
              <table className="w-full text-left">
                <thead className="bg-[#f8f9fa]">
                  <tr>
                    <th className="px-6 py-5 font-black text-[#343a40] text-xs uppercase tracking-widest">Producto</th>
                    <th className="px-6 py-5 font-black text-[#343a40] text-xs uppercase tracking-widest text-center">Vendido</th>
                    <th className="px-6 py-5 font-black text-[#343a40] text-xs uppercase tracking-widest text-right">Ganancia</th>
                    <th className="px-6 py-5 font-black text-[#343a40] text-xs uppercase tracking-widest text-center">Stock</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-gray-100">
                  {topProducts.length > 0 ? topProducts.map((p, idx) => (
                    <tr key={idx} className="hover:bg-gray-50 transition-colors">
                      <td className="px-6 py-5">
                        <div className="flex flex-col">
                          <span className="font-bold text-[#1a1c23]">{p.nombre_producto}</span>
                          <span className="text-[10px] text-gray-400 font-black uppercase">Frescofruver Premium</span>
                        </div>
                      </td>
                      <td className="px-6 py-5 text-center font-bold text-gray-600">{p.cantidad_vendida}</td>
                      <td className="px-6 py-5 text-right font-black text-green-600">${p.ganancia.toLocaleString()}</td>
                      <td className="px-6 py-5 text-center font-black text-[#1a1c23]">{p.stock_actual}</td>
                    </tr>
                  )) : (
                    <tr><td colSpan="4" className="px-6 py-20 text-center text-gray-400 italic">No hay datos de rendimiento registrados para el período seleccionado.</td></tr>
                  )}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

const StatCard = ({ label, value, color }) => (
  <div className="bg-white p-10 rounded-[40px] shadow-sm border border-gray-100 flex flex-col justify-between overflow-hidden relative group transition-all hover:shadow-xl hover:-translate-y-1">
    <div className={`absolute top-0 left-0 w-2 h-full ${color}`}></div>
    <span className="text-[11px] font-black text-gray-400 tracking-widest uppercase mb-4">{label}</span>
    <p className="text-4xl font-black text-[#1a1c23] tracking-tighter">{value}</p>
    <div className={`w-12 h-1 rounded-full mt-6 opacity-20 ${color}`}></div>
  </div>
);

export default Dashboard;

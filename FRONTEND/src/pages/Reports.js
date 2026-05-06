import React, { useState, useEffect, useCallback } from 'react';
import { reports, sales } from '../api';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import Modal from '../components/Modal';

const Reports = () => {
  const [ventasData, setVentasData] = useState(null);
  const [comprasData, setComprasData] = useState(null);
  const [consolidatedData, setConsolidatedData] = useState(null);
  const [loading, setLoading] = useState(true);
  
  // Modal states
  const [selectedVenta, setSelectedVenta] = useState(null);
  const [isCancelModalOpen, setIsCancelModalOpen] = useState(false);
  const [isCanceling, setIsCanceling] = useState(false);

  const [dateRange, setDateRange] = useState({
    start: new Date(new Date().setMonth(new Date().getMonth() - 5)).toISOString().split('T')[0],
    end: new Date().toISOString().split('T')[0]
  });

  const getMonthlyChartData = (ventas) => {
    if (!ventas) return [];
    const months = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'];
    const grouped = {};
    ventas.forEach(v => {
      const date = new Date(v.fecha_venta);
      const monthStr = months[date.getMonth()];
      if (!grouped[monthStr]) grouped[monthStr] = 0;
      grouped[monthStr] += v.total;
    });
    
    // Convert to array and preserve original chronological order (assuming dates in data are roughly chronological)
    // A better approach for charts is strict sorting by month index, but we need year context if it spans years.
    // For simplicity, we just sort by month index
    return Object.keys(grouped).map(k => ({
      name: k,
      total: grouped[k]
    })).sort((a, b) => months.indexOf(a.name) - months.indexOf(b.name));
  };

  const loadReports = useCallback(async () => {
    setLoading(true);
    try {
      const [vData, cData, consData] = await Promise.all([
        reports.getVentasReport(dateRange.start, dateRange.end),
        reports.getComprasReport(dateRange.start, dateRange.end),
        reports.getConsolidated(dateRange.start, dateRange.end)
      ]);
      setVentasData(vData);
      setComprasData(cData);
      setConsolidatedData(consData);
    } catch (err) {
      console.error('Error loading reports:', err);
    } finally {
      setLoading(false);
    }
  }, [dateRange]);

  useEffect(() => {
    loadReports();
  }, [loadReports]);

  const loadLastMonth = async () => {
    setLoading(true);
    try {
      const data = await reports.getLastMonth();
      setConsolidatedData(data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const openCancelModal = (venta) => {
    setSelectedVenta(venta);
    setIsCancelModalOpen(true);
  };

  const closeCancelModal = () => {
    setSelectedVenta(null);
    setIsCancelModalOpen(false);
  };

  const handleCancelSale = async () => {
    if (!selectedVenta) return;
    setIsCanceling(true);
    try {
      // Assuming numero_factura contains the ID, e.g. "F-1" or "#V-1024"
      const ventaId = selectedVenta.numero_factura.replace(/\D/g, '');
      await sales.cancelSale(ventaId);
      closeCancelModal();
      loadReports(); // Refresh data
    } catch (err) {
      console.error('Error al cancelar la venta:', err);
      alert('Hubo un error al cancelar la venta. Revisa la consola para más detalles.');
    } finally {
      setIsCanceling(false);
    }
  };

  const exportToCSV = (data, filename) => {
    if (!data || data.length === 0) return;
    const headers = Object.keys(data[0]).join(',');
    const rows = data.map(row => 
      Object.values(row).map(value => `"${value}"`).join(',')
    ).join('\n');
    const csvContent = "data:text/csv;charset=utf-8," + headers + "\n" + rows;
    const encodedUri = encodeURI(csvContent);
    const link = document.createElement("a");
    link.setAttribute("href", encodedUri);
    link.setAttribute("download", `${filename}.csv`);
    document.body.appendChild(link);
    link.click();
  };

  if (loading && !consolidatedData) return (
    <div className="p-20 flex flex-col items-center justify-center space-y-4">
      <div className="w-12 h-12 border-4 border-[#4263eb] border-t-transparent rounded-full animate-spin"></div>
      <p className="text-gray-400 font-black uppercase tracking-widest text-xs">Sincronizando Inteligencia de Negocio...</p>
    </div>
  );

  const resumen = consolidatedData?.resumen;

  return (
    <div className="space-y-10">
      <div className="flex flex-col lg:flex-row justify-between items-start lg:items-end gap-6">
        <div>
          <h2 className="text-4xl font-black text-[#1a1c23] tracking-tight">Inteligencia de Negocio</h2>
          <p className="text-lg text-gray-500 mt-2">Visión consolidada y analítica de rendimientos.</p>
        </div>
        
        <div className="flex flex-wrap gap-4 bg-white p-6 rounded-[32px] shadow-sm border border-gray-100 items-end">
          <div className="flex flex-col gap-1">
            <span className="text-[10px] font-black text-gray-400 uppercase tracking-widest ml-1">Desde</span>
            <input 
              type="date" 
              value={dateRange.start}
              onChange={(e) => setDateRange({...dateRange, start: e.target.value})}
              className="px-6 py-3 rounded-xl border border-gray-100 bg-[#f8f9fa] font-bold outline-none focus:ring-2 focus:ring-[#4263eb]"
            />
          </div>
          <div className="flex flex-col gap-1">
            <span className="text-[10px] font-black text-gray-400 uppercase tracking-widest ml-1">Hasta</span>
            <input 
              type="date" 
              value={dateRange.end}
              onChange={(e) => setDateRange({...dateRange, end: e.target.value})}
              className="px-6 py-3 rounded-xl border border-gray-100 bg-[#f8f9fa] font-bold outline-none focus:ring-2 focus:ring-[#4263eb]"
            />
          </div>
          <button 
            onClick={loadLastMonth}
            className="px-6 py-3 rounded-xl bg-gray-100 font-black text-[10px] uppercase tracking-widest hover:bg-gray-200 transition-all"
          >
            Último Mes
          </button>
        </div>
      </div>

      {/* Financial Health Header */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <div className="bg-[#1a1c23] p-8 rounded-[32px] text-white">
          <p className="text-[10px] font-black opacity-40 uppercase tracking-widest mb-2">Ventas Totales</p>
          <p className="text-3xl font-black tracking-tighter">{Math.round(resumen?.total_ventas || 0).toLocaleString()}</p>
        </div>
        <div className="bg-white p-8 rounded-[32px] border border-gray-100">
          <p className="text-[10px] font-black text-gray-400 uppercase tracking-widest mb-2">Costo de Inversión</p>
          <p className="text-3xl font-black text-[#f03e3e] tracking-tighter">${resumen?.total_costos?.toLocaleString() || 0}</p>
        </div>
        <div className="bg-[#f8f9fa] p-8 rounded-[32px]">
          <p className="text-[10px] font-black text-gray-400 uppercase tracking-widest mb-2">Ganancia Bruta</p>
          <p className="text-3xl font-black text-[#40c057] tracking-tighter">${resumen?.ganancia_bruta?.toLocaleString() || 0}</p>
        </div>
        <div className="bg-[#4263eb] p-8 rounded-[32px] text-white">
          <p className="text-[10px] font-black opacity-60 uppercase tracking-widest mb-2">Margen de Ganancia</p>
          <p className="text-3xl font-black tracking-tighter">{resumen?.margen_porcentaje?.toFixed(1) || 0}%</p>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Sales Chart (Full/Half Width depending on layout, here left column) */}
        <div className="lg:col-span-1 bg-white p-10 rounded-[40px] shadow-sm border border-gray-100 flex flex-col">
          <h3 className="text-xl font-black text-[#4263eb] tracking-tight mb-8">Estadísticas de Ventas Mensuales</h3>
          <div className="flex-grow w-full min-h-[300px]">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={getMonthlyChartData(ventasData?.ventas)} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
                <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#f0f0f0" />
                <XAxis dataKey="name" axisLine={false} tickLine={false} tick={{fill: '#868e96', fontSize: 12}} dy={10} />
                <YAxis tickFormatter={(val) => `$${val}`} axisLine={false} tickLine={false} tick={{fill: '#868e96', fontSize: 12}} />
                <Tooltip cursor={{fill: '#f8f9fa'}} contentStyle={{borderRadius: '12px', border: 'none', boxShadow: '0 4px 6px -1px rgb(0 0 0 / 0.1)'}} formatter={(value) => [`$${value.toLocaleString()}`, 'Total']} />
                <Bar dataKey="total" fill="#4263eb" radius={[4, 4, 0, 0]} maxBarSize={60} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Sales Table (Right column) */}
        <div className="lg:col-span-1 bg-white p-10 rounded-[40px] shadow-sm border border-gray-100">
          <div className="flex justify-between items-center mb-8">
            <h3 className="text-xl font-black text-[#4263eb] tracking-tight">Informe Tabular: Ventas Recientes</h3>
            <button onClick={() => exportToCSV(ventasData?.ventas, 'ventas')} className="text-[10px] font-black text-[#4263eb] hover:underline uppercase">Exportar CSV</button>
          </div>
          <div className="overflow-hidden">
            <table className="w-full text-left">
              <thead>
                <tr className="border-b border-gray-100">
                  <th className="py-4 text-[#1a1c23] font-black text-sm">ID Venta</th>
                  <th className="py-4 text-[#1a1c23] font-black text-sm">Fecha</th>
                  <th className="py-4 text-[#1a1c23] font-black text-sm">Total</th>
                  <th className="py-4 text-[#1a1c23] font-black text-sm text-center">Ver Detalle</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-50">
                {ventasData?.ventas?.slice()?.sort((a, b) => new Date(b.fecha_venta) - new Date(a.fecha_venta))?.slice(0, 5).map((v, i) => (
                  <tr key={i} className="hover:bg-[#f8f9fa] transition-colors">
                    <td className="py-5 text-sm text-gray-600">#{v.numero_factura}</td>
                    <td className="py-5 text-sm text-gray-600">{v.fecha_venta.split('T')[0]}</td>
                    <td className="py-5 text-sm text-gray-600">${v.total.toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2})}</td>
                    <td className="py-5 text-center">
                      <button 
                        onClick={() => openCancelModal(v)}
                        className="bg-[#4263eb] text-white px-4 py-1.5 rounded-lg text-xs font-bold hover:bg-[#3b5bdb] transition-colors shadow-sm"
                      >
                        Ver
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        {/* Optional: Add a Top Products / Purchases breakdown row here if needed */}
        <div className="lg:col-span-2 grid grid-cols-1 md:grid-cols-2 gap-8 mt-4">
          <div className="bg-white p-10 rounded-[40px] shadow-sm border border-gray-100">
            <h3 className="text-xl font-black text-[#1a1c23] tracking-tight mb-8">Top 5 Rentabilidad</h3>
            <div className="space-y-6">
              {consolidatedData?.detalles_productos_top_5?.map((p, i) => (
                <div key={i} className="relative pt-2">
                  <div className="flex justify-between text-xs font-black mb-2">
                    <span className="text-gray-600 uppercase tracking-tighter">{p.nombre_producto}</span>
                    <span className="text-[#40c057]">+${p.ganancia.toLocaleString()}</span>
                  </div>
                  <div className="w-full h-1.5 bg-gray-100 rounded-full overflow-hidden">
                    <div 
                      className="h-full bg-[#40c057] rounded-full" 
                      style={{ width: `${Math.min(100, (p.ganancia / (resumen?.ganancia_bruta || 1)) * 500)}%` }}
                    ></div>
                  </div>
                </div>
              ))}
            </div>
          </div>
          
          <div className="bg-white p-10 rounded-[40px] shadow-sm border border-gray-100">
            <div className="flex justify-between items-center mb-8">
              <h3 className="text-xl font-black text-[#1a1c23] tracking-tight">Historial Compras</h3>
            </div>
            <div className="space-y-4">
              {comprasData?.compras?.slice()?.sort((a, b) => new Date(b.fecha_orden) - new Date(a.fecha_orden))?.slice(0, 5).map((c, i) => (
                <div key={i} className="flex justify-between items-center p-4 bg-[#f8f9fa] rounded-2xl">
                  <div>
                    <p className="text-xs font-black text-[#1a1c23]">{c.numero_orden}</p>
                    <p className="text-[10px] text-gray-400 font-bold uppercase">{c.proveedor}</p>
                  </div>
                  <p className="text-sm font-black text-[#f03e3e]">${c.total_orden.toLocaleString()}</p>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>

      <Modal isOpen={isCancelModalOpen} onClose={closeCancelModal} title="Detalle de Venta">
        {selectedVenta && (
          <div className="space-y-6">
            <div className="bg-[#f8f9fa] p-6 rounded-2xl">
              <h4 className="text-lg font-black text-[#1a1c23] mb-4">Información de Factura</h4>
              <div className="grid grid-cols-2 gap-4 text-sm">
                <div>
                  <p className="text-gray-500 font-bold">Número de Factura</p>
                  <p className="font-black text-[#1a1c23]">{selectedVenta.numero_factura}</p>
                </div>
                <div>
                  <p className="text-gray-500 font-bold">Fecha</p>
                  <p className="font-black text-[#1a1c23]">{new Date(selectedVenta.fecha_venta).toLocaleDateString()}</p>
                </div>
                <div>
                  <p className="text-gray-500 font-bold">Cliente</p>
                  <p className="font-black text-[#1a1c23]">{selectedVenta.cliente || 'Consumidor Final'}</p>
                </div>
                <div>
                  <p className="text-gray-500 font-bold">Total</p>
                  <p className="font-black text-[#40c057]">${selectedVenta.total.toLocaleString(undefined, {minimumFractionDigits: 2})}</p>
                </div>
              </div>
            </div>

            <div className="border-t border-gray-100 pt-6">
              <p className="text-sm text-gray-500 mb-4 font-bold">Acciones Disponibles</p>
              <div className="flex justify-end gap-4">
                <button 
                  onClick={closeCancelModal}
                  className="px-6 py-3 rounded-xl border border-gray-200 text-gray-600 font-bold hover:bg-gray-50 transition-colors"
                >
                  Cerrar
                </button>
                <button 
                  onClick={handleCancelSale}
                  disabled={isCanceling}
                  className="px-6 py-3 rounded-xl bg-red-500 text-white font-bold hover:bg-red-600 transition-colors disabled:opacity-50 flex items-center gap-2"
                >
                  {isCanceling ? (
                    <>
                      <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
                      Cancelando...
                    </>
                  ) : (
                    'Cancelar Venta'
                  )}
                </button>
              </div>
            </div>
          </div>
        )}
      </Modal>
    </div>
  );
};

export default Reports;

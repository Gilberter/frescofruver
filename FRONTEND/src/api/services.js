import apiClient from './apiClient';

export const clients = {
  getClients: () => apiClient.get('/clientes/').then(res => res.data),
  getClient: (id) => apiClient.get(`/clientes/${id}`).then(res => res.data),
  createClient: (data) => apiClient.post('/clientes/', data).then(res => res.data),
  updateClient: (id, data) => apiClient.patch(`/clientes/${id}`, data).then(res => res.data),
};

export const providers = {
  getProviders: () => apiClient.get('/proveedores/').then(res => res.data),
  getProvider: (id) => apiClient.get(`/proveedores/${id}`).then(res => res.data),
  createProvider: (data) => apiClient.post('/proveedores/', data).then(res => res.data),
  updateProvider: (id, data) => apiClient.patch(`/proveedores/${id}`, data).then(res => res.data),
};

export const users = {
  getUsers: () => apiClient.get('/usuarios/').then(res => res.data),
  createUser: (data) => apiClient.post('/usuarios/', data).then(res => res.data),
  updateUser: (id, data) => apiClient.patch(`/usuarios/${id}`, data).then(res => res.data),
  deactivateUser: (id) => apiClient.delete(`/usuarios/${id}/desactivar`).then(res => res.data),
};

export const sales = {
  getSales: () => apiClient.get('/ventas/').then(res => res.data),
  createSale: (data) => apiClient.post('/ventas/', data).then(res => res.data),
  cancelSale: (id) => apiClient.post(`/ventas/${id}/cancelar`).then(res => res.data),
};

export const reports = {
  getConsolidated: (start, end) => apiClient.get('/informes/consolidado', { params: { fecha_inicio: start, fecha_fin: end } }).then(res => res.data),
  getLastMonth: () => apiClient.get('/informes/ultimo-mes').then(res => res.data),
  getVentasReport: (start, end) => apiClient.get('/informes/ventas', { params: { fecha_inicio: start, fecha_fin: end } }).then(res => res.data),
  getComprasReport: (start, end) => apiClient.get('/informes/compras', { params: { fecha_inicio: start, fecha_fin: end } }).then(res => res.data),
  getLastMonth: () => apiClient.get('/dashboard/ultimo-mes').then(res => res.data),
};
export const purchases = {
  getPurchases: () => apiClient.get('/ordenes-compra/').then(res => res.data),
  getPurchase: (id) => apiClient.get(`/ordenes-compra/${id}`).then(res => res.data),
  createPurchase: (data) => apiClient.post('/ordenes-compra/', data).then(res => res.data),
  receivePurchase: (id) => apiClient.post(`/ordenes-compra/${id}/recibir`).then(res => res.data),
  cancelPurchase: (id) => apiClient.post(`/ordenes-compra/${id}/cancelar`).then(res => res.data),
};
export const auditoria = {
  getLogs: (limit = 100) => apiClient.get('/auditoria/', { params: { limit } }).then(res => res.data),
};

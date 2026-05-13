import apiClient from './apiClient';

export const getProducts = async (categoria = null) => {

  const response = await apiClient.get('/productos', {
    params: categoria ? { categoria } : {}
  });

  return response.data;
};

export const getLowStockProducts = async () => {

  const response = await apiClient.get('/productos/bajo-stock');

  return response.data;
};

export const getProductById = async (id) => {

  const response = await apiClient.get(`/productos/${id}`);

  return response.data;
};

export const createProduct = async (data) => {

  const response = await apiClient.post('/productos', data);

  return response.data;
};

export const updateProduct = async (id, data) => {

  const response = await apiClient.patch(`/productos/${id}`, data);

  return response.data;
};

// export const adjustInventory = async (id, data) => {

//   const response = await apiClient.post(
//     `/productos/${id}/ajuste`,
//     data
//   );

//   return response.data;
// };


export const dataMovement = async (id,data) => {
  const response = await apiClient.post(
    `/productos/${id}/ajuste`,
    data
  );
  return response.data;
}

export const getMovements = async (id) => {

  const response = await apiClient.get(
    `/productos/${id}/movimientos`
  );

  return response.data;
};
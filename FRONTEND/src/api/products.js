import apiClient from './apiClient';

/**
 * Fetch all products from the inventory.
 * @param {string} [categoria] Optional category filter.
 * @returns {Promise<Array>}
 */
export const getProducts = async (categoria = null) => {
  const params = categoria ? { categoria } : {};
  const response = await apiClient.get('/productos/', { params });
  return response.data;
};

/**
 * Fetch a single product by ID.
 * @param {number} productId 
 * @returns {Promise<Object>}
 */
export const getProductById = async (productId) => {
  const response = await apiClient.get(`/productos/${productId}`);
  return response.data;
};

/**
 * Create a new product.
 * @param {Object} productData 
 * @returns {Promise<Object>}
 */
export const createProduct = async (productData) => {
  const response = await apiClient.post('/productos/', productData);
  return response.data;
};

/**
 * Update an existing product.
 * @param {number} productId 
 * @param {Object} updateData 
 * @returns {Promise<Object>}
 */
export const updateProduct = async (productId, updateData) => {
  const response = await apiClient.patch(`/productos/${productId}`, updateData);
  return response.data;
};

/**
 * Fetch products with low stock.
 * @returns {Promise<Array>}
 */
export const getLowStockProducts = async () => {
  const response = await apiClient.get('/productos/bajo-stock');
  return response.data;
};
/**
 * Perform manual inventory adjustment (RF-03.4).
 * @param {number} productId 
 * @param {Object} adjustmentData { cantidad_ajuste: number, motivo: string }
 * @returns {Promise<Object>}
 */
export const adjustInventory = async (productId, adjustmentData) => {
  const response = await apiClient.post(`/productos/${productId}/ajuste`, adjustmentData);
  return response.data;
};

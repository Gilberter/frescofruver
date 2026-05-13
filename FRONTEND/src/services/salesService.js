export const salesService = {
  buildSalePayload(cart, clientId) {
    return {
      cliente_id: parseInt(clientId),
      detalles: cart.map(item => ({
        producto_id: item.producto_id,
        cantidad: item.cantidad
      }))
    };
  }
};
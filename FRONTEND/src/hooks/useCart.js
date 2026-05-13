import { useMemo, useState } from 'react';
import { IVA } from '../services/constants';

export const useCart = () => {
  const [cart, setCart] = useState([]);

  const addProduct = (product) => {
    setCart(prev => {
      const existing = prev.find(i => i.producto_id === product.id);

      if (existing) {
        if (existing.cantidad >= product.stock_actual) {
          return prev;
        }

        return prev.map(i =>
          i.producto_id === product.id
            ? { ...i, cantidad: i.cantidad + 1 }
            : i
        );
      }

      return [
        ...prev,
        {
          producto_id: product.id,
          nombre: product.nombre,
          precio: product.precio_venta,
          stock: product.stock_actual,
          unidad_medida: product.unidad_medida,
          cantidad: 1
        }
      ];
    });
  };

  const removeProduct = (productoId) => {
    setCart(prev => prev.filter(i => i.producto_id !== productoId));
  };

  const increaseQuantity = (productoId) => {
    setCart(prev =>
      prev.map(item => {
        if (item.producto_id !== productoId) return item;

        if (item.cantidad >= item.stock) return item;

        return {
          ...item,
          cantidad: item.cantidad + 1
        };
      })
    );
  };

  const decreaseQuantity = (productoId) => {
    setCart(prev =>
      prev
        .map(item =>
          item.producto_id === productoId
            ? { ...item, cantidad: item.cantidad - 1 }
            : item
        )
        .filter(item => item.cantidad > 0)
    );
  };

  const clearCart = () => setCart([]);

  const subtotal = useMemo(() => {
    return cart.reduce((acc, item) => {
      return acc + item.precio * item.cantidad;
    }, 0);
  }, [cart]);

  const iva = useMemo(() => subtotal * IVA, [subtotal]);

  const total = useMemo(() => subtotal + iva, [subtotal, iva]);

  return {
    cart,
    addProduct,
    removeProduct,
    increaseQuantity,
    decreaseQuantity,
    clearCart,
    subtotal,
    iva,
    total
  };
};
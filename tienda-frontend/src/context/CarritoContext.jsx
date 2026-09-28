import { createContext, useContext, useState, useEffect } from 'react';

const CarritoContext = createContext();

export const useCarrito = () => {
  const context = useContext(CarritoContext);
  if (!context) {
    throw new Error('useCarrito debe ser usado dentro de un CarritoProvider');
  }
  return context;
};

export const CarritoProvider = ({ children }) => {
  // 1.2 Inicializar leyendo de localStorage con useState y una función envuelta en try/catch
  const [items, setItems] = useState(() => {
    try {
      const guardado = localStorage.getItem('carrito');
      return guardado ? JSON.parse(guardado) : [];
    } catch (error) {
      console.error('JSON roto o inválido en localStorage (carrito). Iniciando con carrito vacío:', error);
      return [];
    }
  });

  // 1.3 useEffect que guarda el carrito en localStorage cada vez que cambie
  useEffect(() => {
    try {
      localStorage.setItem('carrito', JSON.stringify(items));
    } catch (error) {
      console.error('Error al guardar el carrito en localStorage:', error);
    }
  }, [items]);

  // 1.4 agregar(producto, cantidad): si ya está en el carrito suma cantidad, no agrega fila repetida
  const agregar = (producto, cantidad = 1) => {
    const idProducto = Number(producto.producto_id ?? producto.id);
    const cant = Number(cantidad) > 0 ? Number(cantidad) : 1;

    setItems((prevItems) => {
      const index = prevItems.findIndex(
        (item) => Number(item.producto_id ?? item.id) === idProducto
      );

      if (index !== -1) {
        return prevItems.map((item, i) =>
          i === index
            ? { ...item, cantidad: item.cantidad + cant }
            : item
        );
      }

      return [
        ...prevItems,
        {
          ...producto,
          id: idProducto,
          producto_id: idProducto,
          cantidad: cant,
        },
      ];
    });
  };

  // 1.5 quitar(producto_id)
  const quitar = (producto_id) => {
    const targetId = Number(producto_id);
    setItems((prevItems) =>
      prevItems.filter((item) => Number(item.producto_id ?? item.id) !== targetId)
    );
  };

  // 1.5 vaciar()
  const vaciar = () => {
    setItems([]);
  };

  // 1.5 total calculado con reduce
  const total = items.reduce((acc, item) => {
    const precio = Number(item.precio_final ?? item.precio ?? 0);
    return acc + precio * item.cantidad;
  }, 0);

  // Cantidad total de productos en unidades
  const cantidadTotal = items.reduce((acc, item) => acc + item.cantidad, 0);

  const value = {
    items,
    agregar,
    quitar,
    vaciar,
    total,
    cantidadTotal,
    // Alias de compatibilidad
    cart: items,
    agregarAlCarrito: agregar,
    quitarDelCarrito: quitar,
    vaciarCarrito: vaciar,
    precioTotal: total,
  };

  return (
    <CarritoContext.Provider value={value}>
      {children}
    </CarritoContext.Provider>
  );
};

export default CarritoContext;

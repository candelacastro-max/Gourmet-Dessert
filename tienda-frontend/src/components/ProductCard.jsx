import { useState } from 'react';
import { useCarrito } from '../context/CarritoContext';

const ProductCard = ({ producto }) => {
  const { nombre, precio_final, precio, stock, cuotas_cantidad, cuotas_valor, garantia_meses } = producto;
  const { agregar } = useCarrito();
  const [agregado, setAgregado] = useState(false);

  const precioMostrar = Number(precio_final || precio || 0);

  const handleAddToCart = () => {
    agregar(producto, 1);
    setAgregado(true);
    setTimeout(() => setAgregado(false), 1200);
  };

  const sinStock = stock <= 0;

  return (
    <div className="product-card">
      <div className="product-card-top">
        <h3>{nombre}</h3>
        <span className={`stock-badge ${sinStock ? 'sin-stock' : 'con-stock'}`}>
          {sinStock ? 'Sin stock' : `${stock} disponibles`}
        </span>
      </div>

      <p className="precio">${precioMostrar.toLocaleString('es-AR')}</p>

      {cuotas_cantidad > 1 && cuotas_valor && (
        <p className="cuotas">
          {cuotas_cantidad} cuotas de ${Number(cuotas_valor).toLocaleString('es-AR')}
        </p>
      )}

      <p className="garantia">
        Garantía: {garantia_meses > 0 ? `${garantia_meses} meses` : 'Sin garantía'}
      </p>

      <button
        onClick={handleAddToCart}
        disabled={sinStock}
        className={`btn-add-cart ${agregado ? 'btn-agregado' : ''}`}
      >
        {sinStock ? 'Agotado' : agregado ? '✓ ¡Agregado!' : 'Agregar al carrito'}
      </button>
    </div>
  );
};

export default ProductCard;

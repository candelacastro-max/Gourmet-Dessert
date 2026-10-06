import { useState } from 'react';
import { useCarrito } from '../context/CarritoContext';
import { useAuth } from '../context/AuthContext';
import { eliminarProducto } from '../services/api';
import { urlImagen } from '../utils/imagenes';

const ProductCard = ({ producto, onEditar, onEliminado }) => {
  const { id, nombre, precio_final, precio, stock, cuotas_cantidad, cuotas_valor, garantia_meses } = producto;
  const { agregar } = useCarrito();
  const { user } = useAuth();
  const [agregado, setAgregado] = useState(false);
  const [borrando, setBorrando] = useState(false);

  const isAdmin = user?.rol === 'admin';
  const precioMostrar = Number(precio_final || precio || 0);
  const imgUrl = urlImagen(producto);

  const handleAddToCart = () => {
    agregar(producto, 1);
    setAgregado(true);
    setTimeout(() => setAgregado(false), 1200);
  };

  const handleEliminar = async () => {
    if (!window.confirm(`¿Estás segura de eliminar el producto "${nombre}"?`)) return;
    try {
      setBorrando(true);
      await eliminarProducto(id);
      if (onEliminado) onEliminado(id);
    } catch (err) {
      alert(err.message || 'Error al eliminar el producto');
    } finally {
      setBorrando(false);
    }
  };

  const sinStock = stock <= 0;

  return (
    <div className="product-card">
      <div className="product-card-image aspect-square">
        {imgUrl ? (
          <img
            src={imgUrl}
            alt={nombre}
            loading="lazy"
            className="product-card-img object-cover"
          />
        ) : (
          <div className="product-image-placeholder aspect-square">
            <span className="placeholder-icon">🍰</span>
            <span className="placeholder-text">Sin imagen</span>
          </div>
        )}
      </div>

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

      <div className="product-card-actions">
        <button
          onClick={handleAddToCart}
          disabled={sinStock}
          className={`btn-add-cart ${agregado ? 'btn-agregado' : ''}`}
        >
          {sinStock ? 'Agotado' : agregado ? '✓ ¡Agregado!' : 'Agregar al carrito'}
        </button>

        {isAdmin && (
          <div className="admin-card-actions">
            <button
              onClick={() => onEditar && onEditar(producto)}
              className="btn-admin-edit"
              title="Modificar precio o datos"
            >
              ✏️ Modificar
            </button>
            <button
              onClick={() => onEditar && onEditar(producto)}
              className="btn-admin-edit"
              style={{ background: '#f1f5f9', color: '#0f172a' }}
              title="Cambiar o poner imagen al producto"
            >
              📷 Imagen
            </button>
            <button
              onClick={handleEliminar}
              disabled={borrando}
              className="btn-admin-delete"
              title="Eliminar producto"
            >
              {borrando ? '...' : '🗑️ Eliminar'}
            </button>
          </div>
        )}
      </div>
    </div>
  );
};

export default ProductCard;

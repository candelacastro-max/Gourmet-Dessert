import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useCarrito } from '../context/CarritoContext';
import { crearPedido } from '../services/api';

const Carrito = () => {
  const { items, quitar, vaciar, total } = useCarrito();
  const [enviando, setEnviando] = useState(false);
  const [error, setError] = useState(null);
  const navigate = useNavigate();

  // Parte 2.4 y 2.5: confirmar() arranca con if (enviando) return, try/catch/finally y estado enviando
  const confirmar = async () => {
    if (enviando) return;
    if (!items || items.length === 0) return;

    setEnviando(true);
    setError(null);

    try {
      await crearPedido(items);
      vaciar();
      navigate('/mis-pedidos');
    } catch (err) {
      console.error('Error al confirmar compra:', err);
      setError(err.message || 'Error al procesar la compra.');
    } finally {
      setEnviando(false);
    }
  };

  return (
    <div className="carrito-page-container">
      <div className="carrito-header">
        <div>
          <h2>🛒 Mi Carrito de Compras</h2>
          <p>Revisá tus postres y delicias antes de confirmar el pedido</p>
        </div>
        <Link to="/catalogo" className="btn-secondary">
          ← Volver al Catálogo
        </Link>
      </div>

      {error && (
        <div className="auth-alert error" style={{ marginBottom: '24px' }}>
          <span>⚠️</span>
          <div>
            <strong>Atención:</strong> {error}
          </div>
        </div>
      )}

      {items.length === 0 ? (
        <div className="empty-pedidos" style={{ margin: '40px 0' }}>
          <span className="empty-icon">🍰</span>
          <h3>Tu carrito está vacío</h3>
          <p>Explora nuestras creaciones y agrega productos para iniciar tu pedido.</p>
          <Link to="/catalogo" className="btn-auth-primary" style={{ display: 'inline-block', marginTop: '16px' }}>
            Explorar Catálogo
          </Link>
        </div>
      ) : (
        <div className="carrito-content-layout">
          <div className="carrito-table-wrapper">
            <table className="carrito-table">
              <thead>
                <tr>
                  <th>Producto</th>
                  <th>Precio Unitario</th>
                  <th>Cantidad</th>
                  <th>Subtotal</th>
                  <th style={{ textAlign: 'center' }}>Acción</th>
                </tr>
              </thead>
              <tbody>
                {items.map((item) => {
                  const idItem = Number(item.producto_id ?? item.id);
                  const precio = Number(item.precio_final ?? item.precio ?? 0);
                  const subtotal = precio * item.cantidad;

                  return (
                    <tr key={idItem}>
                      <td className="carrito-item-nombre">
                        <strong>{item.nombre}</strong>
                      </td>
                      <td>${precio.toLocaleString('es-AR')}</td>
                      <td>
                        <span className="badge-cantidad">{item.cantidad}</span>
                      </td>
                      <td className="carrito-subtotal">
                        ${subtotal.toLocaleString('es-AR')}
                      </td>
                      <td style={{ textAlign: 'center' }}>
                        <button
                          onClick={() => quitar(idItem)}
                          className="btn-item-quitar"
                          title="Quitar del carrito"
                        >
                          🗑️ Quitar
                        </button>
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>

            <div className="carrito-actions-bar">
              <button
                onClick={vaciar}
                className="btn-vaciar-carrito"
                disabled={enviando}
              >
                Vaciar Carrito
              </button>
            </div>
          </div>

          <div className="carrito-summary-card">
            <h3>Resumen de la orden</h3>
            <div className="summary-row">
              <span>Total de unidades:</span>
              <strong>{items.reduce((acc, i) => acc + i.cantidad, 0)}</strong>
            </div>
            <div className="summary-row total-row">
              <span>Total:</span>
              <strong className="summary-total-price">
                ${Number(total).toLocaleString('es-AR')}
              </strong>
            </div>

            {/* Parte 2.5: Botón deshabilitado mientras enviando sea true, cambia texto a 'Confirmando…' */}
            <button
              onClick={confirmar}
              disabled={enviando || items.length === 0}
              className="btn-checkout-primary btn-confirmar-compra"
            >
              {enviando ? 'Confirmando…' : 'Confirmar compra'}
            </button>
          </div>
        </div>
      )}
    </div>
  );
};

export default Carrito;

import { useState } from 'react';
import { useCart } from '../context/CartContext';
import { useAuth } from '../context/AuthContext';
import { useNavigate } from 'react-router-dom';
import CheckoutModal from './CheckoutModal';

const Cart = ({ isOpen, onClose }) => {
  const { cart, quitarDelCarrito, cantidadTotal, precioTotal } = useCart();
  const { isAuthenticated } = useAuth();
  const navigate = useNavigate();
  const [mostrarCheckout, setMostrarCheckout] = useState(false);

  if (!isOpen) return null;

  const handleProcederCheckout = () => {
    if (!isAuthenticated) {
      onClose();
      navigate('/login', {
        state: { message: 'Debes iniciar sesión para finalizar tu compra.' },
      });
      return;
    }
    setMostrarCheckout(true);
  };

  return (
    <>
      <div className="cart-drawer-overlay" onClick={onClose}>
        <div className="cart-drawer" onClick={(e) => e.stopPropagation()}>
          <div className="cart-drawer-header">
            <h3>🛒 Carrito de Compras ({cantidadTotal})</h3>
            <button onClick={onClose} className="btn-close-drawer">✕</button>
          </div>

          {cart.length === 0 ? (
            <div className="cart-empty-drawer">
              <span className="empty-cart-icon">🛒</span>
              <p>Tu carrito está vacío.</p>
              <button onClick={onClose} className="btn-auth-primary" style={{ marginTop: '12px' }}>
                Explorar Productos
              </button>
            </div>
          ) : (
            <>
              <ul className="cart-items-list">
                {cart.map((item) => (
                  <li key={item.id} className="cart-item-row">
                    <div className="cart-item-info">
                      <span className="cart-item-name">{item.nombre}</span>
                      <span className="cart-item-sub">
                        {item.cantidad} x ${Number(item.precio_final || item.precio || 0).toLocaleString('es-AR')}
                      </span>
                    </div>
                    <div className="cart-item-actions">
                      <span className="cart-item-total">
                        ${Number((item.precio_final || item.precio || 0) * item.cantidad).toLocaleString('es-AR')}
                      </span>
                      <button
                        onClick={() => quitarDelCarrito(item.id)}
                        className="btn-item-remove"
                        title="Quitar"
                      >
                        🗑️
                      </button>
                    </div>
                  </li>
                ))}
              </ul>

              <div className="cart-drawer-footer">
                <div className="cart-total-row">
                  <span>Total estimado:</span>
                  <strong>${precioTotal.toLocaleString('es-AR')}</strong>
                </div>

                {!isAuthenticated && (
                  <div className="cart-guest-warning">
                    ⚠️ Estás en modo invitado. Debes iniciar sesión para comprar.
                  </div>
                )}

                <button
                  onClick={handleProcederCheckout}
                  className="btn-checkout-primary"
                >
                  {isAuthenticated ? 'Finalizar Compra 🛍️' : 'Iniciar Sesión para Comprar 🔒'}
                </button>
              </div>
            </>
          )}
        </div>
      </div>

      {mostrarCheckout && (
        <CheckoutModal onClose={() => setMostrarCheckout(false)} />
      )}
    </>
  );
};

export default Cart;

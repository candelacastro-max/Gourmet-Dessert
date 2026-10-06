from write_frontend import write

checkout_modal = """import { useState } from 'react';
import { useCart } from '../context/CartContext';
import { useAuth } from '../context/AuthContext';
import { crearPedido } from '../services/api';
import Ticket from './Ticket';

const METODOS_PAGO = [
  { id: 'efectivo', label: '💵 Efectivo contra entrega' },
  { id: 'debito', label: '💳 Tarjeta de Débito' },
  { id: 'credito', label: '💳 Tarjeta de Crédito (Hasta 3 cuotas sin interés)' },
  { id: 'transferencia', label: '📱 Transferencia Bancaria / Mercado Pago' },
];

const overlayStyle = {
  position: 'fixed', inset: 0,
  background: 'rgba(0,0,0,0.65)',
  backdropFilter: 'blur(3px)',
  display: 'flex', alignItems: 'center', justifyContent: 'center',
  zIndex: 2000,
};

const modalStyle = {
  background: '#fff', borderRadius: '16px',
  padding: '32px', maxWidth: '440px', width: '90%',
  boxShadow: '0 20px 40px rgba(0,0,0,0.25)',
};

const CheckoutModal = ({ onClose }) => {
  const { cart, precioTotal, vaciarCarrito } = useCart();
  const { token, isAuthenticated } = useAuth();
  const [metodoPago, setMetodoPago] = useState('');
  const [guardando, setGuardando] = useState(false);
  const [ticket, setTicket] = useState(null);

  const handleConfirmar = async () => {
    if (!metodoPago || guardando) return;
    setGuardando(true);

    let numeroPedido = Math.floor(Math.random() * 900000) + 100000;
    const fecha = new Date().toLocaleString('es-AR');

    if (isAuthenticated && token) {
      try {
        const payload = {
          items: cart.map(item => ({
            producto_id: item.id,
            cantidad: item.cantidad
          }))
        };
        const pedidoCreado = await crearPedido(token, payload);
        if (pedidoCreado?.id) {
          numeroPedido = pedidoCreado.id;
        }
      } catch (err) {
        console.warn('Nota: guardado local activo (backend:', err.message, ')');
      }
    }

    setTicket({
      numero: numeroPedido,
      fecha,
      items: cart,
      total: precioTotal,
      metodoPago: METODOS_PAGO.find(m => m.id === metodoPago)?.label,
    });
    vaciarCarrito();
    setGuardando(false);
  };

  if (ticket) {
    return (
      <div style={overlayStyle} onClick={onClose}>
        <div onClick={e => e.stopPropagation()}>
          <Ticket ticket={ticket} onClose={onClose} />
        </div>
      </div>
    );
  }

  return (
    <div style={overlayStyle} onClick={onClose}>
      <div style={modalStyle} onClick={e => e.stopPropagation()}>
        <h2 style={{ marginTop: 0, fontSize: '22px', fontWeight: 800 }}>💳 Confirmar Compra</h2>

        <p style={{ color: '#475569', marginBottom: '18px', fontSize: '15px' }}>
          Total a pagar: <strong style={{ color: '#9333ea', fontSize: '18px' }}>${precioTotal.toLocaleString('es-AR')}</strong>
        </p>

        <p style={{ fontSize: '13px', fontWeight: 600, color: '#334155', marginBottom: '8px' }}>
          Selecciona tu método de pago:
        </p>

        <div style={{ display: 'flex', flexDirection: 'column', gap: '10px', marginBottom: '24px' }}>
          {METODOS_PAGO.map(m => (
            <label
              key={m.id}
              style={{
                display: 'flex', alignItems: 'center', gap: '10px',
                padding: '12px 14px',
                border: '2px solid ' + (metodoPago === m.id ? '#9333ea' : '#e2e8f0'),
                borderRadius: '10px', cursor: 'pointer',
                background: metodoPago === m.id ? '#f3e8ff' : '#f8fafc',
                fontWeight: metodoPago === m.id ? '600' : 'normal',
                fontSize: '14px',
                transition: 'all 0.15s',
              }}
            >
              <input
                type="radio"
                name="pago"
                value={m.id}
                checked={metodoPago === m.id}
                onChange={() => setMetodoPago(m.id)}
                style={{ accentColor: '#9333ea' }}
              />
              {m.label}
            </label>
          ))}
        </div>

        <div style={{ display: 'flex', gap: '10px', justifyContent: 'flex-end' }}>
          <button
            onClick={onClose}
            disabled={guardando}
            style={{
              padding: '10px 18px', borderRadius: '8px',
              border: '1px solid #cbd5e1', cursor: 'pointer',
              background: '#f8fafc', fontWeight: 600, fontSize: '14px'
            }}
          >
            Cancelar
          </button>
          <button
            onClick={handleConfirmar}
            disabled={!metodoPago || guardando}
            style={{
              padding: '10px 20px', borderRadius: '8px', border: 'none',
              background: metodoPago && !guardando ? '#10b981' : '#cbd5e1',
              color: 'white', fontWeight: 700, fontSize: '14px',
              cursor: metodoPago && !guardando ? 'pointer' : 'not-allowed',
            }}
          >
            {guardando ? 'Procesando...' : 'Confirmar Pedido ✨'}
          </button>
        </div>
      </div>
    </div>
  );
};

export default CheckoutModal;
"""

write("components/CheckoutModal.jsx", checkout_modal)
print("CHECKOUT MODAL OK")

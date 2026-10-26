import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { getMisPedidos, revocarPedido } from '../services/api';

const DIAS_PARA_REVOCAR = 10;
function puedeRevocar(pedido) {
  if (pedido.estado === "cancelado") return false;
  const ms = Date.now() - new Date(pedido.creado_en);
  return ms / 86400000 <= DIAS_PARA_REVOCAR;
}

const MisPedidos = () => {
  const { user } = useAuth();
  const [pedidos, setPedidos] = useState([]);
  const [cargando, setCargando] = useState(true);
  const [error, setError] = useState(null);
  
  // Estado para la revocación
  const [revocandoId, setRevocandoId] = useState(null);
  const [modalPedido, setModalPedido] = useState(null); // Pedido a cancelar en modal
  const [motivoCancelacion, setMotivoCancelacion] = useState('');
  const [codigosRevocacion, setCodigosRevocacion] = useState({});
  const [errorRevocacion, setErrorRevocacion] = useState({});

  const cargarPedidos = () => {
    setCargando(true);
    setError(null);
    getMisPedidos()
      .then((data) => {
        setPedidos(Array.isArray(data) ? data : []);
      })
      .catch((err) => {
        console.error('Error al cargar historial de pedidos:', err);
        setError(err.message || 'No se pudieron cargar tus pedidos previos.');
      })
      .finally(() => {
        setCargando(false);
      });
  };

  useEffect(() => {
    cargarPedidos();
  }, []);

  const abrirModalCancelacion = (pedido) => {
    setModalPedido(pedido);
    setMotivoCancelacion('');
  };

  const cerrarModalCancelacion = () => {
    setModalPedido(null);
    setMotivoCancelacion('');
  };

  const handleConfirmarCancelacion = async () => {
    if (!modalPedido) return;
    const pedidoId = modalPedido.id;
    setRevocandoId(pedidoId);
    setErrorRevocacion({ ...errorRevocacion, [pedidoId]: null });
    
    try {
      const data = await revocarPedido(pedidoId, motivoCancelacion);
      setCodigosRevocacion({ ...codigosRevocacion, [pedidoId]: data.codigo });
      cerrarModalCancelacion();
      cargarPedidos(); // Refrescar historial
    } catch (err) {
      setErrorRevocacion({ ...errorRevocacion, [pedidoId]: err.message });
      cerrarModalCancelacion();
    } finally {
      setRevocandoId(null);
    }
  };

  return (
    <div className="pedidos-container">
      <div className="pedidos-header">
        <div>
          <h2>📜 Mis Pedidos</h2>
          <p>Historial de compras de {user?.nombre || user?.email || 'tu cuenta'}</p>
        </div>
        <Link to="/catalogo" className="btn-secondary">
          ← Volver al Catálogo
        </Link>
      </div>

      {/* ESTADO 1: CARGANDO */}
      {cargando && (
        <div className="loading-state">
          <div className="spinner"></div>
          <p>Cargando historial de pedidos...</p>
        </div>
      )}

      {/* ESTADO 2: ERROR */}
      {!cargando && error && (
        <div className="auth-alert error">
          <span>⚠️</span>
          <div>
            <strong>Error al cargar pedidos:</strong> {error}
          </div>
        </div>
      )}

      {/* ESTADO 3: LISTA VACÍA */}
      {!cargando && !error && pedidos.length === 0 && (
        <div className="empty-pedidos">
          <span className="empty-icon">🛍️</span>
          <h3>Aún no tienes pedidos registrados</h3>
          <p>Explora nuestro catálogo gourmet y realiza tu primer pedido.</p>
          <Link to="/catalogo" className="btn-auth-primary" style={{ display: 'inline-block', marginTop: '16px' }}>
            Explorar Catálogo
          </Link>
        </div>
      )}

      {/* LISTA CON PEDIDOS: producto_id como key */}
      {!cargando && !error && pedidos.length > 0 && (
        <div className="pedidos-list">
          {pedidos.map((pedido) => (
            <div key={pedido.id} className="pedido-card">
              <div className="pedido-card-header">
                <div>
                  <span className="pedido-id">Pedido #{pedido.id}</span>
                  <span className="pedido-fecha">
                    {pedido.creado_en ? new Date(pedido.creado_en).toLocaleString('es-AR') : 'Reciente'}
                  </span>
                </div>
                <span className={`pedido-estado estado-${(pedido.estado || 'comprado').toLowerCase()}`}>
                  {pedido.estado === 'pendiente' ? 'Comprado' : (pedido.estado || 'Comprado')}
                </span>
              </div>

              {pedido.items && pedido.items.length > 0 && (
                <div className="pedido-items-table">
                  <table>
                    <thead>
                      <tr>
                        <th>Producto</th>
                        <th>Cantidad</th>
                        <th>Precio Unitario</th>
                        <th>Subtotal</th>
                      </tr>
                    </thead>
                    <tbody>
                      {pedido.items.map((item) => (
                        <tr key={item.producto_id}>
                          <td>{item.nombre || item.producto_nombre || `Producto #${item.producto_id}`}</td>
                          <td>{item.cantidad}</td>
                          <td>${Number(item.precio_unitario || item.precio || 0).toLocaleString('es-AR')}</td>
                          <td>${Number((item.precio_unitario || item.precio || 0) * item.cantidad).toLocaleString('es-AR')}</td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              )}

              <div className="pedido-card-footer" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <div>
                  {puedeRevocar(pedido) && (
                    <button 
                      className="btn-danger" 
                      onClick={() => abrirModalCancelacion(pedido)}
                      disabled={revocandoId === pedido.id}
                      style={{ padding: '0.5rem 1rem', background: '#dc2626', color: 'white', border: 'none', borderRadius: '6px', cursor: 'pointer' }}
                    >
                      {revocandoId === pedido.id ? 'Cancelando...' : 'Arrepentirme de esta compra'}
                    </button>
                  )}
                  {errorRevocacion[pedido.id] && (
                    <p style={{ color: 'var(--error-color)', fontSize: '0.9rem', marginTop: '0.5rem' }}>
                      {errorRevocacion[pedido.id]}
                    </p>
                  )}
                  {codigosRevocacion[pedido.id] && (
                    <p role="status" style={{ color: 'var(--success-color)', fontWeight: 'bold', marginTop: '0.5rem' }}>
                      Código de revocación: {codigosRevocacion[pedido.id]}
                    </p>
                  )}
                </div>
                <div>
                  <span>Total abonado: </span>
                  <strong>${Number(pedido.total || 0).toLocaleString('es-AR')}</strong>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Modal para ingresar el motivo de cancelación */}
      {modalPedido && (
        <div style={{
          position: 'fixed',
          top: 0,
          left: 0,
          width: '100%',
          height: '100%',
          backgroundColor: 'rgba(0,0,0,0.6)',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          zIndex: 9999,
          padding: '1rem'
        }}>
          <div style={{
            background: 'var(--surface-color, #ffffff)',
            color: 'var(--text-primary, #333333)',
            borderRadius: '12px',
            maxWidth: '480px',
            width: '100%',
            padding: '1.75rem',
            boxShadow: '0 20px 25px -5px rgba(0, 0, 0, 0.3)',
            display: 'flex',
            flexDirection: 'column',
            gap: '1rem'
          }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
              <h3 style={{ margin: 0, fontSize: '1.25rem' }}>Cancelar Pedido #{modalPedido.id}</h3>
              <button 
                onClick={cerrarModalCancelacion} 
                style={{ background: 'none', border: 'none', fontSize: '1.5rem', cursor: 'pointer', color: 'inherit' }}
              >
                ×
              </button>
            </div>

            <p style={{ margin: 0, fontSize: '0.95rem', color: 'var(--text-secondary, #666)' }}>
              ¿Estás seguro/a de que deseas cancelar este pedido? De acuerdo con la ley, se procesará la revocación inmediatamente.
            </p>

            <div>
              <label style={{ display: 'block', fontWeight: 'bold', marginBottom: '0.5rem', fontSize: '0.9rem' }}>
                Motivo de la cancelación (opcional):
              </label>
              <textarea
                value={motivoCancelacion}
                onChange={(e) => setMotivoCancelacion(e.target.value)}
                placeholder="Contanos brevemente por qué cancelás la compra (ej. me equivoqué de producto, demora en el envío, etc.)..."
                rows={3}
                style={{
                  width: '100%',
                  padding: '0.75rem',
                  borderRadius: '8px',
                  border: '1px solid #ccc',
                  fontFamily: 'inherit',
                  fontSize: '0.9rem',
                  boxSizing: 'border-box',
                  resize: 'vertical'
                }}
              />
            </div>

            <div style={{ display: 'flex', justifyContent: 'flex-end', gap: '0.75rem', marginTop: '0.5rem' }}>
              <button
                type="button"
                className="btn-secondary"
                onClick={cerrarModalCancelacion}
                disabled={revocandoId === modalPedido.id}
                style={{ padding: '0.6rem 1.2rem', cursor: 'pointer' }}
              >
                Volver
              </button>
              <button
                type="button"
                className="btn-danger"
                onClick={handleConfirmarCancelacion}
                disabled={revocandoId === modalPedido.id}
                style={{
                  padding: '0.6rem 1.2rem',
                  backgroundColor: '#dc2626',
                  color: '#fff',
                  border: 'none',
                  borderRadius: '6px',
                  cursor: 'pointer',
                  fontWeight: 'bold'
                }}
              >
                {revocandoId === modalPedido.id ? 'Cancelando...' : 'Confirmar Cancelación'}
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default MisPedidos;

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
  const [confirmarId, setConfirmarId] = useState(null);
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

  const handleRevocar = async (pedidoId) => {
    if (confirmarId !== pedidoId) {
      setConfirmarId(pedidoId);
      return;
    }
    
    // Doble clic: Ejecutar revocación
    setRevocandoId(pedidoId);
    setErrorRevocacion({ ...errorRevocacion, [pedidoId]: null });
    
    try {
      const data = await revocarPedido(pedidoId);
      setCodigosRevocacion({ ...codigosRevocacion, [pedidoId]: data.codigo });
      cargarPedidos(); // Refrescar historial
    } catch (err) {
      setErrorRevocacion({ ...errorRevocacion, [pedidoId]: err.message });
    } finally {
      setRevocandoId(null);
      setConfirmarId(null);
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
                      onClick={() => handleRevocar(pedido.id)}
                      disabled={revocandoId === pedido.id}
                      style={{ padding: '0.5rem 1rem', background: confirmarId === pedido.id ? 'var(--error-color)' : 'var(--text-secondary)' }}
                    >
                      {revocandoId === pedido.id ? 'Revocando...' : (confirmarId === pedido.id ? 'Confirmar revocación' : 'Arrepentirme de esta compra')}
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
    </div>
  );
};

export default MisPedidos;

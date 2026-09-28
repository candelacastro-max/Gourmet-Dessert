import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { getMisPedidos } from '../services/api';

const MisPedidos = () => {
  const { user } = useAuth();
  const [pedidos, setPedidos] = useState([]);
  const [cargando, setCargando] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
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
  }, []);

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
                <span className={`pedido-estado estado-${(pedido.estado || 'pendiente').toLowerCase()}`}>
                  {pedido.estado || 'Pendiente'}
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

              <div className="pedido-card-footer">
                <span>Total abonado:</span>
                <strong>${Number(pedido.total || 0).toLocaleString('es-AR')}</strong>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default MisPedidos;

import React, { useState, useEffect, useRef } from 'react';
import { getNotificacionesCancelaciones } from '../services/api';

const NotificacionesAdmin = () => {
  const [notificaciones, setNotificaciones] = useState([]);
  const [abierto, setAbierto] = useState(false);
  const [cargando, setCargando] = useState(false);
  const [detalleModal, setDetalleModal] = useState(null);
  const dropdownRef = useRef(null);

  const cargarNotificaciones = async () => {
    try {
      setCargando(true);
      const data = await getNotificacionesCancelaciones();
      setNotificaciones(Array.isArray(data) ? data : []);
    } catch (err) {
      console.error('Error cargando notificaciones:', err);
    } finally {
      setCargando(false);
    }
  };

  useEffect(() => {
    cargarNotificaciones();
    // Sondeo periódico cada 20 segundos para nuevas cancelaciones
    const interval = setInterval(cargarNotificaciones, 20000);
    return () => clearInterval(interval);
  }, []);

  // Cerrar dropdown al hacer click afuera
  useEffect(() => {
    function handleClickOutside(event) {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target)) {
        setAbierto(false);
      }
    }
    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  return (
    <div style={{ position: 'relative' }} ref={dropdownRef}>
      <button
        onClick={() => {
          setAbierto(!abierto);
          if (!abierto) cargarNotificaciones();
        }}
        title="Notificaciones de cancelaciones"
        style={{
          background: 'rgba(255, 255, 255, 0.1)',
          border: '1px solid rgba(255, 255, 255, 0.2)',
          borderRadius: '50%',
          width: '38px',
          height: '38px',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          cursor: 'pointer',
          position: 'relative',
          fontSize: '1.2rem',
          color: 'inherit',
          transition: 'all 0.2s ease'
        }}
      >
        🔔
        {notificaciones.length > 0 && (
          <span
            style={{
              position: 'absolute',
              top: '-4px',
              right: '-4px',
              backgroundColor: '#ef4444',
              color: 'white',
              borderRadius: '9999px',
              padding: '2px 6px',
              fontSize: '0.7rem',
              fontWeight: 'bold',
              minWidth: '16px',
              textAlign: 'center',
              boxShadow: '0 2px 4px rgba(0,0,0,0.2)'
            }}
          >
            {notificaciones.length}
          </span>
        )}
      </button>

      {/* Menú desplegable */}
      {abierto && (
        <div
          style={{
            position: 'absolute',
            top: '46px',
            right: 0,
            width: '350px',
            maxHeight: '440px',
            backgroundColor: '#ffffff',
            color: '#1f2937',
            borderRadius: '12px',
            boxShadow: '0 10px 25px -5px rgba(0,0,0,0.2), 0 8px 10px -6px rgba(0,0,0,0.1)',
            zIndex: 1000,
            display: 'flex',
            flexDirection: 'column',
            overflow: 'hidden',
            border: '1px solid #e5e7eb'
          }}
        >
          <div
            style={{
              padding: '0.85rem 1rem',
              borderBottom: '1px solid #f3f4f6',
              display: 'flex',
              justifyContent: 'space-between',
              alignItems: 'center',
              background: '#f9fafb'
            }}
          >
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
              <span style={{ fontSize: '1rem' }}>📢</span>
              <strong style={{ fontSize: '0.95rem', color: '#111827' }}>Pedidos Cancelados</strong>
            </div>
            <button
              onClick={cargarNotificaciones}
              style={{
                background: 'none',
                border: 'none',
                color: '#4f46e5',
                cursor: 'pointer',
                fontSize: '0.8rem',
                fontWeight: '500'
              }}
            >
              {cargando ? 'Actualizando...' : 'Actualizar'}
            </button>
          </div>

          <div style={{ overflowY: 'auto', flex: 1 }}>
            {notificaciones.length === 0 ? (
              <div style={{ padding: '2rem 1rem', textAlign: 'center', color: '#6b7280', fontSize: '0.9rem' }}>
                <span style={{ fontSize: '2rem', display: 'block', marginBottom: '0.5rem' }}>✨</span>
                No hay cancelaciones registradas.
              </div>
            ) : (
              notificaciones.map((n) => (
                <div
                  key={n.id}
                  onClick={() => setDetalleModal(n)}
                  style={{
                    padding: '0.85rem 1rem',
                    borderBottom: '1px solid #f3f4f6',
                    cursor: 'pointer',
                    transition: 'background-color 0.15s ease',
                  }}
                  onMouseEnter={(e) => (e.currentTarget.style.backgroundColor = '#f9fafb')}
                  onMouseLeave={(e) => (e.currentTarget.style.backgroundColor = 'transparent')}
                >
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
                    <span style={{ fontWeight: '600', fontSize: '0.9rem', color: '#dc2626' }}>
                      Pedido #{n.pedido_id} cancelado
                    </span>
                    <span style={{ fontSize: '0.75rem', color: '#9ca3af' }}>
                      {n.creada_en ? new Date(n.creada_en).toLocaleDateString('es-AR') : ''}
                    </span>
                  </div>
                  <div style={{ fontSize: '0.85rem', color: '#4b5563', marginTop: '0.25rem' }}>
                    <strong>Cliente:</strong> {n.cliente_nombre} ({n.cliente_email})
                  </div>
                  <div style={{ fontSize: '0.85rem', color: '#374151', marginTop: '0.3rem', fontStyle: n.motivo ? 'italic' : 'normal' }}>
                    <strong>Motivo:</strong> {n.motivo}
                  </div>
                </div>
              ))
            )}
          </div>
        </div>
      )}

      {/* Modal de Detalle Completo de la Cancelación */}
      {detalleModal && (
        <div
          style={{
            position: 'fixed',
            top: 0,
            left: 0,
            width: '100vw',
            height: '100vh',
            backgroundColor: 'rgba(0,0,0,0.5)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            zIndex: 99999,
            padding: '1rem'
          }}
        >
          <div
            style={{
              backgroundColor: '#ffffff',
              color: '#1f2937',
              borderRadius: '12px',
              maxWidth: '520px',
              width: '100%',
              padding: '1.75rem',
              boxShadow: '0 20px 25px -5px rgba(0,0,0,0.3)',
              display: 'flex',
              flexDirection: 'column',
              gap: '1rem'
            }}
          >
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
              <h3 style={{ margin: 0, fontSize: '1.25rem', color: '#dc2626' }}>
                Detalle de Cancelación - Pedido #{detalleModal.pedido_id}
              </h3>
              <button
                onClick={() => setDetalleModal(null)}
                style={{ background: 'none', border: 'none', fontSize: '1.5rem', cursor: 'pointer', color: '#9ca3af' }}
              >
                ×
              </button>
            </div>

            <div style={{ background: '#fef2f2', border: '1px solid #fee2e2', borderRadius: '8px', padding: '0.85rem' }}>
              <div style={{ fontSize: '0.9rem', marginBottom: '0.25rem' }}>
                <strong>Código de Revocación:</strong> <code>{detalleModal.codigo}</code>
              </div>
              <div style={{ fontSize: '0.9rem', marginBottom: '0.25rem' }}>
                <strong>Fecha:</strong> {detalleModal.creada_en ? new Date(detalleModal.creada_en).toLocaleString('es-AR') : 'N/A'}
              </div>
              <div style={{ fontSize: '0.9rem', marginBottom: '0.25rem' }}>
                <strong>Cliente:</strong> {detalleModal.cliente_nombre} ({detalleModal.cliente_email})
              </div>
              <div style={{ fontSize: '0.9rem' }}>
                <strong>Total Reembolsado/Anulado:</strong> ${detalleModal.total_pedido.toLocaleString('es-AR')}
              </div>
            </div>

            <div>
              <h4 style={{ margin: '0 0 0.5rem 0', fontSize: '0.95rem' }}>Motivo expresado por el cliente:</h4>
              <div
                style={{
                  background: '#f9fafb',
                  border: '1px solid #e5e7eb',
                  borderRadius: '6px',
                  padding: '0.75rem',
                  fontSize: '0.9rem',
                  fontStyle: 'italic',
                  color: '#374151'
                }}
              >
                "{detalleModal.motivo}"
              </div>
            </div>

            {detalleModal.items && detalleModal.items.length > 0 && (
              <div>
                <h4 style={{ margin: '0 0 0.5rem 0', fontSize: '0.95rem' }}>Productos cancelados:</h4>
                <ul style={{ margin: 0, paddingLeft: '1.2rem', fontSize: '0.85rem', color: '#4b5563' }}>
                  {detalleModal.items.map((it, idx) => (
                    <li key={idx} style={{ marginBottom: '0.25rem' }}>
                      {it.nombre} x {it.cantidad} (${it.precio_unitario.toLocaleString('es-AR')} c/u)
                    </li>
                  ))}
                </ul>
              </div>
            )}

            <div style={{ display: 'flex', justifyContent: 'flex-end', marginTop: '0.5rem' }}>
              <button
                onClick={() => setDetalleModal(null)}
                style={{
                  padding: '0.5rem 1.25rem',
                  backgroundColor: '#4f46e5',
                  color: 'white',
                  border: 'none',
                  borderRadius: '6px',
                  cursor: 'pointer',
                  fontWeight: '500'
                }}
              >
                Cerrar
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default NotificacionesAdmin;

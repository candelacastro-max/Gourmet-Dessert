import React from 'react';
import { useRegisterSW } from 'virtual:pwa-register/react';

export function ActualizacionDisponible() {
  const {
    needRefresh: [needRefresh, setNeedRefresh],
    updateServiceWorker,
  } = useRegisterSW({
    onRegistered(r) {
      console.log('Service Worker registrado:', r);
    },
    onRegisterError(error) {
      console.error('Error registrando Service Worker:', error);
    },
  });

  if (!needRefresh) return null;

  return (
    <div
      role="alert"
      style={{
        position: 'fixed',
        bottom: '20px',
        right: '20px',
        backgroundColor: '#1f2937',
        color: '#ffffff',
        padding: '16px 20px',
        borderRadius: '12px',
        boxShadow: '0 10px 25px -5px rgba(0, 0, 0, 0.4), 0 8px 10px -6px rgba(0, 0, 0, 0.3)',
        display: 'flex',
        alignItems: 'center',
        gap: '14px',
        zIndex: 9999,
        maxWidth: '90vw',
        fontSize: '14px',
      }}
    >
      <span>✨ Hay una versión nueva de la tienda.</span>
      <div style={{ display: 'flex', gap: '8px' }}>
        <button
          onClick={() => updateServiceWorker(true)}
          style={{
            backgroundColor: '#863bff',
            color: 'white',
            border: 'none',
            padding: '8px 14px',
            borderRadius: '6px',
            cursor: 'pointer',
            fontWeight: '600',
            fontSize: '13px',
          }}
        >
          Actualizar
        </button>
        <button
          onClick={() => setNeedRefresh(false)}
          style={{
            backgroundColor: 'transparent',
            color: '#9ca3af',
            border: '1px solid #4b5563',
            padding: '8px 12px',
            borderRadius: '6px',
            cursor: 'pointer',
            fontSize: '13px',
          }}
        >
          Cerrar
        </button>
      </div>
    </div>
  );
}

export default ActualizacionDisponible;

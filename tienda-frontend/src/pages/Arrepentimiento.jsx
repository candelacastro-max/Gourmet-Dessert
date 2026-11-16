import React, { useState } from 'react';

const BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const Arrepentimiento = () => {
  const [email, setEmail] = useState('');
  const [pedidoId, setPedidoId] = useState('');
  const [motivo, setMotivo] = useState('');
  const [codigo, setCodigo] = useState(null);
  const [error, setError] = useState(null);
  const [cargando, setCargando] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null);
    setCargando(true);

    try {
      // Disposición 954/2025: Sin requerir inicio de sesión ni token de autorización
      const res = await fetch(`${BASE_URL}/arrepentimiento`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          email: email.trim(),
          pedido_id: Number(pedidoId),
        }),
      });

      if (!res.ok) {
        const errorData = await res.json().catch(() => ({}));
        throw new Error(errorData.detail || 'Error al procesar la solicitud de arrepentimiento');
      }

      const data = await res.json();
      setCodigo(data.codigo);
    } catch (err) {
      setError(err.message || 'Error al enviar la solicitud');
    } finally {
      setCargando(false);
    }
  };

  return (
    <div className="container" style={{ padding: '2rem', maxWidth: '600px', margin: '0 auto' }}>
      <h1>Botón de Arrepentimiento</h1>
      <p style={{ marginTop: '0.5rem', color: '#6b7280' }}>
        Conforme a la Ley 24.240 y Disposición 954/2025, podés revocar tu compra dentro de los 10 días corridos sin costo.
      </p>

      {codigo ? (
        <div
          role="status"
          style={{
            marginTop: '2rem',
            padding: '1.5rem',
            backgroundColor: '#ecfdf5',
            border: '1px solid #a7f3d0',
            borderRadius: '8px',
            color: '#065f46',
          }}
        >
          <h3>¡Solicitud de arrepentimiento registrada!</h3>
          <p style={{ marginTop: '0.5rem' }}>
            Tu código de trámite es: <strong>{codigo}</strong>
          </p>
          <p style={{ fontSize: '13px', marginTop: '0.5rem', color: '#047857' }}>
            Guardá este código como comprobante de tu revocación.
          </p>
        </div>
      ) : (
        <form onSubmit={handleSubmit} style={{ marginTop: '2rem', display: 'flex', flexDirection: 'column', gap: '1.25rem' }}>
          {error && (
            <div style={{ padding: '1rem', backgroundColor: '#fef2f2', border: '1px solid #fecaca', color: '#dc2626', borderRadius: '6px' }}>
              {error}
            </div>
          )}

          <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
            <label htmlFor="arrepentimiento-email">Correo electrónico de la compra:</label>
            <input
              id="arrepentimiento-email"
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="ejemplo@correo.com"
              required
              disabled={cargando}
              style={{ padding: '0.75rem', borderRadius: '6px', border: '1px solid #d1d5db' }}
            />
          </div>

          <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
            <label htmlFor="arrepentimiento-pedido">Número de pedido:</label>
            <input
              id="arrepentimiento-pedido"
              type="number"
              value={pedidoId}
              onChange={(e) => setPedidoId(e.target.value)}
              placeholder="Ej: 12"
              required
              disabled={cargando}
              style={{ padding: '0.75rem', borderRadius: '6px', border: '1px solid #d1d5db' }}
            />
          </div>

          <button
            type="submit"
            disabled={cargando}
            style={{
              padding: '0.85rem',
              backgroundColor: '#ef4444',
              color: 'white',
              border: 'none',
              borderRadius: '6px',
              fontWeight: 'bold',
              cursor: 'pointer',
              marginTop: '1rem',
            }}
          >
            {cargando ? 'Enviando...' : 'Enviar solicitud de arrepentimiento'}
          </button>
        </form>
      )}
    </div>
  );
};

export default Arrepentimiento;

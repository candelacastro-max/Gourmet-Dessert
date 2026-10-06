import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

const Arrepentimiento = () => {
  const { isAuthenticated } = useAuth();
  const navigate = useNavigate();

  return (
    <div className="container" style={{ padding: '2rem', maxWidth: '800px', margin: '0 auto' }}>
      <h1>Derecho de Arrepentimiento</h1>
      
      <div className="card" style={{ padding: '2rem', marginTop: '1.5rem', background: 'var(--surface-color)' }}>
        <h2>¿Qué es el botón de arrepentimiento?</h2>
        <p style={{ marginTop: '1rem', lineHeight: '1.6' }}>
          Según la ley, tenés derecho a arrepentirte de cualquier compra realizada por este medio dentro de los <strong>10 días corridos</strong> desde que recibiste el producto o celebraste el contrato, lo último que ocurra.
        </p>
        
        <ul style={{ margin: '1rem 0 1rem 1.5rem', lineHeight: '1.6' }}>
          <li>No tiene ningún costo para vos.</li>
          <li>No tenés que justificar los motivos de tu decisión.</li>
          <li>Los gastos de devolución corren por cuenta del vendedor.</li>
        </ul>

        <div style={{ marginTop: '2rem', textAlign: 'center' }}>
          {isAuthenticated ? (
            <div>
              <p style={{ marginBottom: '1rem' }}>Ya tenés la sesión iniciada. Podés ejercer tu derecho desde tu historial de pedidos.</p>
              <button className="btn-primary" onClick={() => navigate('/mis-pedidos')}>
                Ir a Mis Pedidos
              </button>
            </div>
          ) : (
            <div>
              <p style={{ marginBottom: '1rem' }}>Para arrepentirte de una compra, por favor iniciá sesión.</p>
              <button className="btn-primary" onClick={() => navigate('/login')}>
                Iniciar Sesión
              </button>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default Arrepentimiento;

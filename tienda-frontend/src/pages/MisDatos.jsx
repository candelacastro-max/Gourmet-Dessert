import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { getMisDatos, eliminarMiCuenta, authHeaders } from '../services/api';
import { useAuth } from '../context/AuthContext';
import { useCarrito } from '../context/CarritoContext';

const MisDatos = () => {
  const [datos, setDatos] = useState(null);
  const [cargando, setCargando] = useState(true);
  const [error, setError] = useState(null);
  
  const [eliminarTexto, setEliminarTexto] = useState('');
  const [eliminando, setEliminando] = useState(false);
  
  const { logout } = useAuth();
  const { vaciarCarrito } = useCarrito();
  const navigate = useNavigate();

  useEffect(() => {
    getMisDatos()
      .then(data => setDatos(data))
      .catch(err => setError(err.message))
      .finally(() => setCargando(false));
  }, []);

  const handleDescargarJSON = async () => {
    try {
      const BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';
      const res = await fetch(`${BASE_URL}/usuarios/me/exportar`, {
        method: 'GET',
        headers: authHeaders()
      });
      
      if (!res.ok) throw new Error("No se pudo descargar los datos");
      
      const blob = await res.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = 'mis_datos.json';
      document.body.appendChild(a);
      a.click();
      a.remove();
      window.URL.revokeObjectURL(url);
    } catch (err) {
      alert("Error al descargar: " + err.message);
    }
  };

  const handleEliminarCuenta = async () => {
    if (eliminarTexto !== 'ELIMINAR') return;
    
    setEliminando(true);
    try {
      await eliminarMiCuenta();
      vaciarCarrito();
      logout();
      navigate('/catalogo', { state: { mensaje: "Tu cuenta ha sido eliminada con éxito. Ya no tenemos acceso a tus datos personales." } });
    } catch (err) {
      alert("Error al eliminar cuenta: " + err.message);
      setEliminando(false);
    }
  };

  if (cargando) return (
    <div className="container" style={{ padding: '2rem' }}>
      <div className="loading-state">
        <div className="spinner"></div>
        <p>Cargando tus datos...</p>
      </div>
    </div>
  );

  if (error) return (
    <div className="container" style={{ padding: '2rem' }}>
      <div className="auth-alert error">Error: {error}</div>
    </div>
  );

  return (
    <div className="container" style={{ padding: '2rem', maxWidth: '800px', margin: '0 auto' }}>
      <h1>Mis Datos</h1>
      
      {/* Botón de descarga de datos */}
      <div style={{ marginTop: '1rem', marginBottom: '2rem' }}>
        <button className="btn-secondary" onClick={handleDescargarJSON}>
          Descargar mis datos completos (JSON)
        </button>
      </div>

      <div className="card" style={{ padding: '1.5rem', marginBottom: '2rem', background: 'var(--surface-color)' }}>
        <h2>Datos del perfil</h2>
        <pre style={{ background: '#f4f4f4', padding: '1rem', overflowX: 'auto', borderRadius: '4px', marginTop: '1rem' }}>
          {JSON.stringify(datos?.usuario, null, 2)}
        </pre>
      </div>

      <div className="card" style={{ padding: '1.5rem', marginBottom: '2rem', background: 'var(--surface-color)' }}>
        <h2>Mis Pedidos</h2>
        <pre style={{ background: '#f4f4f4', padding: '1rem', overflowX: 'auto', borderRadius: '4px', marginTop: '1rem' }}>
          {JSON.stringify(datos?.pedidos, null, 2)}
        </pre>
      </div>

      <div className="card" style={{ padding: '1.5rem', marginBottom: '2rem', background: 'var(--surface-color)' }}>
        <h2>Mis Solicitudes de Revocación</h2>
        <pre style={{ background: '#f4f4f4', padding: '1rem', overflowX: 'auto', borderRadius: '4px', marginTop: '1rem' }}>
          {JSON.stringify(datos?.solicitudes_revocacion, null, 2)}
        </pre>
      </div>

      {/* SECCIÓN ELIMINAR CUENTA */}
      <div className="card" style={{ padding: '2rem', border: '1px solid var(--error-color)', background: 'var(--surface-color)' }}>
        <h2 style={{ color: 'var(--error-color)' }}>Eliminar mi cuenta</h2>
        <p style={{ marginTop: '1rem', lineHeight: '1.5' }}>
          <strong>¡ATENCIÓN!</strong> Al eliminar tu cuenta:
        </p>
        <ul style={{ margin: '1rem 0 1rem 1.5rem', lineHeight: '1.5' }}>
          <li>Tus datos personales (nombre, correo electrónico, contraseña) serán borrados y anonimizados.</li>
          <li>Tus pedidos y solicitudes seguirán existiendo en el sistema por cuestiones legales y contables, pero no estarán vinculados a ti.</li>
          <li>No podrás iniciar sesión nunca más con esta cuenta.</li>
        </ul>
        
        <div style={{ marginTop: '2rem' }}>
          <label style={{ display: 'block', marginBottom: '0.5rem' }}>Escribe la palabra <strong>ELIMINAR</strong> para confirmar:</label>
          <input 
            type="text" 
            value={eliminarTexto}
            onChange={(e) => setEliminarTexto(e.target.value)}
            placeholder="ELIMINAR"
            style={{ padding: '0.5rem', width: '100%', maxWidth: '300px', marginBottom: '1rem' }}
          />
        </div>
        
        <button 
          className="btn-danger" 
          onClick={handleEliminarCuenta}
          disabled={eliminarTexto !== 'ELIMINAR' || eliminando}
          style={{ 
            background: eliminarTexto === 'ELIMINAR' ? 'var(--error-color)' : 'var(--text-secondary)',
            cursor: eliminarTexto === 'ELIMINAR' ? 'pointer' : 'not-allowed'
          }}
        >
          {eliminando ? 'Eliminando...' : 'Eliminar mi cuenta permanentemente'}
        </button>
      </div>
    </div>
  );
};

export default MisDatos;

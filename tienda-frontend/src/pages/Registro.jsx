import React, { useState } from 'react';
import { useAuth } from '../context/AuthContext';
import { useNavigate } from 'react-router-dom';

export default function Registro() {
  const auth = useAuth?.() || {};
  const register = auth.register;
  const navigate = useNavigate?.() || (() => {});

  const [formData, setFormData] = useState({
    nombre: '',
    email: '',
    password: '',
    confirmPassword: '',
    acepto_tratamiento: false,
  });

  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value,
    }));
    if (error) setError(null);
  };

  const handleRegisterSubmit = async (e) => {
    e.preventDefault();
    if (!formData.nombre.trim()) {
      setError('Por favor ingresa tu nombre completo.');
      return;
    }
    if (!formData.email.trim()) {
      setError('Por favor ingresa un correo electrónico válido.');
      return;
    }
    if (formData.password.length < 8) {
      setError('La contraseña debe tener al menos 8 caracteres.');
      return;
    }
    if (formData.password !== formData.confirmPassword) {
      setError('Las contraseñas no coinciden.');
      return;
    }
    if (!formData.acepto_tratamiento) {
      setError('Debes aceptar el tratamiento de datos personales para continuar.');
      return;
    }

    setLoading(true);
    setError(null);
    try {
      if (register) {
        await register({
          nombre: formData.nombre.trim(),
          email: formData.email.trim(),
          password: formData.password,
          acepto_tratamiento: formData.acepto_tratamiento,
        });
      }
      navigate('/catalogo', { replace: true });
    } catch (err) {
      setError(err.message || 'Error al crear la cuenta.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleRegisterSubmit} className="auth-form">
      {error && (
        <div className="auth-alert error">
          <span>⚠️</span> {error}
        </div>
      )}

      <div className="form-group">
        <label htmlFor="reg-nombre">Nombre y Apellido</label>
        <input
          id="reg-nombre"
          type="text"
          name="nombre"
          placeholder="Ej. Juan Pérez"
          value={formData.nombre}
          onChange={handleChange}
          required
          disabled={loading}
        />
      </div>

      <div className="form-group">
        <label htmlFor="reg-email">Correo Electrónico</label>
        <input
          id="reg-email"
          type="email"
          name="email"
          placeholder="juan@ejemplo.com"
          value={formData.email}
          onChange={handleChange}
          required
          disabled={loading}
        />
      </div>

      <div className="form-group">
        <label htmlFor="reg-password">Contraseña (mínimo 8 caracteres)</label>
        <input
          id="reg-password"
          type="password"
          name="password"
          placeholder="••••••••"
          value={formData.password}
          onChange={handleChange}
          required
          disabled={loading}
        />
      </div>

      <div className="form-group">
        <label htmlFor="reg-confirm">Confirmar Contraseña</label>
        <input
          id="reg-confirm"
          type="password"
          name="confirmPassword"
          placeholder="••••••••"
          value={formData.confirmPassword}
          onChange={handleChange}
          required
          disabled={loading}
        />
      </div>

      <div className="form-checkbox">
        <label>
          <input
            type="checkbox"
            name="acepto_tratamiento"
            checked={formData.acepto_tratamiento}
            onChange={handleChange}
            disabled={loading}
          />
          <span>Acepto el tratamiento de mis datos personales (Ley 25.326)</span>
        </label>
      </div>

      <button
        type="submit"
        className="btn-auth-primary"
        disabled={loading || !formData.acepto_tratamiento}
      >
        {loading ? 'Creando cuenta...' : 'Crear Cuenta'}
      </button>
    </form>
  );
}

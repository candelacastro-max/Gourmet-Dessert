import { useState } from 'react';
import { useAuth } from '../context/AuthContext';
import { useNavigate, useLocation } from 'react-router-dom';

const AuthPage = () => {
  const [isRegister, setIsRegister] = useState(false);
  const { login, register, continueAsGuest } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();

  const [formData, setFormData] = useState({
    nombre: '',
    email: '',
    password: '',
    confirmPassword: '',
    acepto_tratamiento: true,
  });

  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);

  const from = location.state?.from?.pathname || '/catalogo';

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value,
    }));
    if (error) setError(null);
  };

  const handleLoginSubmit = async (e) => {
    e.preventDefault();
    if (!formData.email || !formData.password) {
      setError('Por favor completa todos los campos.');
      return;
    }

    setLoading(true);
    setError(null);
    try {
      await login(formData.email, formData.password);
      navigate(from, { replace: true });
    } catch (err) {
      setError(err.message || 'Error al iniciar sesión. Revisa tus credenciales.');
    } finally {
      setLoading(false);
    }
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
      await register({
        nombre: formData.nombre.trim(),
        email: formData.email.trim(),
        password: formData.password,
        acepto_tratamiento: formData.acepto_tratamiento,
      });
      navigate(from, { replace: true });
    } catch (err) {
      setError(err.message || 'Error al crear la cuenta.');
    } finally {
      setLoading(false);
    }
  };

  const handleGuestAccess = () => {
    continueAsGuest();
    navigate('/catalogo', { replace: true });
  };

  return (
    <div className="auth-wrapper">
      <div className="auth-card">
        <div className="auth-brand">
          <span className="auth-logo-badge">🍰 Gourmet Dessert</span>
          <h2>{isRegister ? 'Crear Cuenta' : 'Iniciar Sesión'}</h2>
          <p className="auth-subtitle">
            {isRegister
              ? 'Regístrate para realizar compras, guardar pedidos y más.'
              : 'Accede a tu cuenta para continuar con tu compra.'}
          </p>
        </div>

        {location.state?.message && !error && (
          <div className="auth-alert info">
            <span>🔒</span> {location.state.message}
          </div>
        )}

        {error && (
          <div className="auth-alert error">
            <span>⚠️</span> {error}
          </div>
        )}

        {isRegister ? (
          <form onSubmit={handleRegisterSubmit} className="auth-form">
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
                <span>Acepto el tratamiento de datos personales (Ley 25.326)</span>
              </label>
            </div>

            <button type="submit" className="btn-auth-primary" disabled={loading}>
              {loading ? 'Creando cuenta...' : 'Crear Cuenta'}
            </button>
          </form>
        ) : (
          <form onSubmit={handleLoginSubmit} className="auth-form">
            <div className="form-group">
              <label htmlFor="login-email">Correo Electrónico</label>
              <input
                id="login-email"
                type="email"
                name="email"
                placeholder="tu@email.com"
                value={formData.email}
                onChange={handleChange}
                required
                disabled={loading}
              />
            </div>

            <div className="form-group">
              <label htmlFor="login-password">Contraseña</label>
              <input
                id="login-password"
                type="password"
                name="password"
                placeholder="••••••••"
                value={formData.password}
                onChange={handleChange}
                required
                disabled={loading}
              />
            </div>

            <button type="submit" className="btn-auth-primary" disabled={loading}>
              {loading ? 'Iniciando sesión...' : 'Ingresar'}
            </button>
          </form>
        )}

        <div className="auth-toggle">
          {isRegister ? (
            <p>
              ¿Ya tienes una cuenta?{' '}
              <button
                type="button"
                className="link-btn"
                onClick={() => {
                  setIsRegister(false);
                  setError(null);
                }}
              >
                Inicia sesión aquí
              </button>
            </p>
          ) : (
            <p>
              ¿No tienes cuenta?{' '}
              <button
                type="button"
                className="link-btn"
                onClick={() => {
                  setIsRegister(true);
                  setError(null);
                }}
              >
                Regístrate aquí
              </button>
            </p>
          )}
        </div>

        <div className="auth-divider">
          <span>O bien</span>
        </div>

        <div className="auth-guest">
          <button
            type="button"
            onClick={handleGuestAccess}
            className="btn-auth-guest"
            disabled={loading}
          >
            <span>👀</span> Continuar como invitado
          </button>
          <p className="auth-guest-note">
            Navega por el catálogo libremente. Para finalizar compras o ver pedidos se te solicitará iniciar sesión.
          </p>
        </div>
      </div>
    </div>
  );
};

export default AuthPage;

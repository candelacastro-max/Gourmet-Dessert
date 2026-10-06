import os

FRONTEND_SRC = r"C:\Users\Profesor\Desktop\Frontend\tienda-frontend\src"

def write(relpath, content):
    fullpath = os.path.join(FRONTEND_SRC, relpath)
    os.makedirs(os.path.dirname(fullpath), exist_ok=True)
    with open(fullpath, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")
    print(f"Written: {fullpath}")

# 1. AuthPage.jsx
auth_page = """import { useState } from 'react';
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
"""

# 2. Navbar.jsx
navbar = """import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { useCart } from '../context/CartContext';

const Navbar = ({ onOpenCart }) => {
  const { user, isAuthenticated, isGuest, logout } = useAuth();
  const { cantidadTotal } = useCart();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  const handleGoToAuth = (register = false) => {
    navigate('/login', { state: { register } });
  };

  return (
    <header className="main-navbar">
      <div className="nav-container">
        <Link to="/catalogo" className="nav-brand">
          <span className="brand-icon">🍰</span>
          <div className="brand-text">
            <span className="brand-title">Gourmet Dessert</span>
            <span className="brand-subtitle">Trampaantojo Store</span>
          </div>
        </Link>

        <nav className="nav-links">
          <Link to="/catalogo" className="nav-link">
            Catálogo
          </Link>

          {isAuthenticated ? (
            <Link to="/pedidos" className="nav-link">
              Mis Pedidos
            </Link>
          ) : (
            <button
              onClick={() => navigate('/login', { state: { message: 'Inicia sesión para ver tu historial de pedidos.' } })}
              className="nav-link-btn"
              title="Disponible solo para usuarios autenticados"
            >
              Mis Pedidos 🔒
            </button>
          )}
        </nav>

        <div className="nav-actions">
          {/* Botón Carrito */}
          <button
            onClick={onOpenCart}
            className="nav-cart-btn"
            aria-label="Abrir carrito"
          >
            <span className="cart-icon">🛒</span>
            <span className="cart-badge">{cantidadTotal}</span>
          </button>

          {/* Estado de Usuario */}
          {isAuthenticated ? (
            <div className="user-profile">
              <div className="user-info">
                <span className="user-name">Hola, {user?.nombre || 'Usuario'}</span>
                <span className="user-role-badge">{user?.rol || 'Cliente'}</span>
              </div>
              <button onClick={handleLogout} className="btn-logout" title="Cerrar sesión">
                Cerrar Sesión
              </button>
            </div>
          ) : isGuest ? (
            <div className="guest-badge-container">
              <span className="guest-pill" title="Permisos restringidos (solo lectura)">
                Modo Invitado
              </span>
              <button onClick={() => handleGoToAuth(false)} className="btn-nav-login">
                Iniciar Sesión
              </button>
            </div>
          ) : (
            <button onClick={() => handleGoToAuth(false)} className="btn-nav-login">
              Ingresar
            </button>
          )}
        </div>
      </div>

      {isGuest && (
        <div className="guest-banner-bar">
          <span>👀 Estás navegando como <strong>Invitado</strong> (Solo lectura). Para comprar o ver pedidos,</span>
          <button onClick={() => handleGoToAuth(false)} className="guest-banner-action">
            Inicia Sesión aquí
          </button>
          <span>o</span>
          <button onClick={() => handleGoToAuth(true)} className="guest-banner-action">
            Regístrate gratis
          </button>
        </div>
      )}
    </header>
  );
};

export default Navbar;
"""

# 3. ProtectedRoute.jsx
protected_route = """import { Navigate, useLocation } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

const ProtectedRoute = ({ children }) => {
  const { isAuthenticated, isLoading } = useAuth();
  const location = useLocation();

  if (isLoading) {
    return (
      <div className="loading-container">
        <div className="spinner"></div>
        <p>Verificando credenciales...</p>
      </div>
    );
  }

  if (!isAuthenticated) {
    return (
      <Navigate
        to="/login"
        state={{
          from: location,
          message: 'Debes iniciar sesión para acceder a esta sección.',
        }}
        replace
      />
    );
  }

  return children;
};

export default ProtectedRoute;
"""

# 4. MisPedidos.jsx
mis_pedidos = """import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { getMisPedidos } from '../services/api';

const MisPedidos = () => {
  const { token, user } = useAuth();
  const [pedidos, setPedidos] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (!token) return;
    setLoading(true);
    getMisPedidos(token)
      .then((data) => setPedidos(data))
      .catch((err) => {
        console.error('Error al cargar pedidos:', err);
        setError('No se pudieron cargar tus pedidos previos.');
      })
      .finally(() => setLoading(false));
  }, [token]);

  return (
    <div className="pedidos-container">
      <div className="pedidos-header">
        <div>
          <h2>📦 Mis Pedidos</h2>
          <p>Historial de compras realizadas por {user?.nombre}</p>
        </div>
        <Link to="/catalogo" className="btn-secondary">
          ← Volver al Catálogo
        </Link>
      </div>

      {loading && (
        <div className="loading-state">
          <div className="spinner"></div>
          <p>Cargando tus pedidos...</p>
        </div>
      )}

      {error && (
        <div className="auth-alert error">
          <span>⚠️</span> {error}
        </div>
      )}

      {!loading && !error && pedidos.length === 0 && (
        <div className="empty-pedidos">
          <span className="empty-icon">🛍️</span>
          <h3>Aún no tienes pedidos registrados</h3>
          <p>Explora nuestro catálogo gourmet y realiza tu primer pedido con tu cuenta.</p>
          <Link to="/catalogo" className="btn-auth-primary" style={{ display: 'inline-block', marginTop: '16px' }}>
            Explorar Catálogo
          </Link>
        </div>
      )}

      {!loading && !error && pedidos.length > 0 && (
        <div className="pedidos-list">
          {pedidos.map((pedido) => (
            <div key={pedido.id} className="pedido-card">
              <div className="pedido-card-header">
                <div>
                  <span className="pedido-id">Pedido #{pedido.id}</span>
                  <span className="pedido-fecha">
                    {pedido.creado_en ? new Date(pedido.creado_en).toLocaleString('es-AR') : 'Fecha no disponible'}
                  </span>
                </div>
                <span className={`pedido-estado estado-${(pedido.estado || 'completado').toLowerCase()}`}>
                  {pedido.estado || 'Completado'}
                </span>
              </div>

              {pedido.items && pedido.items.length > 0 && (
                <div className="pedido-items-table">
                  <table>
                    <thead>
                      <tr>
                        <th>Producto</th>
                        <th>Cant.</th>
                        <th>Precio Unit.</th>
                        <th>Subtotal</th>
                      </tr>
                    </thead>
                    <tbody>
                      {pedido.items.map((item, idx) => (
                        <tr key={idx}>
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
"""

# 5. ProductCard.jsx
product_card = """import { useCart } from '../context/CartContext';
import { useAuth } from '../context/AuthContext';
import { useNavigate } from 'react-router-dom';

const ProductCard = ({ producto }) => {
  const { nombre, precio_final, cuotas_cantidad, cuotas_valor, garantia_meses } = producto;
  const { agregarAlCarrito } = useCart();
  const { isAuthenticated } = useAuth();
  const navigate = useNavigate();

  const handleAddToCart = () => {
    if (!isAuthenticated) {
      const quiereIngresar = window.confirm(
        'Modo Invitado: Para agregar productos al carrito y comprar necesitas una cuenta.\\n\\n¿Deseas iniciar sesión o registrarte ahora?'
      );
      if (quiereIngresar) {
        navigate('/login', {
          state: { message: 'Inicia sesión o crea una cuenta para añadir productos al carrito.' },
        });
      }
      return;
    }
    agregarAlCarrito(producto);
  };

  return (
    <div className="product-card">
      <h3>{nombre}</h3>
      <p className="precio">${Number(precio_final || producto.precio || 0).toLocaleString('es-AR')}</p>

      {cuotas_cantidad > 1 && cuotas_valor && (
        <p className="cuotas">
          {cuotas_cantidad} cuotas de ${Number(cuotas_valor).toLocaleString('es-AR')}
        </p>
      )}

      <p className="garantia">
        Garantía: {garantia_meses > 0 ? `${garantia_meses} meses` : 'Sin garantía'}
      </p>

      <button onClick={handleAddToCart} className="btn-add-cart">
        {isAuthenticated ? 'Agregar al carrito' : 'Agregar (Requiere cuenta) 🔒'}
      </button>
    </div>
  );
};

export default ProductCard;
"""

# 6. Cart.jsx
cart = """import { useState } from 'react';
import { useCart } from '../context/CartContext';
import { useAuth } from '../context/AuthContext';
import { useNavigate } from 'react-router-dom';
import CheckoutModal from './CheckoutModal';

const Cart = ({ isOpen, onClose }) => {
  const { cart, quitarDelCarrito, cantidadTotal, precioTotal } = useCart();
  const { isAuthenticated } = useAuth();
  const navigate = useNavigate();
  const [mostrarCheckout, setMostrarCheckout] = useState(false);

  if (!isOpen) return null;

  const handleProcederCheckout = () => {
    if (!isAuthenticated) {
      onClose();
      navigate('/login', {
        state: { message: 'Debes iniciar sesión para finalizar tu compra.' },
      });
      return;
    }
    setMostrarCheckout(true);
  };

  return (
    <>
      <div className="cart-drawer-overlay" onClick={onClose}>
        <div className="cart-drawer" onClick={(e) => e.stopPropagation()}>
          <div className="cart-drawer-header">
            <h3>🛒 Carrito de Compras ({cantidadTotal})</h3>
            <button onClick={onClose} className="btn-close-drawer">✕</button>
          </div>

          {cart.length === 0 ? (
            <div className="cart-empty-drawer">
              <span className="empty-cart-icon">🛒</span>
              <p>Tu carrito está vacío.</p>
              <button onClick={onClose} className="btn-auth-primary" style={{ marginTop: '12px' }}>
                Explorar Productos
              </button>
            </div>
          ) : (
            <>
              <ul className="cart-items-list">
                {cart.map((item) => (
                  <li key={item.id} className="cart-item-row">
                    <div className="cart-item-info">
                      <span className="cart-item-name">{item.nombre}</span>
                      <span className="cart-item-sub">
                        {item.cantidad} x ${Number(item.precio_final || item.precio || 0).toLocaleString('es-AR')}
                      </span>
                    </div>
                    <div className="cart-item-actions">
                      <span className="cart-item-total">
                        ${Number((item.precio_final || item.precio || 0) * item.cantidad).toLocaleString('es-AR')}
                      </span>
                      <button
                        onClick={() => quitarDelCarrito(item.id)}
                        className="btn-item-remove"
                        title="Quitar"
                      >
                        🗑️
                      </button>
                    </div>
                  </li>
                ))}
              </ul>

              <div className="cart-drawer-footer">
                <div className="cart-total-row">
                  <span>Total estimado:</span>
                  <strong>${precioTotal.toLocaleString('es-AR')}</strong>
                </div>

                {!isAuthenticated && (
                  <div className="cart-guest-warning">
                    ⚠️ Estás en modo invitado. Debes iniciar sesión para comprar.
                  </div>
                )}

                <button
                  onClick={handleProcederCheckout}
                  className="btn-checkout-primary"
                >
                  {isAuthenticated ? 'Finalizar Compra 🛍️' : 'Iniciar Sesión para Comprar 🔒'}
                </button>
              </div>
            </>
          )}
        </div>
      </div>

      {mostrarCheckout && (
        <CheckoutModal onClose={() => setMostrarCheckout(false)} />
      )}
    </>
  );
};

export default Cart;
"""

# 7. App.jsx
app_jsx = """import { useState } from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider, useAuth } from './context/AuthContext';
import { CartProvider } from './context/CartContext';
import AuthPage from './pages/AuthPage';
import Navbar from './components/Navbar';
import Catalogo from './components/Catalogo';
import Cart from './components/Cart';
import MisPedidos from './components/MisPedidos';
import ProtectedRoute from './components/ProtectedRoute';
import './App.css';

// Componente para proteger o redirigir la raíz inicial
const RootRedirect = () => {
  const { isAuthenticated, isGuest, isLoading } = useAuth();

  if (isLoading) {
    return (
      <div className="loading-screen">
        <div className="spinner"></div>
        <p>Cargando tienda...</p>
      </div>
    );
  }

  // Si no está autenticado ni seleccionó continuar como invitado,
  // la vista inicial obligatoria es Login / Registro
  if (!isAuthenticated && !isGuest) {
    return <Navigate to="/login" replace />;
  }

  return <Navigate to="/catalogo" replace />;
};

// Componente para la página de Login
const LoginPageWrapper = () => {
  const { isAuthenticated, isLoading } = useAuth();

  if (isLoading) {
    return (
      <div className="loading-screen">
        <div className="spinner"></div>
      </div>
    );
  }

  // Si ya tiene sesión activa iniciada, redirigir al catálogo
  if (isAuthenticated) {
    return <Navigate to="/catalogo" replace />;
  }

  return <AuthPage />;
};

// Layout principal para la navegación de la tienda
const MainLayout = ({ children }) => {
  const [isCartOpen, setIsCartOpen] = useState(false);

  return (
    <div className="app-shell">
      <Navbar onOpenCart={() => setIsCartOpen(true)} />
      <main className="main-content">{children}</main>
      <Cart isOpen={isCartOpen} onClose={() => setIsCartOpen(false)} />
    </div>
  );
};

function App() {
  return (
    <AuthProvider>
      <CartProvider>
        <BrowserRouter>
          <Routes>
            {/* Redirección inicial obligatoria */}
            <Route path="/" element={<RootRedirect />} />

            {/* Pantalla obligatoria de Login y Registro */}
            <Route path="/login" element={<LoginPageWrapper />} />

            {/* Catálogo: accesible tanto por usuarios autenticados como por invitados */}
            <Route
              path="/catalogo"
              element={
                <MainLayout>
                  <Catalogo />
                </MainLayout>
              }
            />

            {/* Mis Pedidos: ruta privada protegida */}
            <Route
              path="/pedidos"
              element={
                <ProtectedRoute>
                  <MainLayout>
                    <MisPedidos />
                  </MainLayout>
                </ProtectedRoute>
              }
            />

            {/* Fallback */}
            <Route path="*" element={<Navigate to="/" replace />} />
          </Routes>
        </BrowserRouter>
      </CartProvider>
    </AuthProvider>
  );
}

export default App;
"""

# 8. App.css
app_css = """/* Estilos globales y reset */
:root {
  --primary: #9333ea;
  --primary-hover: #7e22ce;
  --primary-light: #f3e8ff;
  --bg-gradient: linear-gradient(135deg, #0f172a 0%, #1e1b4b 50%, #2e1065 100%);
  --surface: #ffffff;
  --surface-alt: #f8fafc;
  --border-color: #e2e8f0;
  --text-primary: #0f172a;
  --text-secondary: #64748b;
  --accent: #ec4899;
  --danger: #ef4444;
  --success: #10b981;
  --warning: #f59e0b;
  --radius: 12px;
  --shadow-sm: 0 1px 2px 0 rgb(0 0 0 / 0.05);
  --shadow-md: 0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1);
  --shadow-xl: 0 20px 25px -5px rgb(0 0 0 / 0.1), 0 8px 10px -6px rgb(0 0 0 / 0.1);
}

* {
  box-sizing: border-box;
}

body {
  margin: 0;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
  background-color: #f8fafc;
  color: var(--text-primary);
  -webkit-font-smoothing: antialiased;
}

/* Pantalla de Carga */
.loading-screen, .loading-container {
  min-height: 80vh;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 16px;
  color: var(--text-secondary);
}

.spinner {
  width: 40px;
  height: 40px;
  border: 4px solid var(--border-color);
  border-top-color: var(--primary);
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

/* AUTH WRAPPER Y TARJETA */
.auth-wrapper {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 24px 16px;
  background: var(--bg-gradient);
}

.auth-card {
  width: 100%;
  max-width: 440px;
  background: #ffffff;
  border-radius: 20px;
  box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.35);
  padding: 36px 32px;
  animation: fadeIn 0.3s ease-out;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(12px); }
  to { opacity: 1; transform: translateY(0); }
}

.auth-brand {
  text-align: center;
  margin-bottom: 24px;
}

.auth-logo-badge {
  display: inline-block;
  background: var(--primary-light);
  color: var(--primary);
  font-size: 13px;
  font-weight: 700;
  padding: 6px 14px;
  border-radius: 9999px;
  margin-bottom: 12px;
  letter-spacing: 0.5px;
}

.auth-brand h2 {
  margin: 0;
  font-size: 26px;
  font-weight: 800;
  color: #0f172a;
}

.auth-subtitle {
  color: var(--text-secondary);
  font-size: 14px;
  margin-top: 8px;
  line-height: 1.4;
}

.auth-alert {
  padding: 12px 16px;
  border-radius: 8px;
  font-size: 14px;
  margin-bottom: 20px;
  display: flex;
  align-items: center;
  gap: 10px;
}

.auth-alert.error {
  background: #fef2f2;
  border: 1px solid #fecaca;
  color: #b91c1c;
}

.auth-alert.info {
  background: #eff6ff;
  border: 1px solid #bfdbfe;
  color: #1d4ed8;
}

.auth-form {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 6px;
  text-align: left;
}

.form-group label {
  font-size: 13px;
  font-weight: 600;
  color: #334155;
}

.form-group input {
  padding: 11px 14px;
  border-radius: 8px;
  border: 1.5px solid var(--border-color);
  font-size: 14px;
  outline: none;
  transition: all 0.2s;
  background: #fff;
  color: #0f172a;
}

.form-group input:focus {
  border-color: var(--primary);
  box-shadow: 0 0 0 3px rgba(147, 51, 234, 0.15);
}

.form-checkbox {
  text-align: left;
}

.form-checkbox label {
  display: flex;
  align-items: flex-start;
  gap: 10px;
  font-size: 12px;
  color: #475569;
  cursor: pointer;
  line-height: 1.35;
}

.form-checkbox input[type="checkbox"] {
  margin-top: 2px;
  accent-color: var(--primary);
  width: 16px;
  height: 16px;
}

.btn-auth-primary {
  background: var(--primary);
  color: #fff;
  border: none;
  padding: 13px 20px;
  border-radius: 8px;
  font-size: 15px;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.2s;
  margin-top: 4px;
}

.btn-auth-primary:hover:not(:disabled) {
  background: var(--primary-hover);
  transform: translateY(-1px);
}

.btn-auth-primary:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.auth-toggle {
  text-align: center;
  margin-top: 18px;
  font-size: 14px;
  color: var(--text-secondary);
}

.link-btn {
  background: none;
  border: none;
  color: var(--primary);
  font-weight: 700;
  cursor: pointer;
  padding: 0;
  font-size: 14px;
  text-decoration: underline;
}

.link-btn:hover {
  color: var(--primary-hover);
}

.auth-divider {
  position: relative;
  text-align: center;
  margin: 22px 0;
}

.auth-divider::before {
  content: '';
  position: absolute;
  top: 50%;
  left: 0;
  right: 0;
  height: 1px;
  background: var(--border-color);
}

.auth-divider span {
  position: relative;
  background: #ffffff;
  padding: 0 12px;
  font-size: 12px;
  color: #94a3b8;
  text-transform: uppercase;
  font-weight: 600;
}

.auth-guest {
  display: flex;
  flex-direction: column;
  gap: 8px;
  text-align: center;
}

.btn-auth-guest {
  background: #f8fafc;
  color: #1e293b;
  border: 1.5px solid #cbd5e1;
  padding: 12px 20px;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
}

.btn-auth-guest:hover {
  background: #f1f5f9;
  border-color: #94a3b8;
  transform: translateY(-1px);
}

.auth-guest-note {
  font-size: 11.5px;
  color: #64748b;
  line-height: 1.35;
  margin: 0;
}

/* NAVBAR */
.main-navbar {
  position: sticky;
  top: 0;
  z-index: 100;
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  border-bottom: 1px solid var(--border-color);
  box-shadow: var(--shadow-sm);
}

.nav-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 12px 24px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
}

.nav-brand {
  display: flex;
  align-items: center;
  gap: 10px;
  text-decoration: none;
  color: var(--text-primary);
}

.brand-icon {
  font-size: 28px;
}

.brand-title {
  display: block;
  font-size: 18px;
  font-weight: 800;
  letter-spacing: -0.5px;
  color: #0f172a;
}

.brand-subtitle {
  display: block;
  font-size: 11px;
  color: var(--text-secondary);
  font-weight: 500;
}

.nav-links {
  display: flex;
  align-items: center;
  gap: 16px;
}

.nav-link {
  color: #334155;
  text-decoration: none;
  font-weight: 600;
  font-size: 14px;
  padding: 6px 12px;
  border-radius: 6px;
  transition: all 0.2s;
}

.nav-link:hover {
  color: var(--primary);
  background: var(--primary-light);
}

.nav-link-btn {
  background: none;
  border: none;
  color: #94a3b8;
  font-weight: 600;
  font-size: 14px;
  padding: 6px 12px;
  cursor: pointer;
  transition: all 0.2s;
}

.nav-link-btn:hover {
  color: var(--primary);
}

.nav-actions {
  display: flex;
  align-items: center;
  gap: 14px;
}

.nav-cart-btn {
  position: relative;
  background: #f1f5f9;
  border: 1px solid var(--border-color);
  border-radius: 8px;
  padding: 8px 12px;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 6px;
  transition: all 0.2s;
}

.nav-cart-btn:hover {
  background: #e2e8f0;
}

.cart-icon {
  font-size: 18px;
}

.cart-badge {
  background: var(--primary);
  color: #fff;
  font-size: 12px;
  font-weight: 700;
  padding: 2px 7px;
  border-radius: 9999px;
}

.user-profile {
  display: flex;
  align-items: center;
  gap: 12px;
}

.user-info {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
}

.user-name {
  font-size: 13.5px;
  font-weight: 700;
  color: #0f172a;
}

.user-role-badge {
  font-size: 11px;
  color: var(--primary);
  background: var(--primary-light);
  padding: 2px 8px;
  border-radius: 9999px;
  font-weight: 600;
  text-transform: capitalize;
}

.btn-logout {
  background: #fee2e2;
  color: #dc2626;
  border: none;
  padding: 7px 12px;
  border-radius: 6px;
  font-size: 13px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-logout:hover {
  background: #fca5a5;
}

.guest-badge-container {
  display: flex;
  align-items: center;
  gap: 8px;
}

.guest-pill {
  background: #fef3c7;
  color: #b45309;
  font-size: 12px;
  font-weight: 700;
  padding: 5px 10px;
  border-radius: 9999px;
}

.btn-nav-login {
  background: var(--primary);
  color: #fff;
  border: none;
  padding: 7px 14px;
  border-radius: 6px;
  font-size: 13px;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-nav-login:hover {
  background: var(--primary-hover);
}

.guest-banner-bar {
  background: #fffbeb;
  border-top: 1px solid #fde68a;
  border-bottom: 1px solid #fde68a;
  padding: 8px 16px;
  text-align: center;
  font-size: 13px;
  color: #92400e;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  flex-wrap: wrap;
}

.guest-banner-action {
  background: none;
  border: none;
  color: #b45309;
  font-weight: 700;
  text-decoration: underline;
  cursor: pointer;
  padding: 0;
  font-size: 13px;
}

/* MAIN CONTENT */
.main-content {
  max-width: 1200px;
  margin: 0 auto;
  padding: 32px 20px;
  min-height: calc(100vh - 120px);
}

/* PRODUCT CARD & CATALOG GRID */
.catalogo-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(270px, 1fr));
  gap: 24px;
  margin-top: 24px;
}

.product-card {
  background: #ffffff;
  border: 1px solid var(--border-color);
  border-radius: 16px;
  padding: 24px;
  display: flex;
  flex-direction: column;
  gap: 12px;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  box-shadow: var(--shadow-sm);
  position: relative;
  overflow: hidden;
}

.product-card:hover {
  transform: translateY(-4px);
  box-shadow: var(--shadow-md);
  border-color: #cbd5e1;
}

.product-card h3 {
  font-size: 18px;
  font-weight: 700;
  margin: 0;
  color: #0f172a;
}

.product-card .precio {
  font-size: 26px;
  font-weight: 800;
  color: var(--primary);
  margin: 4px 0;
}

.product-card .cuotas {
  font-size: 13px;
  color: #1e293b;
  background: #f3e8ff;
  padding: 4px 10px;
  border-radius: 6px;
  font-weight: 600;
  align-self: flex-start;
}

.product-card .garantia {
  font-size: 13px;
  color: var(--text-secondary);
  margin-top: auto;
  padding-top: 12px;
  border-top: 1px dashed var(--border-color);
}

.btn-add-cart {
  background: #0f172a;
  color: #ffffff;
  border: none;
  padding: 12px 16px;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-add-cart:hover {
  background: var(--primary);
}

/* CART DRAWER */
.cart-drawer-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.5);
  backdrop-filter: blur(4px);
  z-index: 1000;
  display: flex;
  justify-content: flex-end;
  animation: fadeIn 0.2s ease-out;
}

.cart-drawer {
  background: #ffffff;
  width: 100%;
  max-width: 420px;
  height: 100%;
  display: flex;
  flex-direction: column;
  box-shadow: var(--shadow-xl);
  animation: slideLeft 0.25s cubic-bezier(0.16, 1, 0.3, 1);
}

@keyframes slideLeft {
  from { transform: translateX(100%); }
  to { transform: translateX(0); }
}

.cart-drawer-header {
  padding: 20px 24px;
  border-bottom: 1px solid var(--border-color);
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.cart-drawer-header h3 {
  margin: 0;
  font-size: 18px;
  font-weight: 700;
}

.btn-close-drawer {
  background: none;
  border: none;
  font-size: 20px;
  cursor: pointer;
  color: var(--text-secondary);
}

.cart-items-list {
  list-style: none;
  padding: 16px 24px;
  margin: 0;
  flex: 1;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.cart-item-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-bottom: 12px;
  border-bottom: 1px solid var(--border-color);
}

.cart-item-name {
  display: block;
  font-weight: 600;
  font-size: 14.5px;
  color: #0f172a;
}

.cart-item-sub {
  font-size: 13px;
  color: var(--text-secondary);
}

.cart-item-actions {
  display: flex;
  align-items: center;
  gap: 12px;
}

.cart-item-total {
  font-weight: 700;
  font-size: 15px;
  color: #0f172a;
}

.btn-item-remove {
  background: none;
  border: none;
  cursor: pointer;
  padding: 4px;
  font-size: 16px;
}

.cart-drawer-footer {
  padding: 20px 24px;
  border-top: 1px solid var(--border-color);
  background: #f8fafc;
}

.cart-total-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 16px;
  margin-bottom: 16px;
}

.cart-total-row strong {
  font-size: 22px;
  color: var(--primary);
}

.cart-guest-warning {
  background: #fffbeb;
  border: 1px solid #fde68a;
  color: #92400e;
  padding: 8px 12px;
  border-radius: 6px;
  font-size: 12.5px;
  margin-bottom: 12px;
}

.btn-checkout-primary {
  width: 100%;
  background: var(--success);
  color: #fff;
  border: none;
  padding: 14px 20px;
  border-radius: 8px;
  font-size: 15px;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-checkout-primary:hover {
  filter: brightness(0.95);
  transform: translateY(-1px);
}

.cart-empty-drawer {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 40px;
  text-align: center;
  color: var(--text-secondary);
}

.empty-cart-icon {
  font-size: 48px;
  margin-bottom: 12px;
  opacity: 0.5;
}

/* MIS PEDIDOS */
.pedidos-container {
  max-width: 860px;
  margin: 0 auto;
}

.pedidos-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 28px;
}

.pedidos-header h2 {
  margin: 0;
  font-size: 26px;
  font-weight: 800;
}

.pedidos-header p {
  color: var(--text-secondary);
  font-size: 14px;
  margin-top: 4px;
}

.btn-secondary {
  display: inline-block;
  background: #ffffff;
  color: #1e293b;
  border: 1px solid var(--border-color);
  padding: 8px 16px;
  border-radius: 8px;
  text-decoration: none;
  font-size: 13.5px;
  font-weight: 600;
  transition: all 0.2s;
}

.btn-secondary:hover {
  background: #f1f5f9;
}

.pedido-card {
  background: #ffffff;
  border: 1px solid var(--border-color);
  border-radius: 12px;
  padding: 20px;
  margin-bottom: 16px;
  box-shadow: var(--shadow-sm);
}

.pedido-card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
  padding-bottom: 12px;
  border-bottom: 1px solid var(--border-color);
}

.pedido-id {
  font-size: 16px;
  font-weight: 700;
  display: block;
}

.pedido-fecha {
  font-size: 12.5px;
  color: var(--text-secondary);
}

.pedido-estado {
  font-size: 12px;
  font-weight: 700;
  padding: 4px 10px;
  border-radius: 9999px;
}

.estado-completado {
  background: #dcfce7;
  color: #15803d;
}

.estado-pendiente {
  background: #fef3c7;
  color: #b45309;
}

.pedido-items-table {
  width: 100%;
  margin-bottom: 16px;
  overflow-x: auto;
}

.pedido-items-table table {
  width: 100%;
  border-collapse: collapse;
  font-size: 13.5px;
}

.pedido-items-table th {
  text-align: left;
  padding: 8px;
  color: var(--text-secondary);
  border-bottom: 1px solid var(--border-color);
}

.pedido-items-table td {
  padding: 10px 8px;
  border-bottom: 1px solid #f1f5f9;
}

.pedido-card-footer {
  display: flex;
  justify-content: flex-end;
  align-items: center;
  gap: 12px;
  font-size: 15px;
}

.pedido-card-footer strong {
  font-size: 20px;
  color: var(--primary);
}

.empty-pedidos {
  background: #ffffff;
  border: 1px dashed var(--border-color);
  border-radius: 16px;
  padding: 48px 24px;
  text-align: center;
}

.empty-icon {
  font-size: 56px;
  display: block;
  margin-bottom: 12px;
}
"""

write("pages/AuthPage.jsx", auth_page)
write("components/Navbar.jsx", navbar)
write("components/ProtectedRoute.jsx", protected_route)
write("components/MisPedidos.jsx", mis_pedidos)
write("components/ProductCard.jsx", product_card)
write("components/Cart.jsx", cart)
write("App.jsx", app_jsx)
write("App.css", app_css)
print("ALL FILES WRITTEN SUCCESSFULLY")

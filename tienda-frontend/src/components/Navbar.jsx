import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { useCarrito } from '../context/CarritoContext';

const Navbar = () => {
  const { user, isAuthenticated, isGuest, logout } = useAuth();
  const { cantidadTotal } = useCarrito();
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
            <span className="brand-subtitle">Pastelería & Delicias</span>
          </div>
        </Link>

        <nav className="nav-links">
          <Link to="/catalogo" className="nav-link">
            Catálogo
          </Link>

          {/* Enlace en el Navbar a /mis-pedidos visible solo con sesión iniciada */}
          {isAuthenticated && (
            <>
              <Link to="/mis-pedidos" className="nav-link">
                Mis Pedidos
              </Link>
              <Link to="/mis-datos" className="nav-link">
                Mis Datos
              </Link>
            </>
          )}
        </nav>

        <div className="nav-actions">
          {/* Botón Carrito que lleva a /carrito */}
          <Link to="/carrito" className="nav-cart-btn" aria-label="Ver carrito">
            <span className="cart-icon">🛒</span>
            <span className="cart-badge">{cantidadTotal}</span>
          </Link>

          {/* Estado de Usuario */}
          {isAuthenticated ? (
            <div className="user-profile">
              <div className="user-info">
                <span className="user-name">Hola, {user?.nombre || user?.email || 'Usuario'}</span>
                <span className={`user-role-badge ${user?.rol === 'admin' ? 'badge-admin' : ''}`}>
                  {user?.rol === 'admin' ? '👑 Admin' : (user?.rol || 'Cliente')}
                </span>
              </div>
              <button onClick={handleLogout} className="btn-logout" title="Cerrar sesión">
                Cerrar Sesión
              </button>
            </div>
          ) : isGuest ? (
            <div className="guest-badge-container">
              <span className="guest-pill" title="Modo Invitado">
                Invitado
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
    </header>
  );
};

export default Navbar;

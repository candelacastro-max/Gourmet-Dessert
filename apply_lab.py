import os

FRONTEND_SRC = r"C:\Users\Profesor\Desktop\Frontend\tienda-frontend\src"

def write(relpath, content):
    fullpath = os.path.join(FRONTEND_SRC, relpath)
    os.makedirs(os.path.dirname(fullpath), exist_ok=True)
    with open(fullpath, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")
    print(f"Written: {fullpath}")

# 1. CarritoContext.jsx
carrito_context = """import { createContext, useContext, useState, useEffect } from 'react';

const CarritoContext = createContext();

export const useCarrito = () => {
  const context = useContext(CarritoContext);
  if (!context) {
    throw new Error('useCarrito debe ser usado dentro de un CarritoProvider');
  }
  return context;
};

export const CarritoProvider = ({ children }) => {
  // 1.2 Inicializar leyendo de localStorage con useState y una función envuelta en try/catch
  const [items, setItems] = useState(() => {
    try {
      const guardado = localStorage.getItem('carrito');
      return guardado ? JSON.parse(guardado) : [];
    } catch (error) {
      console.error('JSON roto o inválido en localStorage (carrito). Iniciando con carrito vacío:', error);
      return [];
    }
  });

  // 1.3 useEffect que guarda el carrito en localStorage cada vez que cambie
  useEffect(() => {
    try {
      localStorage.setItem('carrito', JSON.stringify(items));
    } catch (error) {
      console.error('Error al guardar el carrito en localStorage:', error);
    }
  }, [items]);

  // 1.4 agregar(producto, cantidad): si ya está en el carrito suma cantidad, no agrega fila repetida
  const agregar = (producto, cantidad = 1) => {
    const idProducto = Number(producto.producto_id ?? producto.id);
    const cant = Number(cantidad) > 0 ? Number(cantidad) : 1;

    setItems((prevItems) => {
      const index = prevItems.findIndex(
        (item) => Number(item.producto_id ?? item.id) === idProducto
      );

      if (index !== -1) {
        return prevItems.map((item, i) =>
          i === index
            ? { ...item, cantidad: item.cantidad + cant }
            : item
        );
      }

      return [
        ...prevItems,
        {
          ...producto,
          id: idProducto,
          producto_id: idProducto,
          cantidad: cant,
        },
      ];
    });
  };

  // 1.5 quitar(producto_id)
  const quitar = (producto_id) => {
    const targetId = Number(producto_id);
    setItems((prevItems) =>
      prevItems.filter((item) => Number(item.producto_id ?? item.id) !== targetId)
    );
  };

  // 1.5 vaciar()
  const vaciar = () => {
    setItems([]);
  };

  // 1.5 total calculado con reduce
  const total = items.reduce((acc, item) => {
    const precio = Number(item.precio_final ?? item.precio ?? 0);
    return acc + precio * item.cantidad;
  }, 0);

  // Cantidad total de productos en unidades
  const cantidadTotal = items.reduce((acc, item) => acc + item.cantidad, 0);

  const value = {
    items,
    agregar,
    quitar,
    vaciar,
    total,
    cantidadTotal,
    // Alias de compatibilidad
    cart: items,
    agregarAlCarrito: agregar,
    quitarDelCarrito: quitar,
    vaciarCarrito: vaciar,
    precioTotal: total,
  };

  return (
    <CarritoContext.Provider value={value}>
      {children}
    </CarritoContext.Provider>
  );
};

export default CarritoContext;
"""
write("context/CarritoContext.jsx", carrito_context)

# 2. CartContext.jsx (compatibilidad)
cart_context_compat = """export { CarritoContext as default, CarritoProvider as CartProvider, useCarrito as useCart, CarritoProvider, useCarrito } from './CarritoContext';
"""
write("context/CartContext.jsx", cart_context_compat)

# 3. api.js
api_js = """const BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

// Función para obtener headers con autenticación leyendo access_token
export function authHeaders() {
  const token = localStorage.getItem('access_token');
  const headers = {
    'Content-Type': 'application/json',
  };
  if (token) {
    headers['Authorization'] = `Bearer ${token}`;
  }
  return headers;
}

// Parte 2.3: manejarRespuesta(res) con los 3 casos:
// 401 traducido, 409 con detail tal como viene del backend, y un mensaje genérico para el resto
export async function manejarRespuesta(res) {
  if (res.ok) {
    if (res.status === 204) return null;
    return await res.json();
  }

  // 1. Caso 401: traducido
  if (res.status === 401) {
    throw new Error('La sesión venció o no es válida. Por favor, iniciá sesión nuevamente.');
  }

  // 2. Caso 409: mostrando el detail tal como viene del backend
  if (res.status === 409) {
    const data = await res.json().catch(() => ({}));
    throw new Error(data.detail || 'Conflicto con el stock del producto.');
  }

  // 3. Caso resto: mensaje genérico
  let mensajeGenerico = 'Algo salió mal al procesar la solicitud.';
  try {
    const data = await res.json();
    if (data?.detail) {
      if (typeof data.detail === 'string') {
        mensajeGenerico = data.detail;
      } else if (Array.isArray(data.detail)) {
        mensajeGenerico = data.detail.map((d) => d.msg || JSON.stringify(d)).join(', ');
      }
    }
  } catch {
    // mantiene el genérico
  }
  throw new Error(mensajeGenerico);
}

export async function getProductos({ page = 0, limit = 10, nombre = '' } = {}) {
  const params = new URLSearchParams({ page, limit });
  if (nombre) params.set('nombre', nombre);
  const res = await fetch(`${BASE_URL}/productos?${params}`);
  return manejarRespuesta(res);
}

export async function loginUser(email, password) {
  const formData = new URLSearchParams();
  formData.append('username', email);
  formData.append('password', password);

  const res = await fetch(`${BASE_URL}/auth/login`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded',
    },
    body: formData.toString(),
  });

  return manejarRespuesta(res);
}

export async function registerUser({ nombre, email, password, acepto_tratamiento = true }) {
  const res = await fetch(`${BASE_URL}/auth/register`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      nombre,
      email,
      password,
      acepto_tratamiento,
    }),
  });

  return manejarRespuesta(res);
}

export async function getMe(token) {
  const headers = token ? { Authorization: `Bearer ${token}` } : authHeaders();
  const res = await fetch(`${BASE_URL}/auth/me`, { headers });
  return manejarRespuesta(res);
}

// Parte 4.1: getMisPedidos() con authHeaders()
export async function getMisPedidos() {
  const res = await fetch(`${BASE_URL}/pedidos/mios`, {
    method: 'GET',
    headers: authHeaders(),
  });
  return manejarRespuesta(res);
}

// Parte 2.2: crearPedido(items)
// Con map que deja solo producto_id y cantidad:
// { "items": [ {"producto_id": 3, "cantidad": 2}, {"producto_id": 7, "cantidad": 1} ] }
export async function crearPedido(items) {
  const payload = {
    items: items.map((item) => ({
      producto_id: Number(item.producto_id ?? item.id),
      cantidad: Number(item.cantidad),
    })),
  };

  const res = await fetch(`${BASE_URL}/pedidos/`, {
    method: 'POST',
    headers: authHeaders(),
    body: JSON.stringify(payload),
  });

  return manejarRespuesta(res);
}
"""
write("services/api.js", api_js)

# 4. AuthContext.jsx
auth_context = """import { createContext, useContext, useState, useEffect } from 'react';
import { loginUser, registerUser, getMe } from '../services/api';

const AuthContext = createContext();

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth debe ser usado dentro de un AuthProvider');
  }
  return context;
};

export const AuthProvider = ({ children }) => {
  const [token, setToken] = useState(() => localStorage.getItem('access_token') || localStorage.getItem('token'));
  const [user, setUser] = useState(null);
  const [isGuest, setIsGuest] = useState(() => localStorage.getItem('isGuest') === 'true');
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const initAuth = async () => {
      const storedToken = localStorage.getItem('access_token') || localStorage.getItem('token');
      if (storedToken) {
        try {
          const userData = await getMe(storedToken);
          setUser(userData);
          setToken(storedToken);
          setIsGuest(false);
          localStorage.removeItem('isGuest');
        } catch (err) {
          console.error('Token inválido o expirado:', err);
          localStorage.removeItem('access_token');
          localStorage.removeItem('token');
          setToken(null);
          setUser(null);
        }
      }
      setIsLoading(false);
    };

    initAuth();
  }, []);

  const login = async (email, password) => {
    setIsLoading(true);
    try {
      const tokenData = await loginUser(email, password);
      const accessToken = tokenData.access_token;
      localStorage.setItem('access_token', accessToken);
      localStorage.setItem('token', accessToken);
      localStorage.removeItem('isGuest');
      setToken(accessToken);
      setIsGuest(false);

      const userData = await getMe(accessToken);
      setUser(userData);
      return userData;
    } finally {
      setIsLoading(false);
    }
  };

  const register = async ({ nombre, email, password, acepto_tratamiento = true }) => {
    setIsLoading(true);
    try {
      await registerUser({ nombre, email, password, acepto_tratamiento });
      const tokenData = await loginUser(email, password);
      const accessToken = tokenData.access_token;
      localStorage.setItem('access_token', accessToken);
      localStorage.setItem('token', accessToken);
      localStorage.removeItem('isGuest');
      setToken(accessToken);
      setIsGuest(false);

      const userData = await getMe(accessToken);
      setUser(userData);
      return userData;
    } finally {
      setIsLoading(false);
    }
  };

  const continueAsGuest = () => {
    localStorage.removeItem('access_token');
    localStorage.removeItem('token');
    localStorage.setItem('isGuest', 'true');
    setToken(null);
    setUser(null);
    setIsGuest(true);
  };

  const logout = () => {
    localStorage.removeItem('access_token');
    localStorage.removeItem('token');
    localStorage.removeItem('isGuest');
    setToken(null);
    setUser(null);
    setIsGuest(false);
  };

  const value = {
    user,
    token,
    isGuest,
    isLoading,
    isAuthenticated: !!user && !!token,
    login,
    register,
    continueAsGuest,
    logout,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};
"""
write("context/AuthContext.jsx", auth_context)

# 5. ProductCard.jsx
product_card = """import { useState } from 'react';
import { useCarrito } from '../context/CarritoContext';

const ProductCard = ({ producto }) => {
  const { nombre, precio_final, precio, stock, cuotas_cantidad, cuotas_valor, garantia_meses } = producto;
  const { agregar } = useCarrito();
  const [agregado, setAgregado] = useState(false);

  const precioMostrar = Number(precio_final || precio || 0);

  const handleAddToCart = () => {
    agregar(producto, 1);
    setAgregado(true);
    setTimeout(() => setAgregado(false), 1200);
  };

  const sinStock = stock <= 0;

  return (
    <div className="product-card">
      <div className="product-card-top">
        <h3>{nombre}</h3>
        <span className={`stock-badge ${sinStock ? 'sin-stock' : 'con-stock'}`}>
          {sinStock ? 'Sin stock' : `${stock} disponibles`}
        </span>
      </div>

      <p className="precio">${precioMostrar.toLocaleString('es-AR')}</p>

      {cuotas_cantidad > 1 && cuotas_valor && (
        <p className="cuotas">
          {cuotas_cantidad} cuotas de ${Number(cuotas_valor).toLocaleString('es-AR')}
        </p>
      )}

      <p className="garantia">
        Garantía: {garantia_meses > 0 ? `${garantia_meses} meses` : 'Sin garantía'}
      </p>

      <button
        onClick={handleAddToCart}
        disabled={sinStock}
        className={`btn-add-cart ${agregado ? 'btn-agregado' : ''}`}
      >
        {sinStock ? 'Agotado' : agregado ? '✓ ¡Agregado!' : 'Agregar al carrito'}
      </button>
    </div>
  );
};

export default ProductCard;
"""
write("components/ProductCard.jsx", product_card)

# 6. Carrito.jsx (Página /carrito)
carrito_page = """import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useCarrito } from '../context/CarritoContext';
import { crearPedido } from '../services/api';

const Carrito = () => {
  const { items, quitar, vaciar, total } = useCarrito();
  const [enviando, setEnviando] = useState(false);
  const [error, setError] = useState(null);
  const navigate = useNavigate();

  // Parte 2.4 y 2.5: confirmar() arranca con if (enviando) return, try/catch/finally y estado enviando
  const confirmar = async () => {
    if (enviando) return;
    if (!items || items.length === 0) return;

    setEnviando(true);
    setError(null);

    try {
      await crearPedido(items);
      vaciar();
      navigate('/mis-pedidos');
    } catch (err) {
      console.error('Error al confirmar compra:', err);
      setError(err.message || 'Error al procesar la compra.');
    } finally {
      setEnviando(false);
    }
  };

  return (
    <div className="carrito-page-container">
      <div className="carrito-header">
        <div>
          <h2>🛒 Mi Carrito de Compras</h2>
          <p>Revisá tus postres y delicias antes de confirmar el pedido</p>
        </div>
        <Link to="/catalogo" className="btn-secondary">
          ← Volver al Catálogo
        </Link>
      </div>

      {error && (
        <div className="auth-alert error" style={{ marginBottom: '24px' }}>
          <span>⚠️</span>
          <div>
            <strong>Atención:</strong> {error}
          </div>
        </div>
      )}

      {items.length === 0 ? (
        <div className="empty-pedidos" style={{ margin: '40px 0' }}>
          <span className="empty-icon">🍰</span>
          <h3>Tu carrito está vacío</h3>
          <p>Explora nuestras creaciones y agrega productos para iniciar tu pedido.</p>
          <Link to="/catalogo" className="btn-auth-primary" style={{ display: 'inline-block', marginTop: '16px' }}>
            Explorar Catálogo
          </Link>
        </div>
      ) : (
        <div className="carrito-content-layout">
          <div className="carrito-table-wrapper">
            <table className="carrito-table">
              <thead>
                <tr>
                  <th>Producto</th>
                  <th>Precio Unitario</th>
                  <th>Cantidad</th>
                  <th>Subtotal</th>
                  <th style={{ textAlign: 'center' }}>Acción</th>
                </tr>
              </thead>
              <tbody>
                {items.map((item) => {
                  const idItem = Number(item.producto_id ?? item.id);
                  const precio = Number(item.precio_final ?? item.precio ?? 0);
                  const subtotal = precio * item.cantidad;

                  return (
                    <tr key={idItem}>
                      <td className="carrito-item-nombre">
                        <strong>{item.nombre}</strong>
                      </td>
                      <td>${precio.toLocaleString('es-AR')}</td>
                      <td>
                        <span className="badge-cantidad">{item.cantidad}</span>
                      </td>
                      <td className="carrito-subtotal">
                        ${subtotal.toLocaleString('es-AR')}
                      </td>
                      <td style={{ textAlign: 'center' }}>
                        <button
                          onClick={() => quitar(idItem)}
                          className="btn-item-quitar"
                          title="Quitar del carrito"
                        >
                          🗑️ Quitar
                        </button>
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>

            <div className="carrito-actions-bar">
              <button
                onClick={vaciar}
                className="btn-vaciar-carrito"
                disabled={enviando}
              >
                Vaciar Carrito
              </button>
            </div>
          </div>

          <div className="carrito-summary-card">
            <h3>Resumen de la orden</h3>
            <div className="summary-row">
              <span>Total de unidades:</span>
              <strong>{items.reduce((acc, i) => acc + i.cantidad, 0)}</strong>
            </div>
            <div className="summary-row total-row">
              <span>Total:</span>
              <strong className="summary-total-price">
                ${Number(total).toLocaleString('es-AR')}
              </strong>
            </div>

            {/* Parte 2.5: Botón deshabilitado mientras enviando sea true, cambia texto a 'Confirmando…' */}
            <button
              onClick={confirmar}
              disabled={enviando || items.length === 0}
              className="btn-checkout-primary btn-confirmar-compra"
            >
              {enviando ? 'Confirmando…' : 'Confirmar compra'}
            </button>
          </div>
        </div>
      )}
    </div>
  );
};

export default Carrito;
"""
write("pages/Carrito.jsx", carrito_page)

# 8. RutaProtegida.jsx y ProtectedRoute.jsx
ruta_protegida = """import { Navigate, useLocation } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

export const RutaProtegida = ({ children }) => {
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

export default RutaProtegida;
"""
write("components/RutaProtegida.jsx", ruta_protegida)
write("components/ProtectedRoute.jsx", ruta_protegida)

# 9. MisPedidos.jsx (3 estados: cargando, error, lista vacía; key producto_id)
mis_pedidos = """import { useState, useEffect } from 'react';
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
"""
write("components/MisPedidos.jsx", mis_pedidos)

# 10. Navbar.jsx (link a /mis-pedidos solo autenticado, carrito redirige a /carrito)
navbar = """import { Link, useNavigate } from 'react-router-dom';
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
            <Link to="/mis-pedidos" className="nav-link">
              Mis Pedidos
            </Link>
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
                <span className="user-role-badge">{user?.rol || 'Cliente'}</span>
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
"""
write("components/Navbar.jsx", navbar)

# 11. App.jsx (Envolviendo con CarritoProvider por fuera de las rutas, rutas /carrito y /mis-pedidos)
app_jsx = """import { useState } from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider, useAuth } from './context/AuthContext';
import { CarritoProvider } from './context/CarritoContext';
import AuthPage from './pages/AuthPage';
import Navbar from './components/Navbar';
import Catalogo from './components/Catalogo';
import Carrito from './pages/Carrito';
import MisPedidos from './components/MisPedidos';
import RutaProtegida from './components/RutaProtegida';
import './App.css';

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

  return <Navigate to="/catalogo" replace />;
};

const LoginPageWrapper = () => {
  const { isAuthenticated, isLoading } = useAuth();

  if (isLoading) {
    return (
      <div className="loading-screen">
        <div className="spinner"></div>
      </div>
    );
  }

  if (isAuthenticated) {
    return <Navigate to="/catalogo" replace />;
  }

  return <AuthPage />;
};

const MainLayout = ({ children }) => {
  return (
    <div className="app-shell">
      <Navbar />
      <main className="main-content">{children}</main>
    </div>
  );
};

function App() {
  return (
    <AuthProvider>
      <CarritoProvider>
        <BrowserRouter>
          <Routes>
            <Route path="/" element={<RootRedirect />} />
            <Route path="/login" element={<LoginPageWrapper />} />

            <Route
              path="/catalogo"
              element={
                <MainLayout>
                  <Catalogo />
                </MainLayout>
              }
            />

            {/* Página /carrito */}
            <Route
              path="/carrito"
              element={
                <MainLayout>
                  <Carrito />
                </MainLayout>
              }
            />

            {/* Ruta /mis-pedidos protegida con RutaProtegida */}
            <Route
              path="/mis-pedidos"
              element={
                <RutaProtegida>
                  <MainLayout>
                    <MisPedidos />
                  </MainLayout>
                </RutaProtegida>
              }
            />

            {/* Redirección para compatibilidad */}
            <Route path="/pedidos" element={<Navigate to="/mis-pedidos" replace />} />
            <Route path="*" element={<Navigate to="/catalogo" replace />} />
          </Routes>
        </BrowserRouter>
      </CarritoProvider>
    </AuthProvider>
  );
}

export default App;
"""
write("App.jsx", app_jsx)

# 12. CSS para /carrito
css_addon = """
/* ESTILOS DE LA PÁGINA DEL CARRITO */
.carrito-page-container {
  max-width: 1100px;
  margin: 0 auto;
  padding: 32px 16px 64px 16px;
}

.carrito-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 28px;
  border-bottom: 1px solid var(--border-color);
  padding-bottom: 16px;
}

.carrito-header h2 {
  font-size: 26px;
  font-weight: 800;
  margin: 0 0 6px 0;
  color: var(--text-primary);
}

.carrito-header p {
  margin: 0;
  color: var(--text-secondary);
  font-size: 15px;
}

.carrito-content-layout {
  display: grid;
  grid-template-columns: 1fr 340px;
  gap: 32px;
  align-items: flex-start;
}

@media (max-width: 860px) {
  .carrito-content-layout {
    grid-template-columns: 1fr;
  }
}

.carrito-table-wrapper {
  background: #ffffff;
  border: 1px solid var(--border-color);
  border-radius: var(--radius);
  overflow: hidden;
  box-shadow: var(--shadow-sm);
}

.carrito-table {
  width: 100%;
  border-collapse: collapse;
  text-align: left;
}

.carrito-table th {
  background-color: var(--surface-alt);
  padding: 14px 18px;
  font-size: 13px;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: var(--text-secondary);
  font-weight: 700;
  border-bottom: 1px solid var(--border-color);
}

.carrito-table td {
  padding: 18px;
  border-bottom: 1px solid var(--border-color);
  font-size: 15px;
  vertical-align: middle;
}

.carrito-item-nombre strong {
  color: var(--text-primary);
  font-size: 16px;
}

.badge-cantidad {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  background: var(--primary-light);
  color: var(--primary);
  font-weight: 700;
  font-size: 14px;
  padding: 4px 12px;
  border-radius: 20px;
}

.carrito-subtotal {
  font-weight: 700;
  color: var(--primary);
}

.btn-item-quitar {
  background: #fee2e2;
  color: #b91c1c;
  border: 1px solid #fecaca;
  padding: 6px 12px;
  border-radius: 8px;
  font-weight: 600;
  font-size: 13px;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-item-quitar:hover {
  background: #fca5a5;
  color: #7f1d1d;
}

.carrito-actions-bar {
  padding: 16px 18px;
  display: flex;
  justify-content: flex-end;
  background: var(--surface-alt);
}

.btn-vaciar-carrito {
  background: transparent;
  color: var(--danger);
  border: 1px dashed var(--danger);
  padding: 8px 16px;
  border-radius: 8px;
  font-size: 13px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-vaciar-carrito:hover:not(:disabled) {
  background: #fef2f2;
}

.btn-vaciar-carrito:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.carrito-summary-card {
  background: #ffffff;
  border: 1px solid var(--border-color);
  border-radius: var(--radius);
  padding: 24px;
  box-shadow: var(--shadow-sm);
}

.carrito-summary-card h3 {
  margin: 0 0 20px 0;
  font-size: 18px;
  font-weight: 700;
  color: var(--text-primary);
  border-bottom: 1px solid var(--border-color);
  padding-bottom: 12px;
}

.summary-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 14px;
  font-size: 15px;
  color: var(--text-secondary);
}

.summary-row.total-row {
  margin-top: 20px;
  padding-top: 16px;
  border-top: 2px dashed var(--border-color);
  font-size: 18px;
  font-weight: 700;
  color: var(--text-primary);
}

.summary-total-price {
  color: var(--primary);
  font-size: 24px;
  font-weight: 800;
}

.btn-confirmar-compra {
  width: 100%;
  margin-top: 20px;
  padding: 14px;
  font-size: 16px;
  font-weight: 700;
  background: var(--primary);
  color: white;
  border: none;
  border-radius: var(--radius);
  cursor: pointer;
  transition: all 0.2s;
  box-shadow: 0 4px 12px rgba(147, 51, 234, 0.3);
}

.btn-confirmar-compra:hover:not(:disabled) {
  background: var(--primary-hover);
  transform: translateY(-1px);
}

.btn-confirmar-compra:disabled {
  opacity: 0.65;
  cursor: not-allowed;
  transform: none;
  box-shadow: none;
}

.btn-agregado {
  background-color: var(--success) !important;
  color: white !important;
}

.stock-badge {
  font-size: 12px;
  font-weight: 600;
  padding: 3px 8px;
  border-radius: 6px;
}

.stock-badge.con-stock {
  background-color: #dcfce7;
  color: #15803d;
}

.stock-badge.sin-stock {
  background-color: #fee2e2;
  color: #b91c1c;
}
"""

app_css_path = os.path.join(FRONTEND_SRC, "App.css")
with open(app_css_path, "r", encoding="utf-8") as f:
    existing_css = f.read()

if "carrito-page-container" not in existing_css:
    with open(app_css_path, "a", encoding="utf-8") as f:
        f.write("\n" + css_addon.strip() + "\n")
    print("Appended carrito styles to App.css")
else:
    print("Carrito styles already in App.css")

print("SUCCESS: All lab files written!")

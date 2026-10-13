import { useState, useEffect } from 'react';
import { getProductos } from '../services/api';
import { useAuth } from '../context/AuthContext';
import ProductCard from './ProductCard';
import ProductoModal from './ProductoModal';

const Catalogo = () => {
  const { user } = useAuth();
  const isAdmin = user?.rol === 'admin';

  const [productos, setProductos] = useState([]);
  const [page, setPage] = useState(0);
  const [busqueda, setBusqueda] = useState('');
  const [cargando, setCargando] = useState(true);
  const [lento, setLento] = useState(false);
  const [error, setError] = useState(null);

  // Efecto para aviso si el backend en Render tarda en despertar (> 5s)
  useEffect(() => {
    if (!cargando) {
      setLento(false);
      return;
    }
    const t = setTimeout(() => setLento(true), 5000);
    return () => clearTimeout(t);
  }, [cargando]);

  // Modal para crear / editar
  const [modalAbierto, setModalAbierto] = useState(false);
  const [productoSeleccionado, setProductoSeleccionado] = useState(null);

  const cargarProductos = () => {
    setCargando(true);
    setError(null);

    getProductos({ page, limit: 8, nombre: busqueda })
      .then((data) => {
        setProductos(Array.isArray(data) ? data : (data.items || []));
      })
      .catch((err) => {
        console.error('Error al cargar productos:', err);
        setError('No se pudieron cargar los productos. Por favor, verifica que el backend esté encendido.');
      })
      .finally(() => {
        setCargando(false);
      });
  };

  useEffect(() => {
    cargarProductos();
  }, [page, busqueda]);

  const handleNuevoProducto = () => {
    setProductoSeleccionado(null);
    setModalAbierto(true);
  };

  const handleEditarProducto = (prod) => {
    setProductoSeleccionado(prod);
    setModalAbierto(true);
  };

  const handleProductoEliminado = (idEliminado) => {
    setProductos((prev) => prev.filter((p) => p.id !== idEliminado));
  };

  return (
    <div className="catalogo-section">
      <div className="catalogo-hero">
        <h2>Catálogo de Postres & Delicias</h2>
        <p>Explora nuestras creaciones artesanales preparadas con ingredientes de alta calidad</p>
      </div>

      <div className="catalogo-toolbar">
        <div className="search-bar">
          <span className="search-icon">🔍</span>
          <input
            type="text"
            placeholder="Buscar postres, tortas, bombones..."
            value={busqueda}
            onChange={(e) => {
              setPage(0);
              setBusqueda(e.target.value);
            }}
          />
          {busqueda && (
            <button
              onClick={() => setBusqueda('')}
              className="search-clear-btn"
              title="Limpiar búsqueda"
            >
              ✕
            </button>
          )}
        </div>

        {isAdmin && (
          <button
            onClick={handleNuevoProducto}
            className="btn-nuevo-producto"
            title="Crear un nuevo producto en la tienda"
          >
            ➕ Nuevo Producto
          </button>
        )}
      </div>

      {cargando && (
        <div className="loading-state">
          <div className="spinner"></div>
          <p role="status">
            {lento
              ? "Despertando el servidor, la primera visita puede tardar un minuto…"
              : "Cargando productos…"}
          </p>
        </div>
      )}

      {!cargando && error && (
        <div className="auth-alert error">
          <span>⚠️</span>
          <div>
            <strong>Error al cargar el catálogo:</strong> {error}
          </div>
        </div>
      )}

      {!cargando && !error && (
        <>
          {productos.length === 0 ? (
            <div className="empty-pedidos" style={{ margin: '40px 0' }}>
              <span className="empty-icon">🍰</span>
              <h3>No se encontraron productos</h3>
              <p>Intenta con otro término de búsqueda o limpia el filtro para ver todo el catálogo.</p>
              {busqueda && (
                <button
                  onClick={() => setBusqueda('')}
                  className="btn-auth-primary"
                  style={{ marginTop: '16px' }}
                >
                  Ver todos los productos
                </button>
              )}
            </div>
          ) : (
            <div className="catalogo-grid">
              {productos.map((prod) => (
                <ProductCard
                  key={prod.id}
                  producto={prod}
                  onEditar={handleEditarProducto}
                  onEliminado={handleProductoEliminado}
                />
              ))}
            </div>
          )}

          <div className="pagination-bar">
            <button
              onClick={() => setPage((p) => Math.max(0, p - 1))}
              disabled={page === 0}
              className="btn-pagination"
            >
              ← Anterior
            </button>
            <span className="pagination-indicator">Página {page + 1}</span>
            <button
              onClick={() => setPage((p) => p + 1)}
              disabled={productos.length < 8}
              className="btn-pagination"
            >
              Siguiente →
            </button>
          </div>
        </>
      )}

      {/* Modal para Crear / Editar Producto */}
      {modalAbierto && (
        <ProductoModal
          producto={productoSeleccionado}
          onClose={() => setModalAbierto(false)}
          onGuardado={cargarProductos}
        />
      )}
    </div>
  );
};

export default Catalogo;

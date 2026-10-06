import { useState, useRef, useEffect } from 'react';
import { crearProducto, actualizarProducto, subirImagen } from '../services/api';
import { urlImagen } from '../utils/imagenes';

const ProductoModal = ({ producto, onClose, onGuardado }) => {
  const isEditing = !!producto;
  const [formData, setFormData] = useState({
    nombre: producto ? producto.nombre : '',
    precio: producto ? producto.precio : '',
    precio_final: producto ? (producto.precio_final ?? producto.precio) : '',
    stock: producto ? producto.stock : 10,
    cuotas_cantidad: producto ? (producto.cuotas_cantidad || 1) : 1,
    cuotas_valor: producto ? (producto.cuotas_valor ?? producto.precio) : '',
    garantia_meses: producto ? (producto.garantia_meses || 0) : 0,
  });

  const [guardando, setGuardando] = useState(false);
  const [error, setError] = useState(null);

  // Estados para Parte 1, 2 y 3 (Subida de Imagen)
  const [archivo, setArchivo] = useState(null);
  const [preview, setPreview] = useState(producto ? urlImagen(producto) : null);
  const [subiendoImagen, setSubiendoImagen] = useState(false);
  const [errorImagen, setErrorImagen] = useState(null);
  const fileInputRef = useRef(null);

  // Parte 2.4: useEffect que revoca el ObjectURL cuando cambia o el componente se desmonta
  useEffect(() => {
    return () => {
      if (preview && preview.startsWith('blob:')) {
        URL.revokeObjectURL(preview);
      }
    };
  }, [preview]);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => {
      const updated = { ...prev, [name]: value };
      if (name === 'precio') {
        const pNum = parseFloat(value) || 0;
        const cuotas = parseInt(updated.cuotas_cantidad) || 1;
        updated.precio_final = value;
        updated.cuotas_valor = (pNum / cuotas).toFixed(2);
      }
      if (name === 'cuotas_cantidad') {
        const pNum = parseFloat(updated.precio_final || updated.precio) || 0;
        const cuotas = parseInt(value) || 1;
        updated.cuotas_valor = (pNum / cuotas).toFixed(2);
      }
      return updated;
    });
  };

  // Parte 1 y 2: Manejo de selección de archivo con validación
  const handleFileChange = (e) => {
    setErrorImagen(null);
    const file = e.target.files?.[0];
    if (!file) {
      setArchivo(null);
      return;
    }

    // Parte 1.4: Mostrar en consola el objeto File (name, size, type)
    console.log('Archivo seleccionado:', {
      name: file.name,
      size: file.size,
      type: file.type,
      file,
    });

    // Parte 2.5: Validar antes de previsualizar
    // type dentro de la lista permitida (image/*)
    const tiposPermitidos = ['image/jpeg', 'image/png', 'image/webp', 'image/gif'];
    const esImagen = file.type.startsWith('image/') || tiposPermitidos.includes(file.type);
    const maxBytes = 2 * 1024 * 1024; // 2 MB

    if (!esImagen) {
      setErrorImagen(`El archivo "${file.name}" no es una imagen permitida (tipo reportado: "${file.type || 'desconocido'}").`);
      setArchivo(null);
      if (fileInputRef.current) fileInputRef.current.value = '';
      return;
    }

    if (file.size > maxBytes) {
      const tamMB = (file.size / (1024 * 1024)).toFixed(2);
      setErrorImagen(`La imagen supera el límite de 2 MB (tamaño: ${tamMB} MB).`);
      setArchivo(null);
      if (fileInputRef.current) fileInputRef.current.value = '';
      return;
    }

    // Si pasó las validaciones:
    // Revocar previa si era blob
    if (preview && preview.startsWith('blob:')) {
      URL.revokeObjectURL(preview);
    }

    const objectUrl = URL.createObjectURL(file);
    // Parte 2.3: Anotar URL creada en consola
    console.log('Vista previa ObjectURL creada:', objectUrl);

    setArchivo(file);
    setPreview(objectUrl);
  };

  // Parte 3: Subida manual o automática de la imagen para el producto
  const handleSubirImagenIndividual = async (prodId) => {
    if (!archivo) return;
    try {
      setSubiendoImagen(true);
      setErrorImagen(null);
      await subirImagen(prodId, archivo);
      // Limpieza del campo al terminar
      setArchivo(null);
      if (fileInputRef.current) fileInputRef.current.value = '';
    } catch (err) {
      console.error('Error al subir imagen:', err);
      setErrorImagen(err.message || 'Error al subir la imagen');
      throw err;
    } finally {
      setSubiendoImagen(false);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!formData.nombre.trim()) {
      setError('El nombre del producto es obligatorio.');
      return;
    }
    if (parseFloat(formData.precio) <= 0 || isNaN(parseFloat(formData.precio))) {
      setError('El precio debe ser un número mayor a 0.');
      return;
    }

    setGuardando(true);
    setError(null);

    const payload = {
      nombre: formData.nombre.trim(),
      precio: parseFloat(formData.precio),
      precio_final: parseFloat(formData.precio_final || formData.precio),
      stock: parseInt(formData.stock) || 0,
      cuotas_cantidad: parseInt(formData.cuotas_cantidad) || 1,
      cuotas_valor: parseFloat(formData.cuotas_valor || formData.precio),
      garantia_meses: parseInt(formData.garantia_meses) || 0,
    };

    try {
      let savedProduct;
      if (isEditing) {
        savedProduct = await actualizarProducto(producto.id, payload);
        if (archivo) {
          await handleSubirImagenIndividual(producto.id);
        }
      } else {
        savedProduct = await crearProducto(payload);
        if (archivo && savedProduct?.id) {
          await handleSubirImagenIndividual(savedProduct.id);
        }
      }
      onGuardado();
      onClose();
    } catch (err) {
      console.error(err);
      setError(err.message || 'Error al guardar el producto.');
    } finally {
      setGuardando(false);
    }
  };

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content admin-producto-modal" onClick={(e) => e.stopPropagation()}>
        <div className="modal-header">
          <h3>{isEditing ? '✏️ Editar Producto' : '✨ Agregar Nuevo Producto'}</h3>
          <button className="btn-close-modal" onClick={onClose}>✕</button>
        </div>

        {error && (
          <div className="auth-alert error" style={{ margin: '12px 0' }}>
            <span>⚠️</span>
            <div>{error}</div>
          </div>
        )}

        <form onSubmit={handleSubmit} className="admin-product-form">
          <div className="form-group">
            <label>Nombre del Producto</label>
            <input
              type="text"
              name="nombre"
              value={formData.nombre}
              onChange={handleChange}
              placeholder="Ej: Torta Balcarce, Alfajor de Maicena"
              required
            />
          </div>

          <div className="form-row-2">
            <div className="form-group">
              <label>Precio ($)</label>
              <input
                type="number"
                step="0.01"
                min="0"
                name="precio"
                value={formData.precio}
                onChange={handleChange}
                placeholder="0.00"
                required
              />
            </div>
            <div className="form-group">
              <label>Precio Final / Oferta ($)</label>
              <input
                type="number"
                step="0.01"
                min="0"
                name="precio_final"
                value={formData.precio_final}
                onChange={handleChange}
                placeholder="0.00"
              />
            </div>
          </div>

          <div className="form-row-3">
            <div className="form-group">
              <label>Stock Disponible</label>
              <input
                type="number"
                min="0"
                name="stock"
                value={formData.stock}
                onChange={handleChange}
                required
              />
            </div>
            <div className="form-group">
              <label>Cantidad de Cuotas</label>
              <input
                type="number"
                min="1"
                name="cuotas_cantidad"
                value={formData.cuotas_cantidad}
                onChange={handleChange}
              />
            </div>
            <div className="form-group">
              <label>Valor de Cuota ($)</label>
              <input
                type="number"
                step="0.01"
                min="0"
                name="cuotas_valor"
                value={formData.cuotas_valor}
                onChange={handleChange}
              />
            </div>
          </div>

          <div className="form-group">
            <label>Garantía (en meses)</label>
            <input
              type="number"
              min="0"
              name="garantia_meses"
              value={formData.garantia_meses}
              onChange={handleChange}
            />
          </div>

          {/* Sección de Imagen (Partes 1, 2 y 3) */}
          <div className="form-group imagen-upload-section">
            <label>Imagen del Producto</label>
            
            {/* Parte 1.2 y 1.3: input de archivo sin value, con ref y accept="image/*" */}
            <input
              type="file"
              ref={fileInputRef}
              accept="image/*"
              onChange={handleFileChange}
              className="input-file"
              disabled={guardando || subiendoImagen}
            />

            {errorImagen && (
              <div className="auth-alert error" style={{ margin: '8px 0', fontSize: '13px' }}>
                <span>⚠️</span>
                <div>{errorImagen}</div>
              </div>
            )}

            {/* Parte 2.2: Vista previa chica con object-cover */}
            {preview && (
              <div className="preview-container" style={{ marginTop: '10px' }}>
                <p style={{ fontSize: '12px', color: '#64748b', marginBottom: '6px' }}>Vista previa:</p>
                <div className="preview-thumbnail aspect-square" style={{ width: '100px', height: '100px', borderRadius: '8px', overflow: 'hidden', border: '1px solid #cbd5e1' }}>
                  <img
                    src={preview}
                    alt="Vista previa"
                    className="object-cover"
                    style={{ width: '100%', height: '100%', objectFit: 'cover' }}
                  />
                </div>
              </div>
            )}

            {/* Parte 3.6: Botón dedicado si está editando con archivo elegido */}
            {isEditing && (
              <div style={{ marginTop: '10px' }}>
                <button
                  type="button"
                  disabled={!archivo || subiendoImagen}
                  onClick={async () => {
                    try {
                      await handleSubirImagenIndividual(producto.id);
                      onGuardado();
                    } catch (e) {
                      // error capturado
                    }
                  }}
                  className="btn-subir-imagen"
                >
                  {subiendoImagen ? 'Subiendo…' : 'Subir Imagen Ahora'}
                </button>
              </div>
            )}
          </div>

          <div className="modal-actions">
            <button type="button" onClick={onClose} className="btn-cancelar" disabled={guardando || subiendoImagen}>
              Cancelar
            </button>
            <button type="submit" className="btn-guardar" disabled={guardando || subiendoImagen}>
              {guardando || subiendoImagen ? 'Subiendo…' : (isEditing ? 'Guardar Cambios' : 'Crear Producto')}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default ProductoModal;


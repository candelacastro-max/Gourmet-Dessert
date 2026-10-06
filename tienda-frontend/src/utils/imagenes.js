/**
 * Devuelve la URL completa de la imagen del producto.
 * Si no hay imagen, devuelve null.
 * Si la hay, le concatena VITE_API_URL adelante (o el backend por defecto).
 */
export function urlImagen(producto) {
  if (!producto || !producto.imagen_url) {
    return null;
  }

  // Si ya es una URL absoluta (http:// o https:// o blob:), devolverla tal cual
  if (producto.imagen_url.startsWith('http://') || producto.imagen_url.startsWith('https://') || producto.imagen_url.startsWith('blob:')) {
    return producto.imagen_url;
  }

  const baseUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000';
  // Asegurarse de que no queden dobles barras
  const cleanBase = baseUrl.endsWith('/') ? baseUrl.slice(0, -1) : baseUrl;
  const cleanPath = producto.imagen_url.startsWith('/') ? producto.imagen_url : `/${producto.imagen_url}`;

  return `${cleanBase}${cleanPath}`;
}

const BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

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

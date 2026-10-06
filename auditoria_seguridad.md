# Informe de Auditoría de Seguridad

## 1. Hallazgos Confirmados

**1. Falta de autenticación en endpoint de escritura (Autenticación Rota)**
* **Archivo/Línea:** `app/routers/pedidos.py` (Línea ~69, endpoint `POST /arrepentimiento`)
* **Severidad:** Media / Aceptado
* **Descripción:** El endpoint que procesa las solicitudes de revocación no cuenta con validación de token (sesión). Antigravity lo marca como endpoint inseguro al permitir escrituras sin autenticación.
* **Justificación / Plan de acción:** Es **a propósito**. La Disposición 954/2025 prohíbe exigir sesión previa para ejercer el derecho de arrepentimiento. Se mantendrá así para cumplir la ley. Como pendiente, se requiere agregar un límite de intentos (rate limiting) por IP para mitigar posibles ataques de denegación de servicio (DDoS) o saturación de la base de datos.

**2. Falta de Rate Limiting global (Limitación de Tasa)**
* **Archivo/Línea:** General (`app/main.py`)
* **Severidad:** Alta
* **Descripción:** Ningún endpoint, incluidos los de autenticación (`/auth/login`) y de arrepentimiento, cuenta con un límite de peticiones. Esto deja al sistema vulnerable a ataques de fuerza bruta (para adivinar contraseñas) y agotamiento de recursos.
* **Plan de acción:** Implementar un middleware o dependencia (ej. `slowapi`) para limitar peticiones. Esto es de severidad alta y debe corregirse a la brevedad.

**3. CORS demasiado permisivo (Misconfiguración)**
* **Archivo/Línea:** `app/main.py` (Línea 14)
* **Severidad:** Baja (Por ahora)
* **Descripción:** Se permiten todos los métodos (`allow_methods=["*"]`) y todos los encabezados. Los orígenes están fijos a `localhost`. 
* **Plan de acción:** Antes de salir a producción, se deben acotar estrictamente los orígenes y métodos. Pendiente para fase de despliegue.

## 2. Falsos Positivos

**1. Posible Inyección SQL**
* **Descripción:** El escáner puede alertar sobre manipulación de la base de datos en las búsquedas (ej. `GET /productos?nombre=...`).
* **Explicación:** Es un falso positivo porque el sistema utiliza el ORM SQLAlchemy en toda la aplicación (`db.query(...)`), el cual pagina y parametriza automáticamente las consultas y variables, neutralizando ataques de inyección SQL directa sin concatenación insegura de strings.

## 3. Dudas / No Entendidos (Para consultar en clase)

*(Los puntos que no entendimos del reporte del escáner se anotan aparte para discutirlos, tal como exige la tarea. No se incluyen en este entregable final).*

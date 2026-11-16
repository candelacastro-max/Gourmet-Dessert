# React + Vite

This template provides a minimal setup to get React working in Vite with HMR and some Oxlint rules.

Currently, two official plugins are available:

- [@vitejs/plugin-react](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react) uses [Oxc](https://oxc.rs)
- [@vitejs/plugin-react-swc](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react-swc) uses [SWC](https://swc.rs/)

## React Compiler

The React Compiler is not enabled on this template because of its impact on dev & build performances. To add it, see [this documentation](https://react.dev/learn/react-compiler/installation).

## Expanding the Oxlint configuration

If you are developing a production application, we recommend using TypeScript with type-aware lint rules enabled. Check out the [TS template](https://github.com/vitejs/vite/tree/main/packages/create-vite/template-react-ts) for information on how to integrate TypeScript and Oxlint's TypeScript related rules in your project.


## Tests

Para ejecutar las pruebas automáticas del frontend, se utiliza **Vitest** con **React Testing Library** y entorno **jsdom**.

### Comandos
- Ejecución en modo continuo (observador):
  ```bash
  npm test
  ```
- Ejecución única (para CI o verificación rápida):
  ```bash
  npm run test:run
  ```

### Reglas protegidas por los tests
1. **Detección de conexión (`src/hooks/useConectado.test.js`)**:
   - Verifica que el hook arranque conectado y escuche dinámicamente los eventos `offline` y `online` del navegador para alertar al usuario.
2. **Consentimiento informado en Registro (`src/pages/Registro.test.jsx`)**:
   - Cumple con la **Ley 25.326**: la casilla de consentimiento para el tratamiento de datos personales no viene marcada por defecto y el botón de creación permanece deshabilitado hasta que el usuario la tilde explícitamente.
3. **Derecho de Arrepentimiento sin sesión (`src/pages/Arrepentimiento.test.jsx`)**:
   - Cumple con la **Disposición 954/2025 y Ley 24.240**: permite solicitar la revocación sin requerir autenticación (`Authorization`), envía los datos necesarios (`email`, `pedido_id`) y entrega un código de trámite identificatorio.
4. **Persistencia y cálculo del Carrito (`src/context/CarritoContext.test.jsx`)**:
   - Suma cantidades en lugar de filas duplicadas al agregar el mismo ítem.
   - Calcula el total acumulado exacto mediante `reduce`.
   - Mantiene los ítems del carrito ante una recarga o cierre gracias a `localStorage`.

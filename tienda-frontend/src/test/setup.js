import "@testing-library/jest-dom/vitest";
import { afterEach, vi } from "vitest";
import { cleanup } from "@testing-library/react";

// Mock consistente de localStorage para evitar conflictos de Node 22 con jsdom
const store = new Map();
const mockLocalStorage = {
  getItem: (key) => store.get(String(key)) ?? null,
  setItem: (key, val) => store.set(String(key), String(val)),
  removeItem: (key) => store.delete(String(key)),
  clear: () => store.clear(),
  get length() {
    return store.size;
  },
  key: (i) => Array.from(store.keys())[i] ?? null,
};

Object.defineProperty(window, "localStorage", {
  value: mockLocalStorage,
  writable: true,
  configurable: true,
});

Object.defineProperty(globalThis, "localStorage", {
  value: mockLocalStorage,
  writable: true,
  configurable: true,
});

afterEach(() => {
  cleanup(); // desmonta lo que renderizó cada test
  vi.restoreAllMocks(); // devuelve fetch a la normalidad
  mockLocalStorage.clear(); // el carrito persistido no pasa de un test al otro
});

import React from "react";
import { describe, it, expect } from "vitest";
import { renderHook, act } from "@testing-library/react";
import { CarritoProvider, useCarrito } from "./CarritoContext";

const mate = { id: 1, nombre: "Mate", precio: 1000 };
const bombilla = { id: 2, nombre: "Bombilla", precio: 2500 };

function usarCarrito() {
  return renderHook(() => useCarrito(), { wrapper: CarritoProvider });
}

describe("CarritoContext", () => {
  it("agregar dos veces el mismo producto suma cantidad, no filas", () => {
    const { result } = usarCarrito();

    act(() => {
      result.current.agregar(mate);
    });
    act(() => {
      result.current.agregar(mate);
    });

    expect(result.current.items).toHaveLength(1);
    expect(result.current.items[0].cantidad).toBe(2);
  });

  it("calcula el total correctamente con múltiples productos", () => {
    const { result } = usarCarrito();

    act(() => {
      result.current.agregar(mate);
    });
    act(() => {
      result.current.agregar(bombilla);
    });

    expect(result.current.total).toBe(3500);
  });

  it("sobrevive a una recarga leyendo de localStorage", () => {
    const { result, unmount } = usarCarrito();

    act(() => {
      result.current.agregar(mate);
    });
    expect(result.current.items).toHaveLength(1);

    // Desmontamos (simula recarga / cierre de la app)
    unmount();

    // Volvemos a montar el contexto
    const recarga = usarCarrito();
    expect(recarga.result.current.items).toHaveLength(1);
    expect(recarga.result.current.items[0].id).toBe(mate.id);
  });
});

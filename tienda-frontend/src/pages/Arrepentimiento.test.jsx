import React from "react";
import { describe, it, expect, vi } from "vitest";
import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import Arrepentimiento from "./Arrepentimiento";

function respuesta(cuerpo, status = 201) {
  return new Response(JSON.stringify(cuerpo), {
    status,
    headers: { "Content-Type": "application/json" },
  });
}

describe("Arrepentimiento", () => {
  it("funciona sin sesión y muestra el código en pantalla", async () => {
    const fetchFalso = vi
      .spyOn(globalThis, "fetch")
      .mockResolvedValue(respuesta({ codigo: "ARR-7F3A", detalle: "Recibida" }));
    const usuario = userEvent.setup();

    // Sin AuthProvider a propósito: si esto rompe, el formulario depende del login
    render(<Arrepentimiento />);

    await usuario.type(screen.getByLabelText(/correo/i), "ana@prueba.com");
    await usuario.type(screen.getByLabelText(/pedido/i), "12");
    await usuario.click(screen.getByRole("button", { name: /arrepentimiento/i }));

    expect(await screen.findByRole("status")).toHaveTextContent("ARR-7F3A");

    const [url, opciones] = fetchFalso.mock.calls[0];
    expect(url).toMatch(/\/arrepentimiento$/);
    expect(opciones.headers).not.toHaveProperty("Authorization");
    expect(JSON.parse(opciones.body)).toEqual({
      email: "ana@prueba.com",
      pedido_id: 12,
    });
  });
});

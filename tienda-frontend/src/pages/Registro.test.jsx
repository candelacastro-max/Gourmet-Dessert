import React from "react";
import { describe, it, expect } from "vitest";
import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { MemoryRouter } from "react-router-dom";
import { AuthProvider } from "../context/AuthContext";
import Registro from "./Registro";

describe("Registro", () => {
  it("no deja crear la cuenta sin el consentimiento", async () => {
    const usuario = userEvent.setup();
    render(
      <MemoryRouter>
        <AuthProvider>
          <Registro />
        </AuthProvider>
      </MemoryRouter>
    );
    const boton = screen.getByRole("button", { name: /crear cuenta/i });
    const casilla = screen.getByRole("checkbox", {
      name: /tratamiento de mis datos/i,
    });
    expect(casilla).not.toBeChecked(); // Ley 25.326: no viene pre-marcado
    expect(boton).toBeDisabled();
    await usuario.click(casilla);
    expect(boton).toBeEnabled();
  });
});

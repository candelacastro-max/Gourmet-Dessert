import { describe, it, expect } from "vitest";
import { renderHook, act } from "@testing-library/react";
import { useConectado } from "./useConectado";

describe("useConectado", () => {
  it("arranca conectado y se entera cuando se corta", () => {
    const { result } = renderHook(() => useConectado());
    expect(result.current).toBe(true);

    act(() => window.dispatchEvent(new Event("offline")));
    expect(result.current).toBe(false);

    act(() => window.dispatchEvent(new Event("online")));
    expect(result.current).toBe(true);
  });
});

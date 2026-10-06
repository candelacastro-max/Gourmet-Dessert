import { useState } from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider, useAuth } from './context/AuthContext';
import { CarritoProvider } from './context/CarritoContext';
import AuthPage from './pages/AuthPage';
import Navbar from './components/Navbar';
import Catalogo from './components/Catalogo';
import Carrito from './pages/Carrito';
import MisPedidos from './components/MisPedidos';
import RutaProtegida from './components/RutaProtegida';
import './App.css';

import Arrepentimiento from './pages/Arrepentimiento';
import Footer from './components/Footer';
import MisDatos from './pages/MisDatos'; // Preparando para la parte 3

const RootRedirect = () => {
  const { isAuthenticated, isGuest, isLoading } = useAuth();

  if (isLoading) {
    return (
      <div className="loading-screen">
        <div className="spinner"></div>
        <p>Cargando tienda...</p>
      </div>
    );
  }

  return <Navigate to="/catalogo" replace />;
};

const LoginPageWrapper = () => {
  const { isAuthenticated, isLoading } = useAuth();

  if (isLoading) {
    return (
      <div className="loading-screen">
        <div className="spinner"></div>
      </div>
    );
  }

  if (isAuthenticated) {
    return <Navigate to="/catalogo" replace />;
  }

  return <AuthPage />;
};

const MainLayout = ({ children }) => {
  return (
    <div className="app-shell" style={{ display: 'flex', flexDirection: 'column', minHeight: '100vh' }}>
      <Navbar />
      <main className="main-content" style={{ flex: 1 }}>{children}</main>
      <Footer />
    </div>
  );
};

function App() {
  return (
    <AuthProvider>
      <CarritoProvider>
        <BrowserRouter>
          <Routes>
            <Route path="/" element={<RootRedirect />} />
            <Route path="/login" element={<LoginPageWrapper />} />

            <Route
              path="/catalogo"
              element={
                <MainLayout>
                  <Catalogo />
                </MainLayout>
              }
            />

            {/* Página /carrito */}
            <Route
              path="/carrito"
              element={
                <MainLayout>
                  <Carrito />
                </MainLayout>
              }
            />
            
            {/* Página /arrepentimiento (pública, fuera de RutaProtegida) */}
            <Route
              path="/arrepentimiento"
              element={
                <MainLayout>
                  <Arrepentimiento />
                </MainLayout>
              }
            />

            {/* Ruta /mis-pedidos protegida con RutaProtegida */}
            <Route
              path="/mis-pedidos"
              element={
                <RutaProtegida>
                  <MainLayout>
                    <MisPedidos />
                  </MainLayout>
                </RutaProtegida>
              }
            />
            
            {/* Ruta /mis-datos protegida */}
            <Route
              path="/mis-datos"
              element={
                <RutaProtegida>
                  <MainLayout>
                    <MisDatos />
                  </MainLayout>
                </RutaProtegida>
              }
            />

            {/* Redirección para compatibilidad */}
            <Route path="/pedidos" element={<Navigate to="/mis-pedidos" replace />} />
            <Route path="*" element={<Navigate to="/catalogo" replace />} />
          </Routes>
        </BrowserRouter>
      </CarritoProvider>
    </AuthProvider>
  );
}

export default App;

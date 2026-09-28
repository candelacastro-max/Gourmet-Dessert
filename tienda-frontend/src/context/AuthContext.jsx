import { createContext, useContext, useState, useEffect } from 'react';
import { loginUser, registerUser, getMe } from '../services/api';

const AuthContext = createContext();

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth debe ser usado dentro de un AuthProvider');
  }
  return context;
};

export const AuthProvider = ({ children }) => {
  const [token, setToken] = useState(() => localStorage.getItem('access_token') || localStorage.getItem('token'));
  const [user, setUser] = useState(null);
  const [isGuest, setIsGuest] = useState(() => localStorage.getItem('isGuest') === 'true');
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const initAuth = async () => {
      const storedToken = localStorage.getItem('access_token') || localStorage.getItem('token');
      if (storedToken) {
        try {
          const userData = await getMe(storedToken);
          setUser(userData);
          setToken(storedToken);
          setIsGuest(false);
          localStorage.removeItem('isGuest');
        } catch (err) {
          console.error('Token inválido o expirado:', err);
          localStorage.removeItem('access_token');
          localStorage.removeItem('token');
          setToken(null);
          setUser(null);
        }
      }
      setIsLoading(false);
    };

    initAuth();
  }, []);

  const login = async (email, password) => {
    setIsLoading(true);
    try {
      const tokenData = await loginUser(email, password);
      const accessToken = tokenData.access_token;
      localStorage.setItem('access_token', accessToken);
      localStorage.setItem('token', accessToken);
      localStorage.removeItem('isGuest');
      setToken(accessToken);
      setIsGuest(false);

      const userData = await getMe(accessToken);
      setUser(userData);
      return userData;
    } finally {
      setIsLoading(false);
    }
  };

  const register = async ({ nombre, email, password, acepto_tratamiento = true }) => {
    setIsLoading(true);
    try {
      await registerUser({ nombre, email, password, acepto_tratamiento });
      const tokenData = await loginUser(email, password);
      const accessToken = tokenData.access_token;
      localStorage.setItem('access_token', accessToken);
      localStorage.setItem('token', accessToken);
      localStorage.removeItem('isGuest');
      setToken(accessToken);
      setIsGuest(false);

      const userData = await getMe(accessToken);
      setUser(userData);
      return userData;
    } finally {
      setIsLoading(false);
    }
  };

  const continueAsGuest = () => {
    localStorage.removeItem('access_token');
    localStorage.removeItem('token');
    localStorage.setItem('isGuest', 'true');
    setToken(null);
    setUser(null);
    setIsGuest(true);
  };

  const logout = () => {
    localStorage.removeItem('access_token');
    localStorage.removeItem('token');
    localStorage.removeItem('isGuest');
    setToken(null);
    setUser(null);
    setIsGuest(false);
  };

  const value = {
    user,
    token,
    isGuest,
    isLoading,
    isAuthenticated: !!user && !!token,
    login,
    register,
    continueAsGuest,
    logout,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};

import { useState, useEffect } from 'react';

export function useConectado() {
  const [conectado, setConectado] = useState(
    typeof navigator !== 'undefined' ? navigator.onLine : true
  );

  useEffect(() => {
    const onlineHandler = () => setConectado(true);
    const offlineHandler = () => setConectado(false);

    window.addEventListener('online', onlineHandler);
    window.addEventListener('offline', offlineHandler);

    return () => {
      window.removeEventListener('online', onlineHandler);
      window.removeEventListener('offline', offlineHandler);
    };
  }, []);

  return conectado;
}

export default useConectado;

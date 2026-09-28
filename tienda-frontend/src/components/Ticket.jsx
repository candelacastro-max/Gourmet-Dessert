import { useRef } from 'react';

const ticketStyle = {
  background: '#fff',
  borderRadius: '12px',
  padding: '32px',
  maxWidth: '420px',
  width: '90%',
  boxShadow: '0 8px 32px rgba(0,0,0,0.2)',
  fontFamily: "'Courier New', monospace",
};

const Ticket = ({ ticket, onClose }) => {
  const ticketRef = useRef();

  const handleImprimir = () => {
    const contenido = ticketRef.current.innerHTML;
    const ventana = window.open('', '_blank', 'width=500,height=700');
    ventana.document.write(`
      <html>
        <head>
          <title>Ticket de Compra #${ticket.numero}</title>
          <style>
            body { font-family: 'Courier New', monospace; padding: 30px; }
            h2, h3 { text-align: center; }
            table { width: 100%; border-collapse: collapse; margin: 16px 0; }
            td { padding: 6px 4px; }
            .right { text-align: right; }
            .line { border-top: 1px dashed #999; margin: 12px 0; }
            .total { font-size: 1.2em; font-weight: bold; }
          </style>
        </head>
        <body>${contenido}</body>
      </html>
    `);
    ventana.document.close();
    ventana.print();
  };

  return (
    <div style={ticketStyle}>
      <div ref={ticketRef}>
        <h2 style={{ textAlign: 'center', marginTop: 0 }}>🎉 ¡Compra Confirmada!</h2>
        <h3 style={{ textAlign: 'center', color: '#555' }}>Trampaantojo</h3>

        <div className="line" style={{ borderTop: '1px dashed #999', margin: '12px 0' }} />

        <p style={{ margin: '4px 0' }}><strong>N° de compra:</strong> #{ticket.numero}</p>
        <p style={{ margin: '4px 0' }}><strong>Fecha:</strong> {ticket.fecha}</p>
        <p style={{ margin: '4px 0' }}><strong>Método de pago:</strong> {ticket.metodoPago}</p>

        <div className="line" style={{ borderTop: '1px dashed #999', margin: '12px 0' }} />

        <table style={{ width: '100%', borderCollapse: 'collapse' }}>
          <thead>
            <tr>
              <th style={{ textAlign: 'left' }}>Producto</th>
              <th style={{ textAlign: 'center' }}>Cant.</th>
              <th style={{ textAlign: 'right' }}>Subtotal</th>
            </tr>
          </thead>
          <tbody>
            {ticket.items.map(item => (
              <tr key={item.id}>
                <td>{item.nombre}</td>
                <td style={{ textAlign: 'center' }}>x{item.cantidad}</td>
                <td style={{ textAlign: 'right' }}>
                  ${(item.precio_final * item.cantidad).toLocaleString('es-AR')}
                </td>
              </tr>
            ))}
          </tbody>
        </table>

        <div className="line" style={{ borderTop: '1px dashed #999', margin: '12px 0' }} />

        <p style={{ textAlign: 'right', fontSize: '1.2em', fontWeight: 'bold', margin: 0 }}>
          TOTAL: ${ticket.total.toLocaleString('es-AR')}
        </p>

        <div className="line" style={{ borderTop: '1px dashed #999', margin: '12px 0' }} />

        <p style={{ textAlign: 'center', color: '#888', fontSize: '0.85em' }}>
          ¡Gracias por tu compra! 🍰
        </p>
      </div>

      <div style={{ display: 'flex', gap: '10px', marginTop: '20px', justifyContent: 'center' }}>
        <button
          onClick={handleImprimir}
          style={{
            padding: '10px 20px', borderRadius: '6px', border: 'none',
            background: '#1976d2', color: 'white', fontWeight: 'bold', cursor: 'pointer',
          }}
        >
          🖨️ Imprimir Ticket
        </button>
        <button
          onClick={onClose}
          style={{
            padding: '10px 20px', borderRadius: '6px', border: '1px solid #ccc',
            background: '#f5f5f5', cursor: 'pointer',
          }}
        >
          Cerrar
        </button>
      </div>
    </div>
  );
};

export default Ticket;

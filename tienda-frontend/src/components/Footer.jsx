import React from 'react';
import { Link } from 'react-router-dom';

const Footer = () => {
  return (
    <footer className="footer" style={{ padding: '2rem', textAlign: 'center', background: 'var(--surface-color)', marginTop: '2rem' }}>
      <div className="footer-links">
        <Link to="/arrepentimiento" style={{ color: 'var(--text-secondary)', textDecoration: 'none' }}>
          Botón de arrepentimiento
        </Link>
      </div>
    </footer>
  );
};

export default Footer;

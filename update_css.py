import os

css_addition = """
/* Hero & Toolbar del Catálogo */
.catalogo-hero {
  text-align: center;
  margin-bottom: 24px;
}

.catalogo-hero h2 {
  font-size: 32px;
  font-weight: 800;
  margin: 0 0 8px 0;
  color: #0f172a;
}

.catalogo-hero p {
  color: #64748b;
  font-size: 15px;
  margin: 0;
}

.catalogo-toolbar {
  display: flex;
  justify-content: center;
  margin-bottom: 24px;
}

.search-bar {
  position: relative;
  display: flex;
  align-items: center;
  width: 100%;
  max-width: 480px;
}

.search-icon {
  position: absolute;
  left: 14px;
  font-size: 16px;
  color: #94a3b8;
  pointer-events: none;
}

.search-bar input {
  width: 100%;
  padding: 12px 40px 12px 42px;
  border-radius: 9999px;
  border: 1.5px solid #cbd5e1;
  background: #ffffff;
  font-size: 14px;
  outline: none;
  box-shadow: 0 2px 4px rgba(0,0,0,0.03);
  transition: all 0.2s;
}

.search-bar input:focus {
  border-color: #9333ea;
  box-shadow: 0 0 0 3px rgba(147, 51, 234, 0.15);
}

.search-clear-btn {
  position: absolute;
  right: 12px;
  background: #e2e8f0;
  border: none;
  color: #475569;
  border-radius: 50%;
  width: 22px;
  height: 22px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  font-size: 12px;
}

.search-clear-btn:hover {
  background: #cbd5e1;
}

.loading-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 60px 0;
  gap: 16px;
  color: #64748b;
}

.pagination-bar {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 16px;
  margin-top: 36px;
  padding-bottom: 24px;
}

.btn-pagination {
  background: #ffffff;
  border: 1.5px solid #cbd5e1;
  color: #1e293b;
  padding: 8px 18px;
  border-radius: 8px;
  font-weight: 600;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-pagination:hover:not(:disabled) {
  background: #f3e8ff;
  border-color: #9333ea;
  color: #9333ea;
}

.btn-pagination:disabled {
  opacity: 0.45;
  cursor: not-allowed;
}

.pagination-indicator {
  font-weight: 600;
  font-size: 14px;
  color: #475569;
}
"""

css_path = r"C:\Users\Profesor\Desktop\Frontend\tienda-frontend\src\App.css"
with open(css_path, "a", encoding="utf-8") as f:
    f.write(css_addition)
print("APP.CSS UPDATED")

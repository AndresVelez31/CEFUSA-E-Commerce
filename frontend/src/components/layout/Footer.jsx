import { Link } from 'react-router-dom'

export default function Footer() {
  return (
    <footer className="border-t border-dark-700 bg-dark-900 mt-auto">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-10">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          {/* Brand */}
          <div>
            <span className="text-xl font-extrabold">
              <span className="text-brand-400">CEFUSA</span>
              <span className="text-slate-300"> Store</span>
            </span>
            <p className="mt-2 text-sm text-slate-500">
              Tu tienda online de confianza. Calidad y servicio garantizados.
            </p>
          </div>

          {/* Links */}
          <div>
            <h3 className="text-sm font-semibold text-slate-300 uppercase tracking-wider mb-3">
              Navegación
            </h3>
            <ul className="space-y-2">
              {[
                { label: 'Inicio',    to: '/' },
                { label: 'Carrito',   to: '/cart' },
                { label: 'Checkout',  to: '/checkout' },
              ].map(({ label, to }) => (
                <li key={to}>
                  <Link to={to} className="text-sm text-slate-500 hover:text-brand-400 transition-colors">
                    {label}
                  </Link>
                </li>
              ))}
            </ul>
          </div>

          {/* Info */}
          <div>
            <h3 className="text-sm font-semibold text-slate-300 uppercase tracking-wider mb-3">
              Proyecto
            </h3>
            <p className="text-sm text-slate-500">
              Desarrollado como entregable académico para el curso de Arquitectura de Software 2026.
            </p>
            <p className="mt-2 text-xs text-slate-600">
              Django REST + React + Tailwind CSS
            </p>
          </div>
        </div>

        <div className="mt-8 pt-6 border-t border-dark-700 text-center text-xs text-slate-600">
          © 2026 CEFUSA E-Commerce — Arquitectura de Software
        </div>
      </div>
    </footer>
  )
}

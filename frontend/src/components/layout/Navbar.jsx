import { Link, NavLink } from 'react-router-dom'
import { ShoppingCartIcon, Bars3Icon, XMarkIcon } from '@heroicons/react/24/outline'
import { useState } from 'react'
import { useCart } from '../../context/CartContext'

export default function Navbar() {
  const { itemCount } = useCart()
  const [mobileOpen, setMobileOpen] = useState(false)

  const navItems = [
    { label: 'Inicio',     to: '/' },
    { label: 'Productos',  to: '/?all=true' },
  ]

  return (
    <header className="sticky top-0 z-50 bg-dark-900/80 backdrop-blur-md border-b border-dark-700">
      <nav className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
        {/* Logo */}
        <Link to="/" className="flex items-center gap-2 group">
          <span className="text-2xl font-extrabold tracking-tight">
            <span className="text-brand-400">CEFUSA</span>
            <span className="text-slate-200"> Store</span>
          </span>
        </Link>

        {/* Nav links (desktop) */}
        <div className="hidden md:flex items-center gap-6">
          {navItems.map(({ label, to }) => (
            <NavLink
              key={to}
              to={to}
              className={({ isActive }) =>
                `text-sm font-medium transition-colors duration-200 ${
                  isActive ? 'text-brand-400' : 'text-slate-400 hover:text-slate-100'
                }`
              }
            >
              {label}
            </NavLink>
          ))}
        </div>

        {/* Right side */}
        <div className="flex items-center gap-3">
          <Link
            to="/cart"
            className="relative p-2 rounded-xl text-slate-400 hover:text-slate-100 hover:bg-dark-700 transition-all"
          >
            <ShoppingCartIcon className="w-6 h-6" />
            {itemCount > 0 && (
              <span className="absolute -top-1 -right-1 w-5 h-5 bg-brand-500 text-white text-xs font-bold rounded-full flex items-center justify-center">
                {itemCount > 9 ? '9+' : itemCount}
              </span>
            )}
          </Link>

          {/* Mobile menu button */}
          <button
            className="md:hidden p-2 rounded-xl text-slate-400 hover:text-slate-100 hover:bg-dark-700 transition-all"
            onClick={() => setMobileOpen(!mobileOpen)}
          >
            {mobileOpen ? <XMarkIcon className="w-6 h-6" /> : <Bars3Icon className="w-6 h-6" />}
          </button>
        </div>
      </nav>

      {/* Mobile menu */}
      {mobileOpen && (
        <div className="md:hidden border-t border-dark-700 bg-dark-900 px-4 py-3 space-y-1">
          {navItems.map(({ label, to }) => (
            <Link
              key={to}
              to={to}
              onClick={() => setMobileOpen(false)}
              className="block px-4 py-2 rounded-xl text-slate-300 hover:bg-dark-700 hover:text-white transition-colors"
            >
              {label}
            </Link>
          ))}
        </div>
      )}
    </header>
  )
}

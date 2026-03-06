import { Link, NavLink } from 'react-router-dom'
import { ShoppingCartIcon, Bars3Icon, XMarkIcon } from '@heroicons/react/24/outline'
import { useState } from 'react'
import { useCart } from '../../context/CartContext'

export default function Navbar() {
  const { itemCount } = useCart()
  const [mobileOpen, setMobileOpen] = useState(false)

  const navItems = [
    { label: 'Inicio',     to: '/' },
    { label: 'Carrito',   to: '/cart' },
  ]

  return (
    <header className="sticky top-0 z-50 bg-white/90 backdrop-blur-md border-b border-dark-600 shadow-sm">
      <nav className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
        {/* Logo */}
        <Link to="/" className="flex items-center gap-2.5 group">
          <img
            src="/cefusa-logo.png"
            alt="CEFUSA"
            className="h-10 w-10 object-contain"
          />
          <span className="text-2xl font-extrabold tracking-tight">
            <span className="text-brand-600">CEFUSA</span>
            <span className="text-gray-700"> Store</span>
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
                  isActive ? 'text-brand-600' : 'text-gray-600 hover:text-gray-900'
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
            className="relative p-2 rounded-xl text-gray-600 hover:text-gray-900 hover:bg-dark-700 transition-all"
          >
            <ShoppingCartIcon className="w-6 h-6" />
            {itemCount > 0 && (
              <span className="absolute -top-1 -right-1 w-5 h-5 bg-brand-600 text-white text-xs font-bold rounded-full flex items-center justify-center">
                {itemCount > 9 ? '9+' : itemCount}
              </span>
            )}
          </Link>

          {/* Mobile menu button */}
          <button
            className="md:hidden p-2 rounded-xl text-gray-600 hover:text-gray-900 hover:bg-dark-700 transition-all"
            onClick={() => setMobileOpen(!mobileOpen)}
          >
            {mobileOpen ? <XMarkIcon className="w-6 h-6" /> : <Bars3Icon className="w-6 h-6" />}
          </button>
        </div>
      </nav>

      {/* Mobile menu */}
      {mobileOpen && (
        <div className="md:hidden border-t border-dark-600 bg-white px-4 py-3 space-y-1">
          {navItems.map(({ label, to }) => (
            <Link
              key={to}
              to={to}
              onClick={() => setMobileOpen(false)}
              className="block px-4 py-2 rounded-xl text-gray-700 hover:bg-dark-700 hover:text-gray-900 transition-colors"
            >
              {label}
            </Link>
          ))}
        </div>
      )}
    </header>
  )
}

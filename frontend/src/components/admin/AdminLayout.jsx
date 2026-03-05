import { NavLink, Outlet } from 'react-router-dom'
import {
  HomeIcon,
  ShoppingBagIcon,
  UsersIcon,
  ArrowLeftOnRectangleIcon,
} from '@heroicons/react/24/outline'

const navItems = [
  { to: '/admin',           label: 'Dashboard', Icon: HomeIcon,         end: true },
  { to: '/admin/orders',    label: 'Órdenes',   Icon: ShoppingBagIcon },
  { to: '/admin/customers', label: 'Clientes',  Icon: UsersIcon },
]

export default function AdminLayout() {
  return (
    <div className="flex h-screen bg-slate-950 text-slate-100 overflow-hidden">
      {/* Sidebar */}
      <aside className="w-60 shrink-0 bg-slate-900 border-r border-slate-800 flex flex-col">
        {/* Logo */}
        <div className="px-6 py-5 border-b border-slate-800">
          <p className="text-lg font-bold text-sky-400 tracking-tight">CEFUSA</p>
          <p className="text-xs text-slate-500 mt-0.5">Panel de administración</p>
        </div>

        {/* Nav */}
        <nav className="flex-1 p-3 space-y-0.5">
          {navItems.map(({ to, label, Icon, end }) => (
            <NavLink
              key={to}
              to={to}
              end={end}
              className={({ isActive }) =>
                `flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm transition-colors ${
                  isActive
                    ? 'bg-sky-500/15 text-sky-400 font-medium'
                    : 'text-slate-400 hover:bg-slate-800 hover:text-slate-100'
                }`
              }
            >
              <Icon className="w-5 h-5 shrink-0" />
              {label}
            </NavLink>
          ))}
        </nav>

        {/* Footer del sidebar */}
        <div className="p-3 border-t border-slate-800">
          <a
            href="/"
            className="flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm text-slate-400
                       hover:bg-slate-800 hover:text-slate-100 transition-colors"
          >
            <ArrowLeftOnRectangleIcon className="w-5 h-5 shrink-0" />
            Volver al sitio
          </a>
        </div>
      </aside>

      {/* Contenido principal */}
      <main className="flex-1 overflow-y-auto">
        <Outlet />
      </main>
    </div>
  )
}

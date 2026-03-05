import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import {
  ShoppingBagIcon,
  CurrencyDollarIcon,
  UsersIcon,
  ClockIcon,
} from '@heroicons/react/24/outline'
import { getDashboard } from '../../api/admin'

const STATUS_META = {
  pending:   { label: 'Pendiente',   bar: 'bg-yellow-500', badge: 'bg-yellow-500/15 text-yellow-400' },
  confirmed: { label: 'Confirmado',  bar: 'bg-blue-500',   badge: 'bg-blue-500/15 text-blue-400'   },
  shipped:   { label: 'Enviado',     bar: 'bg-purple-500', badge: 'bg-purple-500/15 text-purple-400'},
  delivered: { label: 'Entregado',   bar: 'bg-emerald-500',badge: 'bg-emerald-500/15 text-emerald-400'},
  cancelled: { label: 'Cancelado',   bar: 'bg-red-500',    badge: 'bg-red-500/15 text-red-400'     },
}

const CARDS = (stats) => [
  {
    label: 'Total Órdenes',
    value: stats.total_orders,
    icon: ShoppingBagIcon,
    iconBg: 'bg-sky-500/15',
    iconColor: 'text-sky-400',
  },
  {
    label: 'Ingresos Totales',
    value: `$${Number(stats.total_revenue).toLocaleString('es-CO')}`,
    icon: CurrencyDollarIcon,
    iconBg: 'bg-emerald-500/15',
    iconColor: 'text-emerald-400',
  },
  {
    label: 'Clientes Registrados',
    value: stats.total_customers,
    icon: UsersIcon,
    iconBg: 'bg-violet-500/15',
    iconColor: 'text-violet-400',
  },
  {
    label: 'Órdenes Pendientes',
    value: stats.pending_orders,
    icon: ClockIcon,
    iconBg: 'bg-amber-500/15',
    iconColor: 'text-amber-400',
  },
]

export default function AdminDashboardPage() {
  const [stats, setStats] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    getDashboard()
      .then(setStats)
      .catch(() => setError('No se pudo conectar con el servidor'))
      .finally(() => setLoading(false))
  }, [])

  if (loading) return <div className="p-8 text-slate-400">Cargando...</div>
  if (error)   return <div className="p-8 text-red-400">{error}</div>

  const total = stats.total_orders || 1  // evitar división por cero

  return (
    <div className="p-8">
      <h2 className="text-2xl font-bold text-slate-100 mb-1">Dashboard</h2>
      <p className="text-slate-400 text-sm mb-6">Resumen general de la tienda</p>

      {/* Stat cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
        {CARDS(stats).map(({ label, value, icon: Icon, iconBg, iconColor }) => (
          <div key={label} className="bg-slate-900 rounded-xl p-5 border border-slate-800">
            <div className={`w-10 h-10 rounded-lg ${iconBg} flex items-center justify-center mb-3`}>
              <Icon className={`w-5 h-5 ${iconColor}`} />
            </div>
            <p className="text-2xl font-bold text-slate-100">{value}</p>
            <p className="text-sm text-slate-400 mt-1">{label}</p>
          </div>
        ))}
      </div>

      {/* Órdenes por estado */}
      <div className="bg-slate-900 rounded-xl border border-slate-800 p-6">
        <h3 className="text-slate-100 font-semibold mb-5">Órdenes por estado</h3>
        <div className="space-y-3">
          {Object.entries(stats.orders_by_status).map(([key, count]) => {
            const meta = STATUS_META[key] ?? { label: key, bar: 'bg-slate-500', badge: 'bg-slate-500/15 text-slate-400' }
            const pct = Math.round((count / total) * 100)
            return (
              <div key={key} className="flex items-center gap-4">
                <span className={`text-xs font-medium px-2.5 py-1 rounded-full w-28 text-center shrink-0 ${meta.badge}`}>
                  {meta.label}
                </span>
                <div className="flex-1 bg-slate-800 rounded-full h-2">
                  <div
                    className={`${meta.bar} h-2 rounded-full transition-all`}
                    style={{ width: `${pct}%` }}
                  />
                </div>
                <span className="text-sm text-slate-300 w-6 text-right shrink-0">{count}</span>
              </div>
            )
          })}
        </div>

        <div className="mt-5 pt-4 border-t border-slate-800">
          <Link to="/admin/orders" className="text-sm text-sky-400 hover:text-sky-300 transition-colors">
            Ver todas las órdenes →
          </Link>
        </div>
      </div>
    </div>
  )
}

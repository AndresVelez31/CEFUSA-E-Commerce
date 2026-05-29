import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import {
  ShoppingBagIcon,
  CurrencyDollarIcon,
  UsersIcon,
  ClockIcon,
} from '@heroicons/react/24/outline'
import { getDashboard } from '../../api/admin'
import QuickBiteInfoCard from '../../components/admin/QuickBiteInfoCard'

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
    iconBg: 'bg-brand-500/15',
    iconColor: 'text-brand-400',
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
      .catch(() =>
        setError(
          'No se pudo cargar el resumen. ¿Django en :8000? Reinicia el frontend (npm run dev) tras .\start.ps1'
        )
      )
      .finally(() => setLoading(false))
  }, [])

  const total = stats?.total_orders || 1

  return (
    <div className="p-8">
      <h2 className="text-2xl font-bold text-gray-900 mb-1">Dashboard</h2>
      <p className="text-gray-500 text-sm mb-6">Resumen general de la tienda</p>

      {loading && <p className="text-gray-500 mb-6">Cargando estadísticas...</p>}

      {error && (
        <div className="mb-6 p-4 rounded-lg border border-amber-300 bg-amber-50 text-amber-800 text-sm">
          {error}
        </div>
      )}

      {/* Stat cards */}
      {stats && (
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
        {CARDS(stats).map(({ label, value, icon: Icon, iconBg, iconColor }) => (
          <div key={label} className="bg-dark-800 rounded-xl p-5 border border-dark-700">
            <div className={`w-10 h-10 rounded-lg ${iconBg} flex items-center justify-center mb-3`}>
              <Icon className={`w-5 h-5 ${iconColor}`} />
            </div>
            <p className="text-2xl font-bold text-gray-900">{value}</p>
            <p className="text-sm text-gray-500 mt-1">{label}</p>
          </div>
        ))}
      </div>
      )}

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
        <QuickBiteInfoCard />

        {/* Órdenes por estado */}
        {stats ? (
        <div className="bg-dark-800 rounded-xl border border-dark-700 p-6">
        <h3 className="text-gray-800 font-semibold mb-5">Órdenes por estado</h3>
        <div className="space-y-3">
          {Object.entries(stats.orders_by_status).map(([key, count]) => {
            const meta = STATUS_META[key] ?? { label: key, bar: 'bg-gray-400', badge: 'bg-gray-100 text-gray-500' }
            const pct = Math.round((count / total) * 100)
            return (
              <div key={key} className="flex items-center gap-4">
                <span className={`text-xs font-medium px-2.5 py-1 rounded-full w-28 text-center shrink-0 ${meta.badge}`}>
                  {meta.label}
                </span>
                <div className="flex-1 bg-dark-700 rounded-full h-2">
                  <div
                    className={`${meta.bar} h-2 rounded-full transition-all`}
                    style={{ width: `${pct}%` }}
                  />
                </div>
                <span className="text-sm text-gray-600 w-6 text-right shrink-0">{count}</span>
              </div>
            )
          })}
        </div>

        <div className="mt-5 pt-4 border-t border-dark-700">
          <Link to="/admin/orders" className="text-sm text-brand-400 hover:text-brand-300 transition-colors">
            Ver todas las órdenes →
          </Link>
        </div>
        </div>
        ) : (
          !loading && (
            <div className="bg-dark-800 rounded-xl border border-dark-700 p-6 text-gray-500 text-sm">
              Las órdenes por estado aparecerán cuando Django responda en el puerto 8000.
            </div>
          )
        )}
      </div>
    </div>
  )
}

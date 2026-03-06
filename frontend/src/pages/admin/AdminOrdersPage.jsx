import { useEffect, useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { PlusIcon, TrashIcon } from '@heroicons/react/24/outline'
import toast from 'react-hot-toast'
import { getAdminOrders, deleteAdminOrder } from '../../api/admin'

const STATUS_OPTIONS = [
  { value: '',          label: 'Todas' },
  { value: 'pending',   label: 'Pendiente' },
  { value: 'confirmed', label: 'Confirmado' },
  { value: 'shipped',   label: 'Enviado' },
  { value: 'delivered', label: 'Entregado' },
  { value: 'cancelled', label: 'Cancelado' },
]

const STATUS_BADGE = {
  pending:   'bg-yellow-500/15 text-yellow-400',
  confirmed: 'bg-blue-500/15 text-blue-400',
  shipped:   'bg-purple-500/15 text-purple-400',
  delivered: 'bg-emerald-500/15 text-emerald-400',
  cancelled: 'bg-red-500/15 text-red-400',
}

const STATUS_LABEL = {
  pending: 'Pendiente', confirmed: 'Confirmado', shipped: 'Enviado',
  delivered: 'Entregado', cancelled: 'Cancelado',
}

export default function AdminOrdersPage() {
  const navigate = useNavigate()
  const [orders, setOrders]       = useState([])
  const [loading, setLoading]     = useState(true)
  const [statusFilter, setStatus] = useState('')

  const load = (s) => {
    setLoading(true)
    getAdminOrders(s).then(setOrders).finally(() => setLoading(false))
  }

  useEffect(() => { load(statusFilter) }, [statusFilter])

  const handleDelete = async (id) => {
    if (!confirm(`¿Eliminar la orden #${id}? Esta acción no se puede deshacer.`)) return
    try {
      await deleteAdminOrder(id)
      setOrders(prev => prev.filter(o => o.id !== id))
      toast.success(`Orden #${id} eliminada`)
    } catch {
      toast.error('Error al eliminar la orden')
    }
  }

  return (
    <div className="p-8">
      <div className="flex items-center justify-between mb-6">
        <div>
          <h2 className="text-2xl font-bold text-gray-900 mb-1">Órdenes</h2>
          <p className="text-gray-500 text-sm">Gestiona y filtra todas las órdenes</p>
        </div>
        <button onClick={() => navigate('/admin/orders/new')}
          className="flex items-center gap-2 px-4 py-2 bg-brand-600 hover:bg-brand-500
                     text-white text-sm font-medium rounded-lg transition-colors">
          <PlusIcon className="w-4 h-4" /> Nueva orden
        </button>
      </div>

      {/* Filtros */}
      <div className="flex flex-wrap gap-2 mb-6">
        {STATUS_OPTIONS.map(({ value, label }) => (
          <button key={value} onClick={() => setStatus(value)}
            className={`px-4 py-1.5 rounded-full text-sm font-medium transition-colors ${
              statusFilter === value
                ? 'bg-brand-500 text-white'
                : 'bg-dark-700 text-gray-600 hover:bg-dark-600 hover:text-gray-900'
            }`}>
            {label}
          </button>
        ))}
      </div>

      {/* Tabla */}
      {loading ? (
        <p className="text-gray-500">Cargando...</p>
      ) : orders.length === 0 ? (
        <div className="bg-dark-800 rounded-xl border border-dark-600 p-10 text-center text-gray-500">
          No hay órdenes con ese filtro.
        </div>
      ) : (
        <div className="bg-dark-800 rounded-xl border border-dark-700 overflow-hidden">
          <table className="w-full text-sm">
            <thead>
              <tr className="border-b border-dark-600 text-gray-500 text-left">
                <th className="px-5 py-3 font-medium">#</th>
                <th className="px-5 py-3 font-medium">Cliente</th>
                <th className="px-5 py-3 font-medium">Email</th>
                <th className="px-5 py-3 font-medium">Total</th>
                <th className="px-5 py-3 font-medium">Estado</th>
                <th className="px-5 py-3 font-medium">Fecha</th>
                <th className="px-5 py-3 font-medium text-center">Acciones</th>
              </tr>
            </thead>
            <tbody>
              {orders.map(order => (
                <tr key={order.id}
                  className="border-b border-dark-700/60 hover:bg-dark-700/40 transition-colors">
                  <td className="px-5 py-3 text-gray-600 font-mono">{order.id}</td>
                  <td className="px-5 py-3 text-gray-800">{order.customer_nombre}</td>
                  <td className="px-5 py-3 text-gray-500">{order.customer_email}</td>
                  <td className="px-5 py-3 text-gray-800 font-medium">
                    ${Number(order.total).toLocaleString('es-CO')}
                  </td>
                  <td className="px-5 py-3">
                    <span className={`text-xs font-medium px-2.5 py-1 rounded-full
                      ${STATUS_BADGE[order.status] ?? 'bg-gray-200 text-gray-600'}`}>
                      {STATUS_LABEL[order.status] ?? order.status}
                    </span>
                  </td>
                  <td className="px-5 py-3 text-gray-500">
                    {new Date(order.fecha_creacion).toLocaleDateString('es-CO')}
                  </td>
                  <td className="px-5 py-3">
                    <div className="flex items-center justify-center gap-2">
                      <Link to={`/admin/orders/${order.id}`}
                        className="text-brand-600 hover:text-brand-500 text-xs font-medium transition-colors">
                        Ver →
                      </Link>
                      <button onClick={() => handleDelete(order.id)}
                        className="p-1.5 text-gray-400 hover:text-red-500 hover:bg-red-50
                                   rounded-lg transition-colors" title="Eliminar">
                        <TrashIcon className="w-4 h-4" />
                      </button>
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  )
}

import { useEffect, useState } from 'react'
import { useParams, Link } from 'react-router-dom'
import { getAdminOrder, updateOrderStatus } from '../../api/admin'
import toast from 'react-hot-toast'

const STATUS_OPTIONS = [
  { value: 'pending',   label: 'Pendiente'  },
  { value: 'confirmed', label: 'Confirmado' },
  { value: 'shipped',   label: 'Enviado'    },
  { value: 'delivered', label: 'Entregado'  },
  { value: 'cancelled', label: 'Cancelado'  },
]

const STATUS_BADGE = {
  pending:   'bg-yellow-500/15 text-yellow-400',
  confirmed: 'bg-blue-500/15 text-blue-400',
  shipped:   'bg-purple-500/15 text-purple-400',
  delivered: 'bg-emerald-500/15 text-emerald-400',
  cancelled: 'bg-red-500/15 text-red-400',
}

export default function AdminOrderDetailPage() {
  const { id } = useParams()
  const [order, setOrder]         = useState(null)
  const [loading, setLoading]     = useState(true)
  const [newStatus, setNewStatus] = useState('')
  const [saving, setSaving]       = useState(false)

  useEffect(() => {
    getAdminOrder(id)
      .then((data) => {
        setOrder(data)
        setNewStatus(data.status)
      })
      .finally(() => setLoading(false))
  }, [id])

  const handleStatusChange = async () => {
    if (newStatus === order.status) return
    setSaving(true)
    try {
      await updateOrderStatus(id, newStatus)
      setOrder((prev) => ({ ...prev, status: newStatus }))
      toast.success('Estado actualizado')
    } catch {
      toast.error('Error al actualizar el estado')
    } finally {
      setSaving(false)
    }
  }

  if (loading) return <div className="p-8 text-gray-500">Cargando...</div>
  if (!order)  return <div className="p-8 text-red-500">Orden no encontrada</div>

  return (
    <div className="p-8 max-w-4xl">
      {/* Encabezado */}
      <div className="flex items-center gap-3 mb-6">
        <Link to="/admin/orders" className="text-gray-500 hover:text-gray-800 text-sm transition-colors">
          ← Órdenes
        </Link>
        <span className="text-gray-400">/</span>
        <h2 className="text-2xl font-bold text-gray-900">Orden #{order.id}</h2>
        <span className={`text-xs font-medium px-2.5 py-1 rounded-full ${STATUS_BADGE[order.status]}`}>
          {STATUS_OPTIONS.find(s => s.value === order.status)?.label ?? order.status}
        </span>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
        {/* Info cliente */}
        <div className="bg-dark-800 rounded-xl border border-dark-700 p-5">
          <h3 className="text-gray-500 text-xs font-medium uppercase tracking-wider mb-3">Cliente</h3>
          <p className="text-gray-900 font-medium">{order.customer_nombre}</p>
          <p className="text-gray-500 text-sm">{order.customer_email}</p>
          <p className="text-gray-400 text-sm mt-2">
            {new Date(order.fecha_creacion).toLocaleString('es-CO')}
          </p>
        </div>

        {/* Info envío */}
        <div className="bg-dark-800 rounded-xl border border-dark-700 p-5">
          <h3 className="text-gray-500 text-xs font-medium uppercase tracking-wider mb-3">Envío</h3>
          <p className="text-gray-800 text-sm">{order.direccion_envio}</p>
          {order.tracking_number && (
            <p className="text-gray-400 text-xs mt-2">
              Tracking: <span className="font-mono text-gray-700">{order.tracking_number}</span>
            </p>
          )}
        </div>
      </div>

      {/* Items */}
      <div className="bg-dark-800 rounded-xl border border-dark-700 overflow-hidden mb-6">
        <div className="px-5 py-4 border-b border-dark-700">
          <h3 className="text-gray-800 font-semibold">Productos</h3>
        </div>
        <table className="w-full text-sm">
          <thead>
            <tr className="border-b border-dark-600 text-gray-500">
              <th className="px-5 py-3 text-left font-medium">Producto</th>
              <th className="px-5 py-3 text-right font-medium">Cant.</th>
              <th className="px-5 py-3 text-right font-medium">Precio</th>
              <th className="px-5 py-3 text-right font-medium">Subtotal</th>
            </tr>
          </thead>
          <tbody>
            {order.items.map((item) => (
              <tr key={item.id} className="border-b border-dark-600/60">
                <td className="px-5 py-3 text-gray-800">{item.product_name}</td>
                <td className="px-5 py-3 text-right text-gray-700">{item.quantity}</td>
                <td className="px-5 py-3 text-right text-gray-700">
                  ${Number(item.price).toLocaleString('es-CO')}
                </td>
                <td className="px-5 py-3 text-right text-gray-800 font-medium">
                  ${Number(item.subtotal).toLocaleString('es-CO')}
                </td>
              </tr>
            ))}
          </tbody>
        </table>

        {/* Totales */}
        <div className="px-5 py-4 space-y-1.5 border-t border-dark-700">
          <div className="flex justify-between text-sm text-gray-500">
            <span>Subtotal</span>
            <span>${Number(order.subtotal).toLocaleString('es-CO')}</span>
          </div>
          {Number(order.discount_amount) > 0 && (
            <div className="flex justify-between text-sm text-emerald-400">
              <span>Descuento {order.discount_code && `(${order.discount_code})`}</span>
              <span>−${Number(order.discount_amount).toLocaleString('es-CO')}</span>
            </div>
          )}
          <div className="flex justify-between text-base font-bold text-gray-900 pt-1 border-t border-dark-600">
            <span>Total</span>
            <span>${Number(order.total).toLocaleString('es-CO')}</span>
          </div>
        </div>
      </div>

      {/* Cambiar estado */}
      <div className="bg-dark-800 rounded-xl border border-dark-700 p-5">
        <h3 className="text-gray-800 font-semibold mb-4">Actualizar estado</h3>
        <div className="flex items-center gap-3">
          <select
            value={newStatus}
            onChange={(e) => setNewStatus(e.target.value)}
            className="bg-white text-gray-900 border border-dark-600 rounded-lg px-3 py-2 text-sm
                       focus:outline-none focus:ring-1 focus:ring-brand-500"
          >
            {STATUS_OPTIONS.map(({ value, label }) => (
              <option key={value} value={value}>{label}</option>
            ))}
          </select>
          <button
            onClick={handleStatusChange}
            disabled={saving || newStatus === order.status}
            className="px-4 py-2 bg-brand-600 hover:bg-brand-500 disabled:opacity-50 disabled:cursor-not-allowed
                       text-white text-sm font-medium rounded-lg transition-colors"
          >
            {saving ? 'Guardando...' : 'Guardar cambio'}
          </button>
        </div>
      </div>
    </div>
  )
}

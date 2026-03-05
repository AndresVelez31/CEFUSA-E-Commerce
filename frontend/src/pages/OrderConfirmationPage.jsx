import { useEffect, useState } from 'react'
import { useParams, useLocation, Link } from 'react-router-dom'
import { CheckCircleIcon, ArrowTopRightOnSquareIcon } from '@heroicons/react/24/outline'
import { getOrder } from '../api/orders'

export default function OrderConfirmationPage() {
  const { id } = useParams()
  const { state: orderFromCheckout } = useLocation()
  const [order, setOrder]   = useState(orderFromCheckout || null)
  const [loading, setLoading] = useState(!orderFromCheckout)

  useEffect(() => {
    if (!orderFromCheckout) {
      getOrder(id)
        .then(setOrder)
        .finally(() => setLoading(false))
    }
  }, [id, orderFromCheckout])

  if (loading) {
    return (
      <div className="max-w-lg mx-auto px-4 py-20 text-center animate-pulse">
        <div className="h-20 w-20 bg-dark-700 rounded-full mx-auto mb-4" />
        <div className="h-6 bg-dark-700 rounded w-1/2 mx-auto" />
      </div>
    )
  }

  return (
    <div className="max-w-lg mx-auto px-4 sm:px-6 py-16">
      <div className="card p-8 text-center space-y-6">
        {/* Icon */}
        <div className="w-20 h-20 bg-green-900/40 rounded-full flex items-center justify-center mx-auto">
          <CheckCircleIcon className="w-10 h-10 text-green-400" />
        </div>

        <div>
          <h1 className="text-2xl font-extrabold text-white">¡Orden confirmada!</h1>
          <p className="text-slate-400 mt-2">
            Gracias por tu compra. Recibirás una notificación cuando tu pedido esté en camino.
          </p>
        </div>

        {/* Order details */}
        <div className="bg-dark-700 rounded-xl p-4 text-left space-y-3">
          <div className="flex justify-between text-sm">
            <span className="text-slate-500">Número de orden</span>
            <span className="font-mono font-bold text-brand-400">#{order?.order_id || id}</span>
          </div>
          {order?.total && (
            <div className="flex justify-between text-sm">
              <span className="text-slate-500">Total pagado</span>
              <span className="font-bold text-white">${parseFloat(order.total).toFixed(2)}</span>
            </div>
          )}
          {order?.items_count && (
            <div className="flex justify-between text-sm">
              <span className="text-slate-500">Artículos</span>
              <span className="text-slate-300">{order.items_count}</span>
            </div>
          )}
          <div className="flex justify-between text-sm">
            <span className="text-slate-500">Estado</span>
            <span className="badge bg-yellow-900/60 text-yellow-300 border border-yellow-700">
              Pendiente
            </span>
          </div>
        </div>

        {order?.message && (
          <p className="text-sm text-slate-400 italic">"{order.message}"</p>
        )}

        <div className="flex flex-col gap-3 pt-2">
          <Link to="/" className="btn-primary">
            Seguir comprando
          </Link>
        </div>
      </div>
    </div>
  )
}

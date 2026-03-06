import { Link } from 'react-router-dom'
import { ShoppingBagIcon } from '@heroicons/react/24/outline'
import { useCart } from '../context/CartContext'
import CartItem from '../components/cart/CartItem'

export default function CartPage() {
  const { items, subtotal, clearCart } = useCart()

  if (items.length === 0) {
    return (
      <div className="max-w-2xl mx-auto px-4 py-24 text-center">
        <ShoppingBagIcon className="w-20 h-20 mx-auto text-gray-300 mb-4" />
        <h2 className="text-2xl font-bold text-gray-700">Tu carrito está vacío</h2>
        <p className="text-gray-500 mt-2">Agrega productos desde el catálogo</p>
        <Link to="/" className="btn-primary mt-6 inline-block">
          Ver catálogo
        </Link>
      </div>
    )
  }

  return (
    <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-10">
      <div className="flex items-center justify-between mb-8">
        <h1 className="section-title">Carrito de compras</h1>
        <button onClick={clearCart} className="text-sm text-red-400 hover:text-red-300 transition-colors">
          Vaciar carrito
        </button>
      </div>

      <div className="grid lg:grid-cols-3 gap-8">
        {/* Items */}
        <div className="lg:col-span-2 space-y-3">
          {items.map(item => (
            <CartItem key={item.variant_id} item={item} />
          ))}
        </div>

        {/* Summary */}
        <div className="card p-6 h-fit space-y-4">
          <h2 className="font-bold text-lg text-gray-900">Resumen</h2>

          <div className="space-y-2 text-sm">
            {items.map(item => (
              <div key={item.variant_id} className="flex justify-between text-gray-500">
                <span className="truncate max-w-[160px]">
                  {item.product_name} ×{item.quantity}
                </span>
                <span>${(parseFloat(item.price) * item.quantity).toLocaleString('es-CO')}</span>
              </div>
            ))}
          </div>

          <div className="border-t border-dark-600 pt-3 flex justify-between font-bold text-gray-900">
            <span>Subtotal</span>
            <span className="text-brand-600">${subtotal.toLocaleString('es-CO')}</span>
          </div>

          <p className="text-xs text-gray-400">
            El descuento y costo de envío se calculan en el checkout.
          </p>

          <Link to="/checkout" className="btn-primary w-full text-center block">
            Proceder al checkout
          </Link>

          <Link to="/" className="btn-secondary w-full text-center block text-sm">
            Seguir comprando
          </Link>
        </div>
      </div>
    </div>
  )
}

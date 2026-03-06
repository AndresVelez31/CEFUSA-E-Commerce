import { TrashIcon, MinusIcon, PlusIcon } from '@heroicons/react/24/outline'
import { useCart } from '../../context/CartContext'

export default function CartItem({ item }) {
  const { updateQuantity, removeItem } = useCart()

  return (
    <div className="card p-4 flex items-center gap-4">
      {/* Icon placeholder */}
      <div className="w-16 h-16 rounded-xl bg-dark-700 flex-shrink-0 flex items-center justify-center text-2xl">
        🛒
      </div>

      {/* Info */}
      <div className="flex-grow min-w-0">
        <p className="font-semibold text-gray-800 truncate">{item.product_name}</p>
        <p className="text-xs text-gray-500 mt-0.5">
          SKU: {item.sku}
          {item.size  && ` · Talla: ${item.size}`}
          {item.color && ` · Color: ${item.color}`}
        </p>
        <p className="text-brand-600 font-bold mt-1">
          ${(parseFloat(item.price) * item.quantity).toLocaleString('es-CO')}
        </p>
      </div>

      {/* Quantity controls */}
      <div className="flex items-center gap-1.5">
        <button
          onClick={() => updateQuantity(item.variant_id, item.quantity - 1)}
          className="w-8 h-8 rounded-lg bg-dark-700 hover:bg-dark-600 flex items-center justify-center text-gray-600 transition-colors"
        >
          <MinusIcon className="w-3.5 h-3.5" />
        </button>
        <span className="w-8 text-center font-semibold text-gray-800">{item.quantity}</span>
        <button
          onClick={() => updateQuantity(item.variant_id, item.quantity + 1)}
          className="w-8 h-8 rounded-lg bg-dark-700 hover:bg-dark-600 flex items-center justify-center text-gray-600 transition-colors"
        >
          <PlusIcon className="w-3.5 h-3.5" />
        </button>
      </div>

      {/* Remove */}
      <button
        onClick={() => removeItem(item.variant_id)}
        className="p-2 rounded-xl text-red-400 hover:bg-red-900/30 transition-colors"
      >
        <TrashIcon className="w-5 h-5" />
      </button>
    </div>
  )
}

import { Link } from 'react-router-dom'
import { ShoppingCartIcon, StarIcon } from '@heroicons/react/24/solid'
import { TagIcon } from '@heroicons/react/24/outline'
import toast from 'react-hot-toast'
import { useCart } from '../../context/CartContext'

const CATEGORY_LABELS = {
  clothes:    'Ropa',
  accesories: 'Accesorios',
  other:      'Otros',
}

export default function ProductCard({ product }) {
  const { addItem } = useCart()

  // Tomar la primera variante disponible como representativa
  const firstVariant = product.variants?.find(v => v.is_available) || product.variants?.[0]
  const minPrice = product.variants?.reduce(
    (min, v) => (parseFloat(v.price) < min ? parseFloat(v.price) : min),
    Infinity
  )

  const handleQuickAdd = (e) => {
    e.preventDefault()
    if (!firstVariant) return
    addItem({
      variant_id: firstVariant.id,
      product_id: product.id,
      product_name: product.name,
      sku: firstVariant.sku,
      size: firstVariant.size,
      color: firstVariant.color,
      price: firstVariant.price,
      quantity: 1,
    })
    toast.success(`${product.name} agregado al carrito`)
  }

  return (
    <Link to={`/products/${product.id}`} className="group block">
      <div className="card overflow-hidden transition-all duration-300 hover:border-brand-400 hover:shadow-xl hover:shadow-brand-100 hover:-translate-y-1">
        {/* Image placeholder */}
        <div className="relative h-52 bg-gradient-to-br from-dark-700 to-dark-600 flex items-center justify-center overflow-hidden">
          <TagIcon className="w-16 h-16 text-gray-200 group-hover:text-brand-200 transition-colors duration-300" />
          <span className="absolute top-3 left-3 badge bg-brand-100 text-brand-700 border border-brand-200">
            {CATEGORY_LABELS[product.category] ?? product.category}
          </span>
          {!firstVariant?.is_available && (
            <span className="absolute top-3 right-3 badge bg-red-100 text-red-600 border border-red-200">
              Sin stock
            </span>
          )}
        </div>

        {/* Content */}
        <div className="p-4 space-y-3">
          <div>
            <h3 className="font-semibold text-gray-800 text-base leading-snug group-hover:text-brand-600 transition-colors line-clamp-2">
              {product.name}
            </h3>
            <p className="text-xs text-gray-500 mt-1 line-clamp-2">{product.description}</p>
          </div>

          {/* Variantes disponibles */}
          {product.variants && product.variants.length > 1 && (
            <div className="flex flex-wrap gap-1">
              {product.variants.slice(0, 4).map(v => (
                <span key={v.id} className="text-xs px-2 py-0.5 rounded-md bg-dark-700 text-gray-600 border border-dark-600">
                  {v.size || v.color || v.sku}
                </span>
              ))}
              {product.variants.length > 4 && (
                <span className="text-xs px-2 py-0.5 rounded-md bg-dark-700 text-gray-400">
                  +{product.variants.length - 4}
                </span>
              )}
            </div>
          )}

          {/* Price + Add */}
          <div className="flex items-center justify-between pt-1">
            <div>
              {minPrice !== Infinity && (
                <span className="text-lg font-bold text-brand-600">
                  {minPrice === parseFloat(firstVariant?.price)
                    ? `$${parseFloat(firstVariant?.price).toLocaleString('es-CO')}`
                    : `Desde $${minPrice.toLocaleString('es-CO')}`}
                </span>
              )}
            </div>
            <button
              onClick={handleQuickAdd}
              disabled={!firstVariant?.is_available}
              className="btn-primary py-2 px-3 text-sm flex items-center gap-1.5"
            >
              <ShoppingCartIcon className="w-4 h-4" />
              Agregar
            </button>
          </div>
        </div>
      </div>
    </Link>
  )
}

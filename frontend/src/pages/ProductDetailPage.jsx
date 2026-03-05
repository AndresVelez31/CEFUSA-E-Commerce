import { useState, useEffect } from 'react'
import { useParams, Link } from 'react-router-dom'
import { ShoppingCartIcon, ArrowLeftIcon, CheckCircleIcon } from '@heroicons/react/24/outline'
import toast from 'react-hot-toast'
import { getProduct } from '../api/products'
import { useCart } from '../context/CartContext'

export default function ProductDetailPage() {
  const { id } = useParams()
  const { addItem } = useCart()

  const [product, setProduct]           = useState(null)
  const [loading, setLoading]           = useState(true)
  const [selectedVariant, setSelected]  = useState(null)
  const [quantity, setQuantity]         = useState(1)
  const [added, setAdded]               = useState(false)

  useEffect(() => {
    getProduct(id)
      .then(data => {
        setProduct(data)
        const first = data.variants?.find(v => v.is_available) || data.variants?.[0]
        setSelected(first)
      })
      .catch(() => toast.error('Error al cargar el producto'))
      .finally(() => setLoading(false))
  }, [id])

  const handleAddToCart = () => {
    if (!selectedVariant) return
    addItem({
      variant_id: selectedVariant.id,
      product_id: product.id,
      product_name: product.name,
      sku: selectedVariant.sku,
      size: selectedVariant.size,
      color: selectedVariant.color,
      price: selectedVariant.price,
      quantity,
    })
    setAdded(true)
    toast.success('Producto agregado al carrito')
    setTimeout(() => setAdded(false), 2000)
  }

  if (loading) {
    return (
      <div className="max-w-5xl mx-auto px-4 py-10 animate-pulse">
        <div className="grid md:grid-cols-2 gap-8">
          <div className="h-96 bg-dark-700 rounded-2xl" />
          <div className="space-y-4">
            <div className="h-8 bg-dark-700 rounded w-3/4" />
            <div className="h-4 bg-dark-700 rounded w-1/2" />
            <div className="h-24 bg-dark-700 rounded" />
          </div>
        </div>
      </div>
    )
  }

  if (!product) {
    return (
      <div className="text-center py-20 text-slate-500">
        <p className="text-4xl mb-3">😕</p>
        <p>Producto no encontrado</p>
        <Link to="/" className="btn-primary mt-4 inline-block">Volver al inicio</Link>
      </div>
    )
  }

  const inStock = selectedVariant?.is_available

  return (
    <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-10">
      {/* Back */}
      <Link to="/" className="inline-flex items-center gap-2 text-slate-400 hover:text-brand-400 text-sm mb-8 transition-colors">
        <ArrowLeftIcon className="w-4 h-4" />
        Volver al catálogo
      </Link>

      <div className="grid md:grid-cols-2 gap-10">
        {/* Image */}
        <div className="card h-80 md:h-full flex items-center justify-center bg-gradient-to-br from-dark-700 to-dark-800 text-8xl rounded-2xl">
          🛍️
        </div>

        {/* Details */}
        <div className="space-y-6">
          <div>
            <span className="badge bg-brand-900/60 text-brand-300 border border-brand-700 mb-2">
              {product.category}
            </span>
            <h1 className="text-3xl font-extrabold text-white mt-2">{product.name}</h1>
            <p className="text-slate-400 mt-3 leading-relaxed">{product.description}</p>
          </div>

          {/* Variants selection */}
          {product.variants && product.variants.length > 0 && (
            <div>
              <p className="label">Variante</p>
              <div className="flex flex-wrap gap-2">
                {product.variants.map(v => (
                  <button
                    key={v.id}
                    onClick={() => { setSelected(v); setQuantity(1) }}
                    disabled={!v.is_available}
                    className={`px-4 py-2 rounded-xl text-sm font-medium border transition-all
                      ${selectedVariant?.id === v.id
                        ? 'bg-brand-600 border-brand-500 text-white'
                        : v.is_available
                          ? 'bg-dark-700 border-dark-600 text-slate-300 hover:border-brand-600'
                          : 'bg-dark-800 border-dark-700 text-slate-600 line-through cursor-not-allowed'
                      }`}
                  >
                    {[v.size, v.color].filter(Boolean).join(' / ') || v.sku}
                  </button>
                ))}
              </div>
            </div>
          )}

          {/* Price */}
          <div>
            <p className="text-4xl font-extrabold text-brand-400">
              ${parseFloat(selectedVariant?.price || 0).toFixed(2)}
            </p>
            {!inStock && (
              <p className="text-red-400 text-sm mt-1">⚠️ Sin stock disponible</p>
            )}
          </div>

          {/* Quantity */}
          <div>
            <p className="label">Cantidad</p>
            <div className="flex items-center gap-3">
              <button
                onClick={() => setQuantity(q => Math.max(1, q - 1))}
                className="w-10 h-10 rounded-xl bg-dark-700 hover:bg-dark-600 flex items-center justify-center text-slate-200 font-bold text-lg transition-colors"
              >
                −
              </button>
              <span className="text-xl font-bold text-white w-8 text-center">{quantity}</span>
              <button
                onClick={() => setQuantity(q => q + 1)}
                className="w-10 h-10 rounded-xl bg-dark-700 hover:bg-dark-600 flex items-center justify-center text-slate-200 font-bold text-lg transition-colors"
              >
                +
              </button>
            </div>
          </div>

          {/* Add to cart */}
          <button
            onClick={handleAddToCart}
            disabled={!inStock || !selectedVariant}
            className={`btn-primary w-full flex items-center justify-center gap-2 py-3 text-base ${added ? 'bg-green-600 hover:bg-green-600' : ''}`}
          >
            {added
              ? <><CheckCircleIcon className="w-5 h-5" /> Agregado</>
              : <><ShoppingCartIcon className="w-5 h-5" /> Agregar al carrito</>
            }
          </button>
        </div>
      </div>
    </div>
  )
}

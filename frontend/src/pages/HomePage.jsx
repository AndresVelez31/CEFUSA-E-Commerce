import { useState, useEffect } from 'react'
import { MagnifyingGlassIcon, FunnelIcon } from '@heroicons/react/24/outline'
import { getProducts } from '../api/products'
import ProductCard from '../components/products/ProductCard'

const CATEGORIES = ['Todos', 'Electrónica', 'Ropa', 'Calzado', 'Hogar', 'Deportes']

export default function HomePage() {
  const [products, setProducts]   = useState([])
  const [loading, setLoading]     = useState(true)
  const [search, setSearch]       = useState('')
  const [category, setCategory]   = useState('Todos')
  const [error, setError]         = useState(null)

  useEffect(() => {
    setLoading(true)
    getProducts()
      .then(data => {
        setProducts(Array.isArray(data) ? data : data.results || [])
        setError(null)
      })
      .catch(() => setError('No se pudo cargar el catálogo. Verifica que el servidor esté corriendo.'))
      .finally(() => setLoading(false))
  }, [])

  const filtered = products.filter(p => {
    const matchSearch  = p.name.toLowerCase().includes(search.toLowerCase())
    const matchCat     = category === 'Todos' || p.category === category
    return matchSearch && matchCat
  })

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-10">
      {/* Hero */}
      <div className="text-center mb-12">
        <h1 className="text-4xl sm:text-5xl font-extrabold text-white leading-tight">
          Catálogo de{' '}
          <span className="text-transparent bg-clip-text bg-gradient-to-r from-brand-400 to-brand-600">
            Productos
          </span>
        </h1>
        <p className="mt-3 text-slate-400 text-lg max-w-xl mx-auto">
          Encuentra lo que necesitas con los mejores precios
        </p>
      </div>

      {/* Filters */}
      <div className="flex flex-col sm:flex-row gap-3 mb-8">
        {/* Search */}
        <div className="relative flex-grow">
          <MagnifyingGlassIcon className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-slate-500" />
          <input
            type="text"
            placeholder="Buscar productos..."
            value={search}
            onChange={e => setSearch(e.target.value)}
            className="input-field pl-10"
          />
        </div>

        {/* Category filter */}
        <div className="relative">
          <FunnelIcon className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-500" />
          <select
            value={category}
            onChange={e => setCategory(e.target.value)}
            className="input-field pl-9 pr-8 appearance-none cursor-pointer min-w-[160px]"
          >
            {CATEGORIES.map(c => <option key={c} value={c}>{c}</option>)}
          </select>
        </div>
      </div>

      {/* Error */}
      {error && (
        <div className="card border-red-800 bg-red-950/30 p-6 text-center text-red-400 mb-8">
          {error}
        </div>
      )}

      {/* Loading skeletons */}
      {loading && (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
          {Array.from({ length: 8 }).map((_, i) => (
            <div key={i} className="card overflow-hidden animate-pulse">
              <div className="h-52 bg-dark-700" />
              <div className="p-4 space-y-3">
                <div className="h-4 bg-dark-700 rounded w-3/4" />
                <div className="h-3 bg-dark-700 rounded w-1/2" />
                <div className="h-8 bg-dark-700 rounded" />
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Products Grid */}
      {!loading && !error && (
        <>
          <p className="text-sm text-slate-500 mb-4">
            {filtered.length} producto{filtered.length !== 1 ? 's' : ''} encontrado{filtered.length !== 1 ? 's' : ''}
          </p>
          {filtered.length > 0 ? (
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
              {filtered.map(product => (
                <ProductCard key={product.id} product={product} />
              ))}
            </div>
          ) : (
            <div className="text-center py-20 text-slate-500">
              <p className="text-6xl mb-4">🔍</p>
              <p className="text-lg font-medium">No se encontraron productos</p>
              <p className="text-sm mt-1">Intenta con otra búsqueda o categoría</p>
            </div>
          )}
        </>
      )}
    </div>
  )
}

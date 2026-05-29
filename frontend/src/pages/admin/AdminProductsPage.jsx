import { useEffect, useState, useRef } from 'react'
import {
  PlusIcon,
  PencilIcon,
  TrashIcon,
  CubeIcon,
  AdjustmentsHorizontalIcon,
} from '@heroicons/react/24/outline'
import toast from 'react-hot-toast'
import {
  getProducts,
  createProduct,
  updateProduct,
  deleteProduct,
  addVariant,
  updateVariant,
  deleteVariant,
  updateStock,
} from '../../api/products'

// ─── helpers ────────────────────────────────────────────────────────────────

const EMPTY_PRODUCT = { name: '', description: '', category: '', is_active: true }
const EMPTY_VARIANT = { sku: '', size: '', color: '', price: '', initial_stock: 0 }

function FieldError({ errors, name }) {
  if (!errors?.[name]) return null
  const msg = Array.isArray(errors[name]) ? errors[name][0] : errors[name]
  return <p className="text-red-400 text-xs mt-1">{msg}</p>
}

// ─── Modal: crear / editar producto ─────────────────────────────────────────

function ProductModal({ open, onClose, initial, onSaved }) {
  const [form, setForm]     = useState(EMPTY_PRODUCT)
  const [errors, setErrors] = useState({})
  const [saving, setSaving] = useState(false)
  const firstRef = useRef(null)
  const isEdit = Boolean(initial)

  useEffect(() => {
    if (open) {
      setForm(initial
        ? { name: initial.name, description: initial.description,
            category: initial.category, is_active: initial.is_active }
        : EMPTY_PRODUCT)
      setErrors({})
      setTimeout(() => firstRef.current?.focus(), 50)
    }
  }, [open, initial])

  if (!open) return null

  const change = (e) => {
    const val = e.target.type === 'checkbox' ? e.target.checked : e.target.value
    setForm(p => ({ ...p, [e.target.name]: val }))
  }

  const validate = () => {
    const e = {}
    if (!form.name.trim())     e.name     = 'Requerido'
    if (!form.category.trim()) e.category = 'Requerido'
    return e
  }

  const submit = async (ev) => {
    ev.preventDefault()
    const e = validate()
    if (Object.keys(e).length) { setErrors(e); return }
    setSaving(true)
    try {
      const saved = isEdit
        ? await updateProduct(initial.id, form)
        : await createProduct({ ...form, variants: [] })
      onSaved(saved, isEdit)
      toast.success(isEdit ? 'Producto actualizado' : 'Producto creado')
      onClose()
    } catch (err) {
      const data = err.response?.data
      if (data && typeof data === 'object') setErrors(data)
      else toast.error('Error al guardar')
    } finally {
      setSaving(false)
    }
  }

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/60">
      <div className="bg-dark-800 border border-dark-600 rounded-2xl w-full max-w-lg mx-4 shadow-2xl">
        <div className="flex items-center justify-between px-6 py-4 border-b border-dark-700">
          <h3 className="text-gray-900 font-semibold">
            {isEdit ? 'Editar producto' : 'Nuevo producto'}
          </h3>
          <button onClick={onClose}
            className="text-gray-400 hover:text-gray-800 text-xl leading-none">×</button>
        </div>
        <form onSubmit={submit} className="p-6 space-y-4">
          <div>
            <label className="block text-xs text-gray-600 mb-1">Nombre *</label>
            <input ref={firstRef} type="text" name="name" value={form.name} onChange={change}
              className={`w-full bg-white border rounded-lg px-3 py-2 text-sm text-gray-900
                placeholder-gray-400 focus:outline-none focus:ring-1 focus:ring-brand-500 transition
                ${errors.name ? 'border-red-500' : 'border-dark-600'}`} />
            <FieldError errors={errors} name="name" />
          </div>
          <div>
            <label className="block text-xs text-gray-600 mb-1">Categoría *</label>
            <input type="text" name="category" value={form.category} onChange={change}
              className={`w-full bg-white border rounded-lg px-3 py-2 text-sm text-gray-900
                placeholder-gray-400 focus:outline-none focus:ring-1 focus:ring-brand-500 transition
                ${errors.category ? 'border-red-500' : 'border-dark-600'}`} />
            <FieldError errors={errors} name="category" />
          </div>
          <div>
            <label className="block text-xs text-gray-600 mb-1">Descripción</label>
            <textarea name="description" value={form.description} onChange={change} rows={3}
              className="w-full bg-white border border-dark-600 rounded-lg px-3 py-2
                text-sm text-gray-900 placeholder-gray-400 focus:outline-none
                focus:ring-1 focus:ring-brand-500 transition resize-none" />
          </div>
          <div className="flex items-center gap-3">
            <input type="checkbox" id="is_active" name="is_active"
              checked={form.is_active} onChange={change}
              className="w-4 h-4 accent-brand-500 rounded" />
            <label htmlFor="is_active" className="text-sm text-gray-700">Activo</label>
          </div>
          <div className="flex justify-end gap-3 pt-2">
            <button type="button" onClick={onClose}
              className="px-4 py-2 text-sm text-gray-500 hover:text-gray-800 transition-colors">
              Cancelar
            </button>
            <button type="submit" disabled={saving}
              className="px-5 py-2 bg-brand-600 hover:bg-brand-500 disabled:opacity-50
                         text-white text-sm font-medium rounded-lg transition-colors">
              {saving ? 'Guardando…' : isEdit ? 'Guardar cambios' : 'Crear producto'}
            </button>
          </div>
        </form>
      </div>
    </div>
  )
}

// ─── Modal: una variante (crear / editar) ─────────────────────────────────────

function VariantModal({ open, onClose, productId, initial, onSaved }) {
  const [form, setForm]     = useState(EMPTY_VARIANT)
  const [errors, setErrors] = useState({})
  const [saving, setSaving] = useState(false)
  const firstRef = useRef(null)
  const isEdit = Boolean(initial)

  useEffect(() => {
    if (open) {
      setForm(initial
        ? { sku: initial.sku, size: initial.size ?? '', color: initial.color ?? '',
            price: initial.price, initial_stock: initial.inventory?.available_quantity ?? 0 }
        : EMPTY_VARIANT)
      setErrors({})
      setTimeout(() => firstRef.current?.focus(), 50)
    }
  }, [open, initial])

  if (!open) return null

  const change = (e) => setForm(p => ({ ...p, [e.target.name]: e.target.value }))

  const validate = () => {
    const e = {}
    if (!form.sku.trim())      e.sku   = 'Requerido'
    if (!form.price)           e.price = 'Requerido'
    if (!isEdit && form.initial_stock === '') e.initial_stock = 'Requerido'
    return e
  }

  const submit = async (ev) => {
    ev.preventDefault()
    const e = validate()
    if (Object.keys(e).length) { setErrors(e); return }
    setSaving(true)
    try {
      const payload = { ...form, price: parseFloat(form.price) }
      if (isEdit) {
        // En edición no enviamos initial_stock (usan el endpoint de stock)
        const { initial_stock, ...rest } = payload
        const saved = await updateVariant(initial.id, rest)
        onSaved(saved, true)
      } else {
        const saved = await addVariant(productId, payload)
        onSaved(saved, false)
      }
      toast.success(isEdit ? 'Variante actualizada' : 'Variante creada')
      onClose()
    } catch (err) {
      const data = err.response?.data
      if (data && typeof data === 'object') setErrors(data)
      else toast.error('Error al guardar')
    } finally {
      setSaving(false)
    }
  }

  return (
    <div className="fixed inset-0 z-[60] flex items-center justify-center bg-black/70">
      <div className="bg-dark-800 border border-dark-600 rounded-2xl w-full max-w-md mx-4 shadow-2xl">
        <div className="flex items-center justify-between px-6 py-4 border-b border-dark-700">
          <h3 className="text-gray-900 font-semibold">
            {isEdit ? 'Editar variante' : 'Nueva variante'}
          </h3>
          <button onClick={onClose}
            className="text-gray-400 hover:text-gray-800 text-xl leading-none">×</button>
        </div>
        <form onSubmit={submit} className="p-6">
          <div className="grid grid-cols-2 gap-4">
            {[
              { name: 'sku',   label: 'SKU *',    type: 'text',   full: true  },
              { name: 'size',  label: 'Talla',     type: 'text',   full: false },
              { name: 'color', label: 'Color',     type: 'text',   full: false },
              { name: 'price', label: 'Precio *',  type: 'number', full: false },
              ...(!isEdit ? [{ name: 'initial_stock', label: 'Stock inicial', type: 'number', full: false }] : []),
            ].map(({ name, label, type, full }, i) => (
              <div key={name} className={full ? 'col-span-2' : ''}>
                <label className="block text-xs text-gray-600 mb-1">{label}</label>
                <input ref={i === 0 ? firstRef : undefined}
                  type={type} name={name} value={form[name]} onChange={change} min={type === 'number' ? 0 : undefined}
                  step={name === 'price' ? '0.01' : undefined}
                  className={`w-full bg-white border rounded-lg px-3 py-2 text-sm text-gray-900
                    placeholder-gray-400 focus:outline-none focus:ring-1 focus:ring-brand-500 transition
                    ${errors[name] ? 'border-red-500' : 'border-dark-600'}`} />
                <FieldError errors={errors} name={name} />
              </div>
            ))}
          </div>
          <div className="flex justify-end gap-3 mt-6">
            <button type="button" onClick={onClose}
              className="px-4 py-2 text-sm text-gray-500 hover:text-gray-800 transition-colors">
              Cancelar
            </button>
            <button type="submit" disabled={saving}
              className="px-5 py-2 bg-brand-600 hover:bg-brand-500 disabled:opacity-50
                         text-white text-sm font-medium rounded-lg transition-colors">
              {saving ? 'Guardando…' : isEdit ? 'Guardar' : 'Crear variante'}
            </button>
          </div>
        </form>
      </div>
    </div>
  )
}

// ─── Modal: gestionar variantes de un producto ────────────────────────────────

function VariantsModal({ open, onClose, product, onProductUpdated }) {
  const [variants, setVariants]   = useState([])
  const [varModal, setVarModal]   = useState({ open: false, variant: null })
  const [stockEdit, setStockEdit] = useState({}) // variantId → value
  const [savingStock, setSavingStock] = useState({})

  useEffect(() => {
    if (open && product) setVariants(product.variants ?? [])
  }, [open, product])

  if (!open || !product) return null

  const openCreate = () => setVarModal({ open: true, variant: null })
  const openEdit   = (v) => setVarModal({ open: true, variant: v })
  const closeVar   = () => setVarModal({ open: false, variant: null })

  const handleVarSaved = (saved, isEdit) => {
    const updated = isEdit
      ? variants.map(v => v.id === saved.id ? saved : v)
      : [...variants, saved]
    setVariants(updated)
    onProductUpdated({ ...product, variants: updated })
  }

  const handleDeleteVariant = async (v) => {
    if (!confirm(`¿Eliminar la variante ${v.sku}?`)) return
    try {
      await deleteVariant(v.id)
      const updated = variants.filter(x => x.id !== v.id)
      setVariants(updated)
      onProductUpdated({ ...product, variants: updated })
      toast.success('Variante eliminada')
    } catch (err) {
      const status = err.response?.status
      if (status === 409)
        toast.error('No se puede eliminar: tiene órdenes asociadas')
      else
        toast.error('Error al eliminar la variante')
    }
  }

  const startStockEdit = (v) =>
    setStockEdit(prev => ({ ...prev, [v.id]: v.inventory?.available_quantity ?? 0 }))

  const cancelStockEdit = (id) =>
    setStockEdit(prev => { const n = { ...prev }; delete n[id]; return n })

  const saveStock = async (v) => {
    const qty = parseInt(stockEdit[v.id], 10)
    if (isNaN(qty) || qty < 0) { toast.error('Cantidad inválida'); return }
    setSavingStock(prev => ({ ...prev, [v.id]: true }))
    try {
      const saved = await updateStock(v.id, qty)
      const updated = variants.map(x =>
        x.id === v.id ? { ...x, inventory: { ...x.inventory, available_quantity: saved.new_stock } } : x)
      setVariants(updated)
      onProductUpdated({ ...product, variants: updated })
      cancelStockEdit(v.id)
      toast.success('Stock actualizado')
    } catch {
      toast.error('Error al actualizar el stock')
    } finally {
      setSavingStock(prev => ({ ...prev, [v.id]: false }))
    }
  }

  return (
    <>
      <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/60">
        <div className="bg-dark-800 border border-dark-600 rounded-2xl w-full max-w-3xl mx-4
                        shadow-2xl flex flex-col max-h-[90vh]">
          {/* Header */}
          <div className="flex items-center justify-between px-6 py-4 border-b border-dark-700 shrink-0">
            <div>
              <h3 className="text-gray-900 font-semibold">Variantes — {product.name}</h3>
              <p className="text-gray-500 text-xs mt-0.5">{variants.length} variante(s)</p>
            </div>
            <div className="flex items-center gap-3">
              <button onClick={openCreate}
                className="flex items-center gap-1.5 px-3 py-1.5 bg-brand-600 hover:bg-brand-500
                           text-white text-xs font-medium rounded-lg transition-colors">
                <PlusIcon className="w-3.5 h-3.5" /> Nueva variante
              </button>
              <button onClick={onClose}
                className="text-gray-400 hover:text-gray-800 text-xl leading-none">×</button>
            </div>
          </div>

          {/* Tabla */}
          <div className="overflow-y-auto flex-1">
            {variants.length === 0 ? (
              <div className="p-10 text-center text-gray-500">
                Sin variantes. Crea la primera.
              </div>
            ) : (
              <table className="w-full text-sm">
                <thead className="sticky top-0 bg-dark-800 z-10">
                  <tr className="border-b border-dark-600 text-gray-500 text-left">
                    <th className="px-5 py-3 font-medium">SKU</th>
                    <th className="px-5 py-3 font-medium">Talla</th>
                    <th className="px-5 py-3 font-medium">Color</th>
                    <th className="px-5 py-3 font-medium">Precio</th>
                    <th className="px-5 py-3 font-medium">Stock</th>
                    <th className="px-5 py-3 font-medium">Disp.</th>
                    <th className="px-5 py-3 font-medium text-center">Acciones</th>
                  </tr>
                </thead>
                <tbody>
                  {variants.map(v => (
                    <tr key={v.id}
                      className="border-b border-dark-700/60 hover:bg-dark-700/30 transition-colors">
                      <td className="px-5 py-3 text-gray-800 font-mono text-xs">{v.sku}</td>
                      <td className="px-5 py-3 text-gray-500">{v.size || '—'}</td>
                      <td className="px-5 py-3 text-gray-500">{v.color || '—'}</td>
                      <td className="px-5 py-3 text-gray-800">
                        ${Number(v.price).toLocaleString('es-CO')}
                      </td>
                      {/* Celda de stock con edición inline */}
                      <td className="px-5 py-3">
                        {stockEdit[v.id] !== undefined ? (
                          <div className="flex items-center gap-1">
                            <input type="number" min={0}
                              value={stockEdit[v.id]}
                              onChange={e => setStockEdit(p => ({ ...p, [v.id]: e.target.value }))}
                              className="w-20 bg-white border border-brand-500 rounded px-2 py-1
                                         text-xs text-gray-900 focus:outline-none" />
                            <button onClick={() => saveStock(v)} disabled={savingStock[v.id]}
                              className="text-emerald-400 hover:text-emerald-300 text-xs font-medium
                                         disabled:opacity-50">
                              {savingStock[v.id] ? '…' : 'OK'}
                            </button>
                            <button onClick={() => cancelStockEdit(v.id)}
                              className="text-gray-400 hover:text-gray-800 text-xs">✕</button>
                          </div>
                        ) : (
                          <button onClick={() => startStockEdit(v)}
                            className="flex items-center gap-1 text-gray-700 hover:text-brand-600
                                       transition-colors group">
                          <span>{v.inventory?.available_quantity ?? 0}</span>
                            <AdjustmentsHorizontalIcon
                              className="w-3.5 h-3.5 opacity-0 group-hover:opacity-100 transition-opacity" />
                          </button>
                        )}
                      </td>
                      <td className="px-5 py-3">
                        <span className={`text-xs font-medium px-2 py-0.5 rounded-full ${
                          v.is_available
                            ? 'bg-emerald-500/15 text-emerald-400'
                            : 'bg-red-500/15 text-red-400'}`}>
                          {v.is_available ? 'Sí' : 'No'}
                        </span>
                      </td>
                      <td className="px-5 py-3">
                        <div className="flex items-center justify-center gap-2">
                          <button onClick={() => openEdit(v)}
                            className="p-1.5 text-gray-400 hover:text-brand-600 hover:bg-brand-50
                                       rounded-lg transition-colors" title="Editar">
                            <PencilIcon className="w-4 h-4" />
                          </button>
                          <button onClick={() => handleDeleteVariant(v)}
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
            )}
          </div>
        </div>
      </div>

      <VariantModal
        open={varModal.open}
        onClose={closeVar}
        productId={product.id}
        initial={varModal.variant}
        onSaved={handleVarSaved}
      />
    </>
  )
}

// ─── Página principal ─────────────────────────────────────────────────────────

export default function AdminProductsPage() {
  const [products, setProducts]     = useState([])
  const [loading, setLoading]       = useState(true)
  const [search, setSearch]         = useState('')
  const [prodModal, setProdModal]   = useState({ open: false, product: null })
  const [varDialog, setVarDialog]   = useState({ open: false, product: null })

  const normalizeProducts = (list) =>
    (Array.isArray(list) ? list : []).map(p => ({
      ...p,
      variants: (p.variants || []).map(v => ({
        ...v,
        inventory: v.inventory ?? {
          available_quantity: v.available_quantity ?? 0,
        },
      })),
    }))

  const load = () => {
    setLoading(true)
    getProducts()
      .then(data => setProducts(normalizeProducts(data)))
      .finally(() => setLoading(false))
  }

  useEffect(load, [])

  const openCreate     = () => setProdModal({ open: true, product: null })
  const openEditProd   = (p) => setProdModal({ open: true, product: p })
  const closeProdModal = () => setProdModal({ open: false, product: null })
  const openVariants   = (p) => setVarDialog({ open: true, product: p })
  const closeVariants  = () => setVarDialog({ open: false, product: null })

  const handleProductSaved = (saved, isEdit) => {
    setProducts(prev =>
      isEdit ? prev.map(p => p.id === saved.id ? { ...prev.find(x => x.id === saved.id), ...saved } : p)
             : [saved, ...prev])
  }

  const handleProductUpdated = (updated) => {
    setProducts(prev => prev.map(p => p.id === updated.id ? updated : p))
    if (varDialog.product?.id === updated.id)
      setVarDialog(prev => ({ ...prev, product: updated }))
  }

  const handleDelete = async (p) => {
    if (!confirm(`¿Eliminar "${p.name}"? Se eliminarán todas sus variantes.`)) return
    try {
      await deleteProduct(p.id)
      setProducts(prev => prev.filter(x => x.id !== p.id))
      toast.success('Producto eliminado')
    } catch (err) {
      const status = err.response?.status
      toast.error(status === 409
        ? 'No se puede eliminar: tiene órdenes asociadas'
        : 'Error al eliminar el producto')
    }
  }

  const filtered = products.filter(p => {
    const q = search.toLowerCase()
    return p.name?.toLowerCase().includes(q) || p.category?.toLowerCase().includes(q)
  })

  return (
    <div className="p-8">
      {/* Cabecera */}
      <div className="flex items-center justify-between mb-6">
        <div>
          <h2 className="text-2xl font-bold text-gray-900 mb-1">Productos</h2>
          <p className="text-gray-500 text-sm">{products.length} productos en catálogo</p>
        </div>
        <button onClick={openCreate}
          className="flex items-center gap-2 px-4 py-2 bg-brand-600 hover:bg-brand-500
                     text-white text-sm font-medium rounded-lg transition-colors">
          <PlusIcon className="w-4 h-4" /> Nuevo producto
        </button>
      </div>

      {/* Búsqueda */}
      <div className="mb-5">
        <input type="text" placeholder="Buscar por nombre o categoría…"
          value={search} onChange={e => setSearch(e.target.value)}
          className="w-full max-w-sm bg-white border border-dark-600 text-gray-900
                     placeholder-gray-400 rounded-lg px-4 py-2 text-sm
                     focus:outline-none focus:ring-1 focus:ring-brand-500" />
      </div>

      {/* Tabla */}
      {loading ? (
        <p className="text-gray-500">Cargando...</p>
      ) : filtered.length === 0 ? (
        <div className="bg-dark-800 rounded-xl border border-dark-600 p-10 text-center text-gray-500">
          {search ? 'Sin resultados.' : 'No hay productos. ¡Crea el primero!'}
        </div>
      ) : (
        <div className="bg-dark-800 rounded-xl border border-dark-700 overflow-hidden">
          <table className="w-full text-sm">
            <thead>
              <tr className="border-b border-dark-600 text-gray-500 text-left">
                <th className="px-5 py-3 font-medium">#</th>
                <th className="px-5 py-3 font-medium">Nombre</th>
                <th className="px-5 py-3 font-medium">Categoría</th>
                <th className="px-5 py-3 font-medium">Variantes</th>
                <th className="px-5 py-3 font-medium">Estado</th>
                <th className="px-5 py-3 font-medium text-center">Acciones</th>
              </tr>
            </thead>
            <tbody>
              {filtered.map(p => (
                <tr key={p.id}
                  className="border-b border-dark-700/60 hover:bg-dark-700/40 transition-colors">
                  <td className="px-5 py-3 text-gray-400 font-mono text-xs">{p.id}</td>
                  <td className="px-5 py-3 text-gray-800 font-medium">{p.name}</td>
                  <td className="px-5 py-3 text-gray-500">{p.category || '—'}</td>
                  <td className="px-5 py-3">
                    <button onClick={() => openVariants(p)}
                      className="flex items-center gap-1.5 text-brand-400 hover:text-brand-300
                                 text-xs font-medium transition-colors">
                      <CubeIcon className="w-3.5 h-3.5" />
                      {(p.variants?.length ?? 0)} variante(s)
                    </button>
                  </td>
                  <td className="px-5 py-3">
                    <span className={`text-xs font-medium px-2.5 py-1 rounded-full ${
                      p.is_active
                        ? 'bg-emerald-500/15 text-emerald-400'
                        : 'bg-gray-100 text-gray-500'}`}>
                      {p.is_active ? 'Activo' : 'Inactivo'}
                    </span>
                  </td>
                  <td className="px-5 py-3">
                    <div className="flex items-center justify-center gap-2">
                      <button onClick={() => openEditProd(p)}
                        className="p-1.5 text-gray-400 hover:text-brand-600 hover:bg-brand-50
                                   rounded-lg transition-colors" title="Editar">
                        <PencilIcon className="w-4 h-4" />
                      </button>
                      <button onClick={() => handleDelete(p)}
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

      {/* Modales */}
      <ProductModal
        open={prodModal.open}
        initial={prodModal.product}
        onClose={closeProdModal}
        onSaved={handleProductSaved}
      />

      <VariantsModal
        open={varDialog.open}
        product={varDialog.product}
        onClose={closeVariants}
        onProductUpdated={handleProductUpdated}
      />
    </div>
  )
}

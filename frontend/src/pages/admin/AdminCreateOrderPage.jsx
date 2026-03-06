import { useState } from 'react'
import { useNavigate, Link } from 'react-router-dom'
import { PlusIcon, TrashIcon } from '@heroicons/react/24/outline'
import toast from 'react-hot-toast'
import { createAdminOrder } from '../../api/admin'

const EMPTY_CUSTOMER = { nombre: '', apellido: '', email: '', telefono: '', direccion: '' }
const EMPTY_ITEM     = { product_name: '', quantity: 1, price: '' }

export default function AdminCreateOrderPage() {
  const navigate = useNavigate()

  const [customer, setCustomer]       = useState(EMPTY_CUSTOMER)
  const [items, setItems]             = useState([{ ...EMPTY_ITEM }])
  const [shippingAddress, setShipping] = useState('')
  const [discountCode, setDiscount]   = useState('')
  const [saving, setSaving]           = useState(false)
  const [errors, setErrors]           = useState({})

  // ─── Customer ────────────────────────────────────────────────────────────────
  const changeCustomer = (e) =>
    setCustomer(p => ({ ...p, [e.target.name]: e.target.value }))

  // ─── Items ───────────────────────────────────────────────────────────────────
  const changeItem = (i, field, value) =>
    setItems(prev => prev.map((it, idx) => idx === i ? { ...it, [field]: value } : it))

  const addItem = () => setItems(p => [...p, { ...EMPTY_ITEM }])

  const removeItem = (i) => setItems(p => p.filter((_, idx) => idx !== i))

  // ─── Totales (preview) ───────────────────────────────────────────────────────
  const subtotal = items.reduce((sum, it) => {
    const qty   = Number(it.quantity) || 0
    const price = parseFloat(it.price) || 0
    return sum + qty * price
  }, 0)
  const hasDiscount  = discountCode.trim().length > 0
  const discountAmt  = hasDiscount ? subtotal * 0.10 : 0
  const total        = subtotal - discountAmt

  // ─── Submit ──────────────────────────────────────────────────────────────────
  const validate = () => {
    const e = {}
    if (!customer.nombre.trim())    e['customer.nombre']   = 'Requerido'
    if (!customer.apellido.trim())  e['customer.apellido'] = 'Requerido'
    if (!customer.email.trim())     e['customer.email']    = 'Requerido'
    if (!shippingAddress.trim())    e.shipping_address     = 'Requerido'
    items.forEach((it, i) => {
      if (!it.product_name.trim())  e[`items[${i}].product_name`] = 'Requerido'
      if (!it.price || Number(it.price) <= 0) e[`items[${i}].price`] = 'Precio inválido'
    })
    return e
  }

  const submit = async (e) => {
    e.preventDefault()
    const errs = validate()
    if (Object.keys(errs).length) { setErrors(errs); return }

    setSaving(true)
    try {
      const payload = {
        customer,
        items: items.map(it => ({
          product_name: it.product_name,
          quantity:     Number(it.quantity),
          price:        parseFloat(it.price),
        })),
        shipping_address: shippingAddress,
        discount_code:    discountCode || null,
      }
      const created = await createAdminOrder(payload)
      toast.success(`Orden #${created.id} creada`)
      navigate(`/admin/orders/${created.id}`)
    } catch (err) {
      const data = err.response?.data
      if (data?.errors && typeof data.errors === 'object') setErrors(data.errors)
      else toast.error(data?.message || 'Error al crear la orden')
    } finally {
      setSaving(false)
    }
  }

  const fieldErr = (key) => errors[key] && (
    <p className="text-red-400 text-xs mt-1">
      {Array.isArray(errors[key]) ? errors[key][0] : errors[key]}
    </p>
  )

  return (
    <div className="p-8 max-w-3xl">
      {/* Encabezado */}
      <div className="flex items-center gap-3 mb-6">
        <Link to="/admin/orders" className="text-gray-500 hover:text-gray-800 text-sm transition-colors">
          ← Órdenes
        </Link>
        <span className="text-gray-400">/</span>
        <h2 className="text-2xl font-bold text-gray-900">Nueva orden</h2>
      </div>

      <form onSubmit={submit} className="space-y-6">

        {/* Datos del cliente */}
        <section className="bg-dark-800 rounded-xl border border-dark-700 p-6">
          <h3 className="text-gray-800 font-semibold mb-4">Datos del cliente</h3>
          <p className="text-gray-400 text-xs mb-4">
            Si el email ya existe en el sistema, la orden se asociará al cliente existente.
          </p>
          <div className="grid grid-cols-2 gap-4">
            {[
              { name: 'nombre',    label: 'Nombre',    col: 1 },
              { name: 'apellido',  label: 'Apellido',  col: 1 },
              { name: 'email',     label: 'Email',     col: 2 },
              { name: 'telefono',  label: 'Teléfono',  col: 1 },
              { name: 'direccion', label: 'Dirección', col: 2 },
            ].map(({ name, label, col }) => (
              <div key={name} className={col === 2 ? 'col-span-2' : ''}>
                <label className="block text-xs text-gray-600 mb-1">{label}</label>
                <input
                  name={name}
                  value={customer[name]}
                  onChange={changeCustomer}
                  className={`w-full bg-white border rounded-lg px-3 py-2 text-sm text-gray-900
                    placeholder-gray-400 focus:outline-none focus:ring-1 focus:ring-brand-500 transition
                    ${errors[`customer.${name}`] ? 'border-red-500' : 'border-dark-600'}`}
                />
                {fieldErr(`customer.${name}`)}
              </div>
            ))}
          </div>
        </section>

        {/* Productos */}
        <section className="bg-dark-800 rounded-xl border border-dark-700 p-6">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-gray-800 font-semibold">Productos</h3>
            <button type="button" onClick={addItem}
              className="flex items-center gap-1.5 text-xs text-brand-400 hover:text-brand-300 transition-colors">
              <PlusIcon className="w-3.5 h-3.5" /> Agregar ítem
            </button>
          </div>

          <div className="space-y-3">
            {items.map((it, i) => (
              <div key={i} className="grid grid-cols-12 gap-3 items-start">
                {/* Producto */}
                <div className="col-span-5">
                  {i === 0 && <label className="block text-xs text-gray-600 mb-1">Producto</label>}
                  <input
                    value={it.product_name}
                    onChange={e => changeItem(i, 'product_name', e.target.value)}
                    placeholder="Nombre del producto"
                    className={`w-full bg-white border rounded-lg px-3 py-2 text-sm text-gray-900
                      placeholder-gray-400 focus:outline-none focus:ring-1 focus:ring-brand-500
                      ${errors[`items[${i}].product_name`] ? 'border-red-500' : 'border-dark-600'}`}
                  />
                  {fieldErr(`items[${i}].product_name`)}
                </div>
                {/* Cantidad */}
                <div className="col-span-2">
                  {i === 0 && <label className="block text-xs text-gray-600 mb-1">Cant.</label>}
                  <input
                    type="number" min="1"
                    value={it.quantity}
                    onChange={e => changeItem(i, 'quantity', e.target.value)}
                    className="w-full bg-white border border-dark-600 rounded-lg px-3 py-2
                               text-sm text-gray-900 focus:outline-none focus:ring-1 focus:ring-brand-500"
                  />
                </div>
                {/* Precio */}
                <div className="col-span-3">
                  {i === 0 && <label className="block text-xs text-gray-600 mb-1">Precio unit.</label>}
                  <input
                    type="number" min="0" step="0.01"
                    value={it.price}
                    onChange={e => changeItem(i, 'price', e.target.value)}
                    placeholder="0.00"
                    className={`w-full bg-white border rounded-lg px-3 py-2 text-sm text-gray-900
                      placeholder-gray-400 focus:outline-none focus:ring-1 focus:ring-brand-500
                      ${errors[`items[${i}].price`] ? 'border-red-500' : 'border-dark-600'}`}
                  />
                  {fieldErr(`items[${i}].price`)}
                </div>
                {/* Subtotal + eliminar */}
                <div className="col-span-2 flex items-end gap-1 pb-0.5">
                  {i === 0 && <div className="h-[21px]" />}
                  <span className="flex-1 text-right text-sm text-gray-700 pb-2">
                    ${((Number(it.quantity) || 0) * (parseFloat(it.price) || 0)).toLocaleString('es-CO')}
                  </span>
                  {items.length > 1 && (
                    <button type="button" onClick={() => removeItem(i)}
                      className="p-1.5 text-gray-400 hover:text-red-500 hover:bg-red-50
                                 rounded-lg transition-colors mb-1">
                      <TrashIcon className="w-4 h-4" />
                    </button>
                  )}
                </div>
              </div>
            ))}
          </div>
        </section>

        {/* Envío y descuento */}
        <section className="bg-dark-800 rounded-xl border border-dark-700 p-6">
          <h3 className="text-gray-800 font-semibold mb-4">Envío y descuento</h3>
          <div className="grid grid-cols-2 gap-4">
            <div className="col-span-2">
              <label className="block text-xs text-gray-600 mb-1">Dirección de envío</label>
              <input
                value={shippingAddress}
                onChange={e => setShipping(e.target.value)}
                placeholder="Calle, ciudad, departamento…"
                className={`w-full bg-white border rounded-lg px-3 py-2 text-sm text-gray-900
                  placeholder-gray-400 focus:outline-none focus:ring-1 focus:ring-brand-500
                  ${errors.shipping_address ? 'border-red-500' : 'border-dark-600'}`}
              />
              {fieldErr('shipping_address')}
            </div>
            <div>
              <label className="block text-xs text-gray-600 mb-1">
                Código de descuento <span className="text-gray-400">(10% si aplica)</span>
              </label>
              <input
                value={discountCode}
                onChange={e => setDiscount(e.target.value)}
                placeholder="SAVE10"
                className="w-full bg-white border border-dark-600 rounded-lg px-3 py-2
                           text-sm text-gray-900 placeholder-gray-400
                           focus:outline-none focus:ring-1 focus:ring-brand-500"
              />
            </div>
          </div>
        </section>

        {/* Resumen de totales */}
        <div className="bg-dark-800 rounded-xl border border-dark-700 p-5 space-y-2">
          <div className="flex justify-between text-sm text-gray-500">
            <span>Subtotal</span>
            <span>${subtotal.toLocaleString('es-CO')}</span>
          </div>
          {hasDiscount && (
            <div className="flex justify-between text-sm text-emerald-400">
              <span>Descuento ({discountCode})</span>
              <span>−${discountAmt.toLocaleString('es-CO')}</span>
            </div>
          )}
          <div className="flex justify-between text-base font-bold text-gray-900
                          pt-2 border-t border-dark-600">
            <span>Total estimado</span>
            <span>${total.toLocaleString('es-CO')}</span>
          </div>
        </div>

        {/* Botones */}
        <div className="flex justify-end gap-3">
          <Link to="/admin/orders"
            className="px-4 py-2 text-sm text-gray-500 hover:text-gray-800 transition-colors">
            Cancelar
          </Link>
          <button type="submit" disabled={saving}
            className="px-6 py-2 bg-brand-600 hover:bg-brand-500 disabled:opacity-50
                       text-white text-sm font-medium rounded-lg transition-colors">
            {saving ? 'Creando…' : 'Crear orden'}
          </button>
        </div>
      </form>
    </div>
  )
}

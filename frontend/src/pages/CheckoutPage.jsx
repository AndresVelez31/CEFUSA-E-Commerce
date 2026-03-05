import { useState } from 'react'
import { useNavigate, Link } from 'react-router-dom'
import { ArrowLeftIcon, LockClosedIcon } from '@heroicons/react/24/outline'
import toast from 'react-hot-toast'
import { checkout } from '../api/orders'
import { useCart } from '../context/CartContext'

const INITIAL_FORM = {
  nombre: '', apellido: '', email: '', telefono: '', direccion: '',
  shipping_address: '', discount_code: '',
}

export default function CheckoutPage() {
  const navigate = useNavigate()
  const { items, subtotal, clearCart } = useCart()
  const [form, setForm]         = useState(INITIAL_FORM)
  const [loading, setLoading]   = useState(false)
  const [errors, setErrors]     = useState({})

  if (items.length === 0) {
    return (
      <div className="max-w-lg mx-auto px-4 py-20 text-center">
        <p className="text-5xl mb-4">🛒</p>
        <p className="text-slate-300 text-lg font-medium">Carrito vacío</p>
        <Link to="/" className="btn-primary mt-4 inline-block">Ir al catálogo</Link>
      </div>
    )
  }

  const handleChange = (e) => {
    setForm(f => ({ ...f, [e.target.name]: e.target.value }))
    setErrors(err => ({ ...err, [e.target.name]: undefined }))
  }

  const validate = () => {
    const e = {}
    if (!form.nombre.trim())       e.nombre           = 'Nombre requerido'
    if (!form.apellido.trim())     e.apellido         = 'Apellido requerido'
    if (!form.email.includes('@')) e.email            = 'Email inválido'
    if (!form.telefono.trim())     e.telefono         = 'Teléfono requerido'
    if (!form.shipping_address.trim()) e.shipping_address = 'Dirección de envío requerida'
    return e
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    const errs = validate()
    if (Object.keys(errs).length > 0) { setErrors(errs); return }

    setLoading(true)
    try {
      const result = await checkout({
        customer: {
          nombre:    form.nombre,
          apellido:  form.apellido,
          email:     form.email,
          telefono:  form.telefono,
          direccion: form.direccion,
        },
        items: items.map(i => ({ variant_id: i.variant_id, quantity: i.quantity })),
        shipping_address: form.shipping_address,
        discount_code: form.discount_code || undefined,
      })

      clearCart()
      toast.success('¡Orden creada exitosamente!')
      navigate(`/order/${result.order_id}`, { state: result })
    } catch (err) {
      const status = err.response?.status
      if (status === 409) toast.error('Stock insuficiente para uno o más productos')
      else if (status === 400) toast.error('Verifica los datos del formulario')
      else toast.error(err.friendlyMessage || 'Error al procesar la orden')
    } finally {
      setLoading(false)
    }
  }

  const Field = ({ name, label, type = 'text', span = false }) => (
    <div className={span ? 'sm:col-span-2' : ''}>
      <label className="label">{label}</label>
      <input
        type={type}
        name={name}
        value={form[name]}
        onChange={handleChange}
        className={`input-field ${errors[name] ? 'border-red-500 focus:ring-red-500' : ''}`}
      />
      {errors[name] && <p className="text-red-400 text-xs mt-1">{errors[name]}</p>}
    </div>
  )

  return (
    <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-10">
      <Link to="/cart" className="inline-flex items-center gap-2 text-slate-400 hover:text-brand-400 text-sm mb-8 transition-colors">
        <ArrowLeftIcon className="w-4 h-4" />
        Volver al carrito
      </Link>

      <h1 className="section-title mb-8">Finalizar compra</h1>

      <form onSubmit={handleSubmit}>
        <div className="grid lg:grid-cols-3 gap-8 items-start">
          {/* Form */}
          <div className="lg:col-span-2 space-y-6">
            {/* Customer data */}
            <div className="card p-6">
              <h2 className="font-bold text-slate-200 mb-5 flex items-center gap-2">
                <span className="w-6 h-6 bg-brand-600 rounded-full text-xs flex items-center justify-center text-white font-bold">1</span>
                Datos personales
              </h2>
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <Field name="nombre"   label="Nombre" />
                <Field name="apellido" label="Apellido" />
                <Field name="email"    label="Correo electrónico" type="email" />
                <Field name="telefono" label="Teléfono" />
                <Field name="direccion" label="Dirección personal (opcional)" span />
              </div>
            </div>

            {/* Shipping */}
            <div className="card p-6">
              <h2 className="font-bold text-slate-200 mb-5 flex items-center gap-2">
                <span className="w-6 h-6 bg-brand-600 rounded-full text-xs flex items-center justify-center text-white font-bold">2</span>
                Dirección de envío
              </h2>
              <Field name="shipping_address" label="Dirección completa de entrega" span />
            </div>

            {/* Discount */}
            <div className="card p-6">
              <h2 className="font-bold text-slate-200 mb-5 flex items-center gap-2">
                <span className="w-6 h-6 bg-dark-600 rounded-full text-xs flex items-center justify-center text-slate-300 font-bold">3</span>
                Código de descuento
                <span className="text-xs text-slate-500 font-normal">(opcional)</span>
              </h2>
              <div className="flex gap-3">
                <input
                  type="text"
                  name="discount_code"
                  placeholder="Ej: SAVE10, VIP20"
                  value={form.discount_code}
                  onChange={handleChange}
                  className="input-field uppercase placeholder-normal"
                />
              </div>
              <p className="text-xs text-slate-500 mt-2">Prueba: SAVE10 (10%) · VIP20 (20%)</p>
            </div>
          </div>

          {/* Order summary */}
          <div className="card p-6 space-y-4 sticky top-24">
            <h2 className="font-bold text-lg text-white">Tu pedido</h2>

            <div className="space-y-2 max-h-48 overflow-y-auto pr-1">
              {items.map(i => (
                <div key={i.variant_id} className="flex justify-between text-sm gap-2">
                  <span className="text-slate-400 truncate">
                    {i.product_name} ×{i.quantity}
                  </span>
                  <span className="text-slate-300 flex-shrink-0">
                    ${(parseFloat(i.price) * i.quantity).toFixed(2)}
                  </span>
                </div>
              ))}
            </div>

            <div className="border-t border-dark-600 pt-3">
              <div className="flex justify-between font-bold text-white">
                <span>Subtotal</span>
                <span className="text-brand-400">${subtotal.toFixed(2)}</span>
              </div>
              <p className="text-xs text-slate-500 mt-1">
                El descuento se aplica al confirmar
              </p>
            </div>

            <button
              type="submit"
              disabled={loading}
              className="btn-primary w-full flex items-center justify-center gap-2 py-3"
            >
              <LockClosedIcon className="w-4 h-4" />
              {loading ? 'Procesando...' : 'Confirmar orden'}
            </button>
          </div>
        </div>
      </form>
    </div>
  )
}

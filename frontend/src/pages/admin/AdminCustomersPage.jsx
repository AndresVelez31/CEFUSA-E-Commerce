import { useEffect, useState, useRef } from 'react'
import { Link } from 'react-router-dom'
import { PlusIcon, PencilIcon, TrashIcon } from '@heroicons/react/24/outline'
import toast from 'react-hot-toast'
import {
  getAdminCustomers,
  createAdminCustomer,
  updateAdminCustomer,
  deleteAdminCustomer,
} from '../../api/admin'

const EMPTY_FORM = { nombre: '', apellido: '', email: '', telefono: '', direccion: '' }

function CustomerModal({ open, onClose, initial, onSaved }) {
  const [form, setForm]     = useState(EMPTY_FORM)
  const [errors, setErrors] = useState({})
  const [saving, setSaving] = useState(false)
  const firstRef = useRef(null)
  const isEdit = Boolean(initial)

  useEffect(() => {
    if (open) {
      setForm(initial ? { ...initial } : EMPTY_FORM)
      setErrors({})
      setTimeout(() => firstRef.current?.focus(), 50)
    }
  }, [open, initial])

  if (!open) return null

  const change = (e) => setForm(p => ({ ...p, [e.target.name]: e.target.value }))

  const validate = () => {
    const e = {}
    if (!form.nombre.trim())   e.nombre   = 'Requerido'
    if (!form.apellido.trim()) e.apellido = 'Requerido'
    if (!form.email.trim())    e.email    = 'Requerido'
    return e
  }

  const submit = async (ev) => {
    ev.preventDefault()
    const e = validate()
    if (Object.keys(e).length) { setErrors(e); return }
    setSaving(true)
    try {
      const saved = isEdit
        ? await updateAdminCustomer(initial.id, form)
        : await createAdminCustomer(form)
      onSaved(saved, isEdit)
      toast.success(isEdit ? 'Cliente actualizado' : 'Cliente creado')
      onClose()
    } catch (err) {
      const data = err.response?.data
      if (data && typeof data === 'object') setErrors(data)
      else toast.error('Error al guardar')
    } finally {
      setSaving(false)
    }
  }

  const FIELDS = [
    { name: 'nombre',    label: 'Nombre',    type: 'text',  full: false },
    { name: 'apellido',  label: 'Apellido',  type: 'text',  full: false },
    { name: 'email',     label: 'Email',     type: 'email', full: true  },
    { name: 'telefono',  label: 'Teléfono',  type: 'text',  full: false },
    { name: 'direccion', label: 'Dirección', type: 'text',  full: true  },
  ]

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/60">
      <div className="bg-dark-800 border border-dark-600 rounded-2xl w-full max-w-lg mx-4 shadow-2xl">
        <div className="flex items-center justify-between px-6 py-4 border-b border-dark-700">
          <h3 className="text-gray-900 font-semibold">
            {isEdit ? 'Editar cliente' : 'Nuevo cliente'}
          </h3>
          <button onClick={onClose} className="text-gray-400 hover:text-gray-800 text-xl leading-none">×</button>
        </div>
        <form onSubmit={submit} className="p-6">
          <div className="grid grid-cols-2 gap-4">
            {FIELDS.map(({ name, label, type, full }, i) => (
              <div key={name} className={full ? 'col-span-2' : ''}>
                <label className="block text-xs text-gray-600 mb-1">{label}</label>
                <input
                  ref={i === 0 ? firstRef : undefined}
                  type={type} name={name} value={form[name]} onChange={change}
                  className={`w-full bg-white border rounded-lg px-3 py-2 text-sm text-gray-900
                    placeholder-gray-400 focus:outline-none focus:ring-1 focus:ring-brand-500 transition
                    ${errors[name] ? 'border-red-500' : 'border-dark-600'}`}
                />
                {errors[name] && (
                  <p className="text-red-400 text-xs mt-1">
                    {Array.isArray(errors[name]) ? errors[name][0] : errors[name]}
                  </p>
                )}
              </div>
            ))}
          </div>
          <div className="flex justify-end gap-3 mt-6">
            <button type="button" onClick={onClose}
              className="px-4 py-2 text-sm text-gray-500 hover:text-gray-800 transition-colors">
              Cancelar
            </button>
            <button type="submit" disabled={saving}
              className="px-5 py-2 bg-brand-600 hover:bg-brand-500 disabled:opacity-50 text-white
                         text-sm font-medium rounded-lg transition-colors">
              {saving ? 'Guardando…' : isEdit ? 'Guardar cambios' : 'Crear cliente'}
            </button>
          </div>
        </form>
      </div>
    </div>
  )
}

export default function AdminCustomersPage() {
  const [customers, setCustomers] = useState([])
  const [loading, setLoading]     = useState(true)
  const [search, setSearch]       = useState('')
  const [modal, setModal]         = useState({ open: false, customer: null })

  const load = () => {
    setLoading(true)
    getAdminCustomers().then(setCustomers).finally(() => setLoading(false))
  }

  useEffect(load, [])

  const openCreate = () => setModal({ open: true, customer: null })
  const openEdit   = (c) => setModal({ open: true, customer: c })
  const closeModal = () => setModal({ open: false, customer: null })

  const handleSaved = (saved, isEdit) => {
    setCustomers(prev =>
      isEdit ? prev.map(c => c.id === saved.id ? saved : c) : [saved, ...prev]
    )
  }

  const handleDelete = async (id, name) => {
    if (!confirm(`¿Eliminar a ${name}? Esta acción no se puede deshacer.`)) return
    try {
      await deleteAdminCustomer(id)
      setCustomers(prev => prev.filter(c => c.id !== id))
      toast.success('Cliente eliminado')
    } catch {
      toast.error('Error al eliminar')
    }
  }

  const filtered = customers.filter(c => {
    const q = search.toLowerCase()
    return c.nombre_completo?.toLowerCase().includes(q) || c.email?.toLowerCase().includes(q)
  })

  return (
    <div className="p-8">
      <div className="flex items-center justify-between mb-6">
        <div>
          <h2 className="text-2xl font-bold text-gray-900 mb-1">Clientes</h2>
          <p className="text-gray-500 text-sm">{customers.length} clientes registrados</p>
        </div>
        <button onClick={openCreate}
          className="flex items-center gap-2 px-4 py-2 bg-brand-600 hover:bg-brand-500
                     text-white text-sm font-medium rounded-lg transition-colors">
          <PlusIcon className="w-4 h-4" /> Nuevo cliente
        </button>
      </div>

      <div className="mb-5">
        <input type="text" placeholder="Buscar por nombre o email…" value={search}
          onChange={e => setSearch(e.target.value)}
          className="w-full max-w-sm bg-white border border-dark-600 text-gray-900
                     placeholder-gray-400 rounded-lg px-4 py-2 text-sm
                     focus:outline-none focus:ring-1 focus:ring-brand-500" />
      </div>

      {loading ? (
        <p className="text-gray-500">Cargando...</p>
      ) : filtered.length === 0 ? (
        <div className="bg-dark-800 rounded-xl border border-dark-600 p-10 text-center text-gray-500">
          {search ? 'Sin resultados.' : 'No hay clientes. ¡Crea el primero!'}
        </div>
      ) : (
        <div className="bg-dark-800 rounded-xl border border-dark-700 overflow-hidden">
          <table className="w-full text-sm">
            <thead>
              <tr className="border-b border-dark-600 text-gray-500 text-left">
                <th className="px-5 py-3 font-medium">Nombre</th>
                <th className="px-5 py-3 font-medium">Email</th>
                <th className="px-5 py-3 font-medium">Teléfono</th>
                <th className="px-5 py-3 font-medium">Dirección</th>
                <th className="px-5 py-3 font-medium">Registrado</th>
                <th className="px-5 py-3 font-medium text-center">Acciones</th>
              </tr>
            </thead>
            <tbody>
              {filtered.map(c => (
                <tr key={c.id}
                  className="border-b border-dark-700/60 hover:bg-dark-700/40 transition-colors">
                  <td className="px-5 py-3 text-gray-800 font-medium">{c.nombre_completo}</td>
                  <td className="px-5 py-3 text-gray-500">{c.email}</td>
                  <td className="px-5 py-3 text-gray-500">{c.telefono || '—'}</td>
                  <td className="px-5 py-3 text-gray-500 max-w-xs truncate">{c.direccion || '—'}</td>
                  <td className="px-5 py-3 text-gray-400">
                    {new Date(c.created_at).toLocaleDateString('es-CO')}
                  </td>
                  <td className="px-5 py-3">
                    <div className="flex items-center justify-center gap-2">
                      <button onClick={() => openEdit(c)}
                        className="p-1.5 text-gray-400 hover:text-brand-600 hover:bg-brand-50
                                   rounded-lg transition-colors" title="Editar">
                        <PencilIcon className="w-4 h-4" />
                      </button>
                      <button onClick={() => handleDelete(c.id, c.nombre_completo)}
                        className="p-1.5 text-gray-400 hover:text-red-500 hover:bg-red-50
                                   rounded-lg transition-colors" title="Eliminar">
                        <TrashIcon className="w-4 h-4" />
                      </button>
                      <Link to={`/admin/orders`}
                        className="text-brand-400 hover:text-brand-300 text-xs font-medium transition-colors">
                        Órdenes →
                      </Link>
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      <CustomerModal
        open={modal.open}
        initial={modal.customer}
        onClose={closeModal}
        onSaved={handleSaved}
      />
    </div>
  )
}

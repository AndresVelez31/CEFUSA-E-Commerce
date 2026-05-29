import api from './axios'

// ─── Dashboard ────────────────────────────────────────────────────────────────
export const getDashboard = () =>
  api.get('/admin/dashboard/').then(r => r.data)

// ─── Órdenes ──────────────────────────────────────────────────────────────────
export const getAdminOrders = (statusFilter = '') =>
  api.get(`/admin/orders/${statusFilter ? `?status=${statusFilter}` : ''}`).then(r => r.data)

export const getAdminOrder = (id) =>
  api.get(`/admin/orders/${id}/`).then(r => r.data)

export const createAdminOrder = (data) =>
  api.post('/admin/orders/', data).then(r => r.data)

export const updateOrderStatus = (id, newStatus) =>
  api.patch(`/admin/orders/${id}/status/`, { status: newStatus }).then(r => r.data)

export const deleteAdminOrder = (id) =>
  api.delete(`/admin/orders/${id}/delete/`).then(r => r.data)

// ─── Clientes ───────────────────────────────────────────────────────
// Rutas v2 — ms-customers (Strangler Pattern)
export const getAdminCustomers = () =>
  api.get('/v2/customers/').then(r => r.data)

export const createAdminCustomer = (data) =>
  api.post('/v2/customers/', data).then(r => r.data.customer ?? r.data)

export const updateAdminCustomer = (id, data) =>
  api.put(`/v2/customers/${id}/`, data).then(r => r.data.customer ?? r.data)

export const deleteAdminCustomer = (id) =>
  api.delete(`/v2/customers/${id}/`).then(r => r.data)

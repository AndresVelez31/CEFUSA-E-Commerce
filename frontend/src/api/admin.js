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

// ─── Clientes ─────────────────────────────────────────────────────────────────
export const getAdminCustomers = () =>
  api.get('/admin/customers/').then(r => r.data)

export const createAdminCustomer = (data) =>
  api.post('/admin/customers/', data).then(r => r.data)

export const updateAdminCustomer = (id, data) =>
  api.put(`/admin/customers/${id}/`, data).then(r => r.data)

export const deleteAdminCustomer = (id) =>
  api.delete(`/admin/customers/${id}/`).then(r => r.data)

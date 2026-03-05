import api from './axios'

/** Crear o actualizar cliente */
export const createCustomer = (data) =>
  api.post('/customers/', data).then(r => r.data)

/** Obtener historial de órdenes de un cliente */
export const getCustomerOrders = (customerId) =>
  api.get(`/customers/${customerId}/orders/`).then(r => r.data)

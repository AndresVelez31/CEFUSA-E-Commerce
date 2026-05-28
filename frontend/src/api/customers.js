import api from './axios'

/**
 * Crear cliente — usa ms-customers v2 (Strangler Pattern)
 * POST /api/v2/customers/
 */
export const createCustomer = (data) =>
  api.post('/v2/customers/', data).then(r => r.data)

/**
 * Obtener historial de órdenes de un cliente
 * Se mantiene en Django legacy (ms-customers no gestiona orders)
 * GET /api/customers/{id}/orders/
 */
export const getCustomerOrders = (customerId) =>
  api.get(`/customers/${customerId}/orders/`).then(r => r.data)

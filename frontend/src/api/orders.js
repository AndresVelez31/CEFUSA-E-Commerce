import api from './axios'

/**
 * Enviar el pedido completo (checkout).
 * Payload esperado:
 * {
 *   customer: { nombre, apellido, email, telefono, direccion },
 *   items: [{ variant_id, quantity }],
 *   shipping_address: string,
 *   discount_code?: string
 * }
 */
export const checkout = (data) =>
  api.post('/orders/checkout/', data).then(r => r.data)

/** Detalle de una orden por ID */
export const getOrder = (id) =>
  api.get(`/orders/${id}/`).then(r => r.data)

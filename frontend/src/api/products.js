import api from './axios'

/** Lista todos los productos (con variantes e inventario) */
export const getProducts = (params = {}) =>
  api.get('/products/', { params }).then(r => r.data)

/** Detalle de un producto por ID */
export const getProduct = (id) =>
  api.get(`/products/${id}/`).then(r => r.data)

/** Verificar disponibilidad de stock para una variante */
export const checkStock = (variantId, quantity) =>
  api.post('/products/check-stock/', { variant_id: variantId, quantity }).then(r => r.data)

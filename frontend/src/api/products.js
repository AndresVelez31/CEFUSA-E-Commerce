import api from './axios'

// ── Productos ──────────────────────────────────────────────────────────────

/** Lista todos los productos (con variantes e inventario) */
export const getProducts = (params = {}) =>
  api.get('/products/', { params }).then(r => r.data)

/** Detalle de un producto por ID */
export const getProduct = (id) =>
  api.get(`/products/${id}/`).then(r => r.data)

/** Crear un nuevo producto */
export const createProduct = (data) =>
  api.post('/products/', data).then(r => r.data)

/** Actualizar un producto (PATCH — campos parciales) */
export const updateProduct = (id, data) =>
  api.patch(`/products/${id}/`, data).then(r => r.data)

/** Eliminar un producto */
export const deleteProduct = (id) =>
  api.delete(`/products/${id}/`).then(r => r.data)

// ── Variantes ──────────────────────────────────────────────────────────────

/** Lista las variantes de un producto */
export const getVariants = (productId) =>
  api.get(`/products/${productId}/variants/`).then(r => r.data)

/** Agregar una variante a un producto */
export const addVariant = (productId, data) =>
  api.post(`/products/${productId}/variants/`, data).then(r => r.data)

/** Actualizar una variante (PATCH — campos parciales) */
export const updateVariant = (variantId, data) =>
  api.patch(`/products/variants/${variantId}/`, data).then(r => r.data)

/** Eliminar una variante */
export const deleteVariant = (variantId) =>
  api.delete(`/products/variants/${variantId}/`).then(r => r.data)

// ── Stock ──────────────────────────────────────────────────────────────────

/** Actualizar el stock de una variante */
export const updateStock = (variantId, quantity) =>
  api.patch(`/products/variants/${variantId}/stock/`, { quantity }).then(r => r.data)

/** Verificar disponibilidad de stock para una variante */
export const checkStock = (variantId, quantity) =>
  api.post('/products/check-stock/', { variant_id: variantId, quantity }).then(r => r.data)

import api from './axios'

// ── Catálogo público (ms-inventory v2) ───────────────────────────────────────

export const getProductsV2 = (params = {}) =>
  api.get('/v2/products/', { params }).then(r => r.data)

export const getProductV2 = (id) =>
  api.get(`/v2/products/${id}/`).then(r => r.data)

// ── Admin productos (ms-inventory v2) ─────────────────────────────────────────

export const getProducts = (params = { all: 1 }) =>
  api.get('/v2/products/', { params }).then(r => r.data)

export const getProduct = (id) =>
  api.get(`/v2/products/${id}/`).then(r => r.data)

export const createProduct = (data) =>
  api.post('/v2/products/', data).then(r => {
    const body = r.data
    return body.product ?? body
  })

export const updateProduct = (id, data) =>
  api.patch(`/v2/products/${id}/`, data).then(r => r.data)

export const deleteProduct = (id) =>
  api.delete(`/v2/products/${id}/`).then(r => r.data)

export const addVariant = (productId, data) =>
  api.post(`/v2/products/${productId}/variants/`, data).then(r => r.data)

export const updateVariant = (variantId, data) =>
  api.patch(`/v2/inventory/variants/${variantId}/`, data).then(r => r.data)

export const deleteVariant = (variantId) =>
  api.delete(`/v2/inventory/variants/${variantId}/`).then(r => r.data)

export const updateStock = (variantId, quantity) =>
  api.put('/v2/inventory/update/', { variant_id: variantId, quantity }).then(r => r.data)

export const checkStock = (variantId, quantity) =>
  api.post('/v2/inventory/check-stock/', { variant_id: variantId, quantity }).then(r => r.data)

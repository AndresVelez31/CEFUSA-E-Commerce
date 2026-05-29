import api from './axios'

export const getCart = (cartId) =>
  api.get(`/v2/cart/${cartId}/`).then(r => r.data)

export const addCartItem = (cartId, item) =>
  api.post(`/v2/cart/${cartId}/items/`, item).then(r => r.data)

export const updateCartItem = (cartId, variantId, quantity) =>
  api.put(`/v2/cart/${cartId}/items/${variantId}/`, { quantity }).then(r => r.data)

export const removeCartItem = (cartId, variantId) =>
  api.delete(`/v2/cart/${cartId}/items/${variantId}/`).then(r => r.data)

export const clearCart = (cartId) =>
  api.delete(`/v2/cart/${cartId}/`).then(r => r.data)

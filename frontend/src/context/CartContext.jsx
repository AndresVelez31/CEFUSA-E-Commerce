import { createContext, useContext, useEffect, useMemo, useState } from 'react'
import {
  addCartItem,
  clearCart as clearCartApi,
  getCart,
  removeCartItem,
  updateCartItem,
} from '../api/cart'

const CartContext = createContext(null)

const CART_ID_KEY = 'cart_id'

const getOrCreateCartId = () => {
  const existing = localStorage.getItem(CART_ID_KEY)
  if (existing) return existing
  const newId = typeof crypto !== 'undefined' && crypto.randomUUID
    ? crypto.randomUUID()
    : `${Date.now()}-${Math.random().toString(16).slice(2)}`
  localStorage.setItem(CART_ID_KEY, newId)
  return newId
}

export function CartProvider({ children }) {
  const [cartId] = useState(getOrCreateCartId)
  const [items, setItems] = useState([])
  const [itemCount, setItemCount] = useState(0)
  const [subtotal, setSubtotal] = useState(0)
  const [loading, setLoading] = useState(true)

  const syncCart = async () => {
    setLoading(true)
    try {
      const data = await getCart(cartId)
      setItems(data.items || [])
      setItemCount(data.item_count || 0)
      setSubtotal(data.subtotal || 0)
    } catch (error) {
      console.error('Error cargando el carrito', error)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    syncCart()
  }, [cartId])

  const addItem = async (item) => {
    try {
      await addCartItem(cartId, item)
      await syncCart()
      return true
    } catch (error) {
      console.error('Error agregando item', error)
      return false
    }
  }

  const removeItem = async (variant_id) => {
    try {
      await removeCartItem(cartId, variant_id)
      await syncCart()
    } catch (error) {
      console.error('Error eliminando item', error)
    }
  }

  const updateQuantity = async (variant_id, quantity) => {
    try {
      await updateCartItem(cartId, variant_id, quantity)
      await syncCart()
    } catch (error) {
      console.error('Error actualizando cantidad', error)
    }
  }

  const clearCart = async () => {
    try {
      await clearCartApi(cartId)
      await syncCart()
    } catch (error) {
      console.error('Error vaciando carrito', error)
    }
  }

  const value = useMemo(() => ({
    items,
    itemCount,
    subtotal,
    loading,
    addItem,
    removeItem,
    updateQuantity,
    clearCart,
  }), [items, itemCount, subtotal, loading])

  return (
    <CartContext.Provider value={value}>
      {children}
    </CartContext.Provider>
  )
}

export const useCart = () => {
  const ctx = useContext(CartContext)
  if (!ctx) throw new Error('useCart debe usarse dentro de CartProvider')
  return ctx
}

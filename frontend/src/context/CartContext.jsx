import { createContext, useContext, useReducer, useEffect } from 'react'

const CartContext = createContext(null)

const initialState = {
  items: JSON.parse(localStorage.getItem('cart') || '[]'),
}

function cartReducer(state, action) {
  switch (action.type) {
    case 'ADD_ITEM': {
      const existing = state.items.find(i => i.variant_id === action.payload.variant_id)
      const items = existing
        ? state.items.map(i =>
            i.variant_id === action.payload.variant_id
              ? { ...i, quantity: i.quantity + action.payload.quantity }
              : i
          )
        : [...state.items, action.payload]
      return { items }
    }
    case 'REMOVE_ITEM':
      return { items: state.items.filter(i => i.variant_id !== action.payload) }
    case 'UPDATE_QUANTITY': {
      const items = state.items.map(i =>
        i.variant_id === action.payload.variant_id
          ? { ...i, quantity: action.payload.quantity }
          : i
      ).filter(i => i.quantity > 0)
      return { items }
    }
    case 'CLEAR_CART':
      return { items: [] }
    default:
      return state
  }
}

export function CartProvider({ children }) {
  const [state, dispatch] = useReducer(cartReducer, initialState)

  // Persistir en localStorage
  useEffect(() => {
    localStorage.setItem('cart', JSON.stringify(state.items))
  }, [state.items])

  const addItem     = (item) => dispatch({ type: 'ADD_ITEM', payload: item })
  const removeItem  = (variant_id) => dispatch({ type: 'REMOVE_ITEM', payload: variant_id })
  const updateQuantity = (variant_id, quantity) =>
    dispatch({ type: 'UPDATE_QUANTITY', payload: { variant_id, quantity } })
  const clearCart   = () => dispatch({ type: 'CLEAR_CART' })

  const itemCount   = state.items.reduce((acc, i) => acc + i.quantity, 0)
  const subtotal    = state.items.reduce((acc, i) => acc + parseFloat(i.price) * i.quantity, 0)

  return (
    <CartContext.Provider value={{
      items: state.items,
      itemCount,
      subtotal,
      addItem,
      removeItem,
      updateQuantity,
      clearCart,
    }}>
      {children}
    </CartContext.Provider>
  )
}

export const useCart = () => {
  const ctx = useContext(CartContext)
  if (!ctx) throw new Error('useCart debe usarse dentro de CartProvider')
  return ctx
}

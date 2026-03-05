import { BrowserRouter, Routes, Route } from 'react-router-dom'
import { Toaster } from 'react-hot-toast'
import { CartProvider } from './context/CartContext'
import Navbar from './components/layout/Navbar'
import Footer from './components/layout/Footer'
import HomePage from './pages/HomePage'
import ProductDetailPage from './pages/ProductDetailPage'
import CartPage from './pages/CartPage'
import CheckoutPage from './pages/CheckoutPage'
import OrderConfirmationPage from './pages/OrderConfirmationPage'

export default function App() {
  return (
    <BrowserRouter>
      <CartProvider>
        <div className="min-h-screen flex flex-col bg-dark-900">
          <Navbar />
          <main className="flex-grow">
            <Routes>
              <Route path="/"              element={<HomePage />} />
              <Route path="/products/:id"  element={<ProductDetailPage />} />
              <Route path="/cart"          element={<CartPage />} />
              <Route path="/checkout"      element={<CheckoutPage />} />
              <Route path="/order/:id"     element={<OrderConfirmationPage />} />
            </Routes>
          </main>
          <Footer />
        </div>
        <Toaster
          position="top-right"
          toastOptions={{
            style: { background: '#1e293b', color: '#f1f5f9', border: '1px solid #334155' },
            success: { iconTheme: { primary: '#0ea5e9', secondary: '#fff' } },
          }}
        />
      </CartProvider>
    </BrowserRouter>
  )
}

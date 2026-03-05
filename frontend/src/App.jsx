import { BrowserRouter, Routes, Route } from 'react-router-dom'
import { Toaster } from 'react-hot-toast'
import { CartProvider } from './context/CartContext'

// Layout público
import Navbar from './components/layout/Navbar'
import Footer from './components/layout/Footer'

// Páginas públicas
import HomePage from './pages/HomePage'
import ProductDetailPage from './pages/ProductDetailPage'
import CartPage from './pages/CartPage'
import CheckoutPage from './pages/CheckoutPage'
import OrderConfirmationPage from './pages/OrderConfirmationPage'

// Panel admin
import AdminLayout from './components/admin/AdminLayout'
import AdminDashboardPage from './pages/admin/AdminDashboardPage'
import AdminOrdersPage from './pages/admin/AdminOrdersPage'
import AdminOrderDetailPage from './pages/admin/AdminOrderDetailPage'
import AdminCreateOrderPage from './pages/admin/AdminCreateOrderPage'
import AdminCustomersPage from './pages/admin/AdminCustomersPage'

function StoreLayout() {
  return (
    <div className="min-h-screen flex flex-col bg-dark-900">
      <Navbar />
      <main className="flex-grow">
        <Routes>
          <Route path="/"             element={<HomePage />} />
          <Route path="/products/:id" element={<ProductDetailPage />} />
          <Route path="/cart"         element={<CartPage />} />
          <Route path="/checkout"     element={<CheckoutPage />} />
          <Route path="/order/:id"    element={<OrderConfirmationPage />} />
        </Routes>
      </main>
      <Footer />
    </div>
  )
}

export default function App() {
  return (
    <BrowserRouter>
      <CartProvider>
        <Toaster
          position="top-right"
          toastOptions={{
            style: { background: '#1e293b', color: '#f1f5f9', border: '1px solid #334155' },
            success: { iconTheme: { primary: '#0ea5e9', secondary: '#fff' } },
          }}
        />
        <Routes>
          {/* Panel admin — sin Navbar/Footer del store */}
          <Route path="/admin" element={<AdminLayout />}>
            <Route index                    element={<AdminDashboardPage />} />
            <Route path="orders"            element={<AdminOrdersPage />} />
            <Route path="orders/new"        element={<AdminCreateOrderPage />} />
            <Route path="orders/:id"        element={<AdminOrderDetailPage />} />
            <Route path="customers"         element={<AdminCustomersPage />} />
          </Route>

          {/* Tienda pública — con Navbar/Footer */}
          <Route path="/*" element={<StoreLayout />} />
        </Routes>
      </CartProvider>
    </BrowserRouter>
  )
}


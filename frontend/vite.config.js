import { defineConfig, loadEnv } from 'vite'
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, process.cwd(), '')
  const useNginx = env.VITE_USE_NGINX === 'true'

  // Con start.ps1: Django :8000 y microservicios en 5001-5003 (sin Nginx en :80).
  // Con docker compose: VITE_USE_NGINX=true → todo pasa por Nginx en :80.
  const proxy = useNginx
    ? {
        '/api': {
          target: env.VITE_NGINX_URL || 'http://localhost',
          changeOrigin: true,
        },
      }
    : {
        '/api/v2/products': { target: 'http://localhost:5001', changeOrigin: true },
        '/api/v2/inventory': { target: 'http://localhost:5001', changeOrigin: true },
        '/api/v2/cart': { target: 'http://localhost:5002', changeOrigin: true },
        '/api/v2/customers': { target: 'http://localhost:5003', changeOrigin: true },
        '/api/v2/shipping': { target: 'http://localhost:5004', changeOrigin: true },
        '/api/v2/checkout': { target: 'http://localhost:5000', changeOrigin: true },
        '/api': {
          target: env.VITE_API_PROXY || 'http://localhost:8000',
          changeOrigin: true,
        },
      }

  return {
    plugins: [react()],
    server: {
      port: 3000,
      proxy,
    },
  }
})

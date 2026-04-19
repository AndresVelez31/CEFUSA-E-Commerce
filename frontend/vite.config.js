import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    port: 3000,
    proxy: {
      '/api': {
        // En Docker, Nginx expone :80 y enruta /api/v2 -> Flask y el resto -> Django.
        target: 'http://localhost',
        changeOrigin: true,
      }
    }
  }
})

import api from './axios'

/**
 * Información del servicio QuickBite (API externa vía Django).
 * GET /api/integrations/ally/
 */
export const getQuickBiteInfo = () =>
  api.get('/integrations/ally/').then(r => r.data)

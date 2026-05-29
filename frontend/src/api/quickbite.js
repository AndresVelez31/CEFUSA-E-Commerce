import api from './axios'

/**
 * Información del servicio QuickBite (API externa vía Django).
 * GET /api/integrations/quickbite/info/
 */
export const getQuickBiteInfo = () =>
  api.get('/integrations/quickbite/info/').then(r => r.data)

import { useEffect, useState } from 'react'
import { ServerStackIcon, SignalIcon } from '@heroicons/react/24/outline'
import { getQuickBiteInfo } from '../../api/quickbite'

export default function QuickBiteInfoCard() {
  const [info, setInfo] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    getQuickBiteInfo()
      .then(res => {
        if (res.success) setInfo(res.data)
        else setError(res.message || 'No se pudo obtener la información')
      })
      .catch(err => {
        const status = err.response?.status
        const msg = err.response?.data?.message
        if (status === 404) {
          setError('Ruta no encontrada en Django. Reinicia el servidor (.\start.ps1 o docker compose).')
        } else if (status === 502 || status === 503 || status === 504) {
          setError(msg || 'QuickBite no está disponible en este momento')
        } else {
          setError(msg || 'No se pudo conectar. Verifica que Django esté corriendo.')
        }
      })
      .finally(() => setLoading(false))
  }, [])

  const isOnline = info?.status?.toLowerCase() === 'online'

  return (
    <div className="bg-dark-800 rounded-xl border border-dark-700 p-6">
      <div className="flex items-center gap-3 mb-4">
        <div className="w-10 h-10 rounded-lg bg-orange-500/15 flex items-center justify-center">
          <ServerStackIcon className="w-5 h-5 text-orange-400" />
        </div>
        <div>
          <h3 className="text-gray-800 font-semibold">Integración QuickBite</h3>
          <p className="text-xs text-gray-500">API externa · GET /api/info/</p>
        </div>
      </div>

      {loading && <p className="text-gray-500 text-sm">Consultando servicio...</p>}

      {error && (
        <p className="text-red-400 text-sm bg-red-950/30 border border-red-800 rounded-lg px-3 py-2">
          {error}
        </p>
      )}

      {info && !error && (
        <div className="space-y-3 text-sm">
          <div className="flex items-center justify-between gap-2">
            <span className="text-gray-500">Estado</span>
            <span
              className={`inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full text-xs font-medium ${
                isOnline
                  ? 'bg-emerald-500/15 text-emerald-400'
                  : 'bg-amber-500/15 text-amber-400'
              }`}
            >
              <SignalIcon className="w-3.5 h-3.5" />
              {info.status}
            </span>
          </div>
          <div>
            <p className="text-gray-500">Servicio</p>
            <p className="text-gray-800 font-medium">{info.service}</p>
          </div>
          <div className="grid grid-cols-2 gap-3">
            <div>
              <p className="text-gray-500">Equipo</p>
              <p className="text-gray-800">{info.team}</p>
            </div>
            <div>
              <p className="text-gray-500">Versión</p>
              <p className="text-gray-800 font-mono">{info.version}</p>
            </div>
          </div>
          <div>
            <p className="text-gray-500">Arquitectura</p>
            <p className="text-gray-700">{info.architecture}</p>
          </div>
          {info.endpoints && (
            <div>
              <p className="text-gray-500 mb-2">Endpoints disponibles</p>
              <ul className="space-y-1">
                {Object.entries(info.endpoints).map(([key, path]) => (
                  <li
                    key={key}
                    className="flex justify-between gap-2 text-xs font-mono bg-dark-700/50 rounded px-2 py-1"
                  >
                    <span className="text-gray-500">{key}</span>
                    <span className="text-brand-400">{path}</span>
                  </li>
                ))}
              </ul>
            </div>
          )}
        </div>
      )}
    </div>
  )
}

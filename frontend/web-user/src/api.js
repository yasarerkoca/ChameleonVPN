import axios from 'axios'

// Vite ortam değişkeni: .env → VITE_API_BASE_URL=http://127.0.0.1:8000
const BASE_URL = (import.meta.env.VITE_API_BASE_URL || '/api').replace(/\/+$/, '')

const api = axios.create({
  baseURL: BASE_URL,           // örn: http://127.0.0.1:8000 veya /api
  timeout: 15000,
  withCredentials: false,      // cookie tabanlı oturum yoksa false kalsın
  headers: { 'Content-Type': 'application/json' },
})

// İsteğe bağlı: JWT’yi header’a eklemek için
export const setAuthToken = (token) => {
  if (token) api.defaults.headers.common.Authorization = `Bearer ${token}`
  else delete api.defaults.headers.common.Authorization
}

// ---- Endpoints (başına / KOYMA) ----
export const fetchServers   = () => api.get('servers').then(r => r.data)
export const fetchProfile   = () => api.get('profile').then(r => r.data)
export const updateProfile  = (profile) => api.put('profile', profile).then(r => r.data)
export const fetchKeys      = () => api.get('keys').then(r => r.data)

// Konfig indirme (Blob + dosya adı yakalama)
export const downloadConfig = async () => {
  const res = await api.get('config', { responseType: 'blob' })
  const cd = res.headers['content-disposition'] || ''
  const m = cd.match(/filename="?([^"]+)"?/)
  return { blob: res.data, filename: m?.[1] || 'config.conf' }
}

export default api

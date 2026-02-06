/** API base URL - empty for same-origin (dev proxy or combined deploy) */
const API_BASE = import.meta.env.VITE_API_URL || ''

export function apiUrl(path: string): string {
  const p = path.startsWith('/') ? path : `/${path}`
  return `${API_BASE.replace(/\/$/, '')}${p}`
}

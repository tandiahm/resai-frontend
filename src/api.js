const BACKEND_URL = (import.meta.env.VITE_BACKEND_URL || 'http://localhost:8000').replace(/\/$/, '')

export async function apiCall(path, file, data = {}) {
  const formData = new FormData()
  formData.append('resume', file)
  for (const [key, value] of Object.entries(data)) {
    formData.append(key, String(value))
  }
  const response = await fetch(`${BACKEND_URL}${path}`, { method: 'POST', body: formData })
  if (!response.ok) {
    const text = await response.text()
    throw new Error(`${response.status}: ${text}`)
  }
  return response.json()
}

export async function checkHealth() {
  const response = await fetch(`${BACKEND_URL}/health`)
  if (!response.ok) throw new Error('Health check failed')
  return response.json()
}

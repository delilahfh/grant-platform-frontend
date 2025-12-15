import axios from 'axios'

// Render backend (your live URL). Can be overridden via VITE_API_BASE_URL in .env
const apiClient = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || 'https://grantsapp.onrender.com',
  headers: { 'Content-Type': 'application/json' }
})

export default {
  signUp(userData) {
    return apiClient.post('/signup', userData)
  },
  getBudgetHeadings() {
    return apiClient.get('/budget-headings')
  },
  saveBudgetLine(line) {
    return apiClient.post('/save-budget-line', line)
  },
  getApplications() {
    return apiClient.get('/admin/applications')
  },
  impersonate(userId) {
    return apiClient.post(`/admin/impersonate/${userId}`)
  },
  toggleBan(userId) {
    return apiClient.post(`/admin/ban/${userId}`)
  },
  generateContract(payload) {
    return apiClient.post('/contracts/generate', payload)
  },
  createProcurement(payload) {
    return apiClient.post('/procurement/create', payload)
  },
  getProcurements(userId) {
    return apiClient.get(`/procurements/${userId}`)
  }
}

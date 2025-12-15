import { createRouter, createWebHistory } from 'vue-router'
import Login from '../views/Login.vue' // Import Login
import SignUp from '../views/SignUp.vue'
import ApplicationForm from '../views/ApplicationForm.vue'
import AdminDashboard from '../views/AdminDashboard.vue'
import ProcurementHub from '../views/ProcurementHub.vue'

const routes = [
  { path: '/', redirect: '/login' }, // Redirect to Login first
  { path: '/login', component: Login }, // New Route
  { path: '/signup', component: SignUp },
  { path: '/application', component: ApplicationForm },
  { path: '/admin', component: AdminDashboard },
  { path: '/hub', component: ProcurementHub }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
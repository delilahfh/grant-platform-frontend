<template>
  <div class="card shadow-sm mx-auto mt-5" style="max-width: 400px;">
    <div class="card-header bg-primary text-white text-center">
      <h4>Login</h4>
    </div>
    <div class="card-body">
      <form @submit.prevent="login">
        <div class="mb-3">
          <label>Email</label>
          <input v-model="email" type="email" class="form-control" required />
        </div>
        <div class="mb-3">
          <label>Password</label>
          <input v-model="password" type="password" class="form-control" required />
        </div>
        <button type="submit" class="btn btn-primary w-100" :disabled="loading">
          {{ loading ? 'Logging in...' : 'Login' }}
        </button>
        <p class="text-center mt-3">
          Don't have an account? <router-link to="/signup">Sign Up</router-link>
        </p>
      </form>
      <div v-if="error" class="alert alert-danger mt-3">{{ error }}</div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  data() {
    return { email: '', password: '', loading: false, error: '' }
  },
  methods: {
    async login() {
      this.loading = true;
      this.error = '';
      try {
        // In a real app, this would be a specific /login endpoint. 
        // For this MVP, we will check if the user exists via a simple backend check.
        // NOTE: Ensure your backend has a way to verify users. 
        // Since we didn't build a specific /login endpoint in the simple backend, 
        // we will simulate it or you must add a simple login endpoint to main.py.
        
        // For now, we will simulate a successful login if the email exists in the system
        // You would normally POST to /login here.
        
        // Simulating "Login" by finding user (You should add a real login endpoint to backend)
        // For this fix, let's assume we store "user" in localStorage
        localStorage.setItem('user_role', this.email.includes('admin') ? 'admin' : 'applicant');
        localStorage.setItem('user_token', '12345'); // Fake token
        
        // Reload page to update Navbar
        window.location.href = '/application';
        
      } catch (err) {
        this.error = 'Login failed';
      } finally {
        this.loading = false;
      }
    }
  }
}
</script>
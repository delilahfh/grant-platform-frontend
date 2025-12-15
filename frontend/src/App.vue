<template>
  <div class="container py-4">
    <nav class="navbar navbar-expand-lg navbar-light bg-light mb-4 shadow-sm rounded px-3">
      <a class="navbar-brand fw-bold text-primary" href="#">Grant Platform</a>
      
      <div class="navbar-nav ms-auto">
        <router-link v-if="!isLoggedIn" to="/login" class="nav-link">Login</router-link>
        <router-link v-if="!isLoggedIn" to="/signup" class="btn btn-primary ms-2">Sign Up</router-link>

        <router-link v-if="isLoggedIn && !isAdmin" to="/application" class="nav-link">My Application</router-link>
        <router-link v-if="isLoggedIn && !isAdmin" to="/hub" class="nav-link">Procurement Hub</router-link>

        <router-link v-if="isAdmin" to="/admin" class="nav-link text-danger fw-bold">Admin Panel</router-link>

        <button v-if="isLoggedIn" @click="logout" class="btn btn-outline-secondary ms-3 btn-sm">Logout</button>
      </div>
    </nav>
    <router-view></router-view>
  </div>
</template>

<script>
export default {
  data() {
    return {
      isLoggedIn: !!localStorage.getItem('user_token'),
      isAdmin: localStorage.getItem('user_role') === 'admin'
    }
  },
  methods: {
    logout() {
      localStorage.clear();
      window.location.href = '/login';
    }
  }
}
</script>
<template>
  <div class="container mt-4">
    <div class="d-flex justify-content-between align-items-center mb-4">
      <h2>Admin Dashboard</h2>
      <button class="btn btn-outline-danger" disabled>Export to Excel (next)</button>
    </div>

    <div class="card shadow-sm">
      <div class="card-body">
        <input
          type="text"
          v-model="search"
          placeholder="Search by Entity Name..."
          class="form-control mb-3"
        />

        <table class="table table-hover">
          <thead class="table-dark">
            <tr>
              <th>ID</th>
              <th>Entity Name</th>
              <th>Type</th>
              <th>Email</th>
              <th>Status</th>
              <th>Actions</th>
            </tr>
          </thead>

          <tbody>
            <tr v-for="app in filteredApps" :key="app.user_id" :class="{ 'table-danger': app.is_banned }">
              <td>{{ app.user_id }}</td>
              <td>{{ app.entity_name }}</td>
              <td><span class="badge bg-info">{{ app.entity_type }}</span></td>
              <td>{{ app.email }}</td>
              <td><span class="badge bg-success">{{ app.status }}</span></td>
              <td>
                <div class="btn-group btn-group-sm">
                  <button @click="impersonate(app.user_id)" class="btn btn-primary">View as User</button>
                  <button @click="toggleBan(app.user_id)" class="btn btn-outline-danger">
                    {{ app.is_banned ? 'Unban' : 'Ban' }}
                  </button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script>
import Api from '../services/Api'

export default {
  data() {
    return {
      applications: [],
      search: ''
    }
  },
  computed: {
    filteredApps() {
      return this.applications.filter(app =>
        app.entity_name.toLowerCase().includes(this.search.toLowerCase())
      )
    }
  },
  async mounted() {
    await this.loadData()
  },
  methods: {
    async loadData() {
      const res = await Api.getApplications()
      this.applications = res.data
    },
    async impersonate(userId) {
      if (confirm('You are about to log in as this user. Proceed?')) {
        const res = await Api.impersonate(userId)
        alert(res.data.message)
        this.$router.push('/application')
      }
    },
    async toggleBan(userId) {
      await Api.toggleBan(userId)
      await this.loadData()
    }
  }
}
</script>

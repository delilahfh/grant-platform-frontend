<template>
  <div class="card shadow-sm mx-auto" style="max-width: 800px;">
    <div class="card-header bg-primary text-white">
      <h4 class="mb-0">Grant Platform Registration</h4>
    </div>
    <div class="card-body">
      <form @submit.prevent="submitForm">
        <h5 class="text-primary border-bottom pb-2 mb-3">Entity Information</h5>

        <div class="mb-3">
          <label class="form-label">Type of Applicant</label>
          <select v-model="form.entity_type" class="form-select" required>
            <option disabled value="">Select Type</option>
            <option>Enterprise</option>
            <option>Organization</option>
            <option>Institution</option>
            <option>Seed idea</option>
            <option>Individual</option>
            <option>Other</option>
          </select>
        </div>

        <div class="mb-3">
          <label class="form-label">Location</label>
          <div class="row">
            <div class="col-md-4" v-for="loc in locationOptions" :key="loc">
              <div class="form-check">
                <input class="form-check-input" type="checkbox" :value="loc" v-model="form.locations" />
                <label class="form-check-label">{{ loc }}</label>
              </div>
            </div>
          </div>
        </div>

        <div class="mb-3">
          <label class="form-label">Detailed Address</label>
          <textarea v-model="form.address" class="form-control" rows="2" required></textarea>
        </div>

        <div class="mb-3">
          <label class="form-label">Name of Applying Entity</label>
          <input type="text" v-model="form.entity_name" class="form-control" required />
        </div>

        <h5 class="text-primary border-bottom pb-2 mb-3 mt-4">Primary Focal Point</h5>

        <div class="row">
          <div class="col-md-6 mb-3">
            <label class="form-label">Full Name</label>
            <input type="text" v-model="form.fp1_name" class="form-control" required />
          </div>
          <div class="col-md-6 mb-3">
            <label class="form-label">Email</label>
            <input type="email" v-model="form.fp1_email" class="form-control" required />
          </div>
        </div>

        <div class="row">
          <div class="col-md-6 mb-3">
            <label class="form-label">Date of Birth</label>
            <input type="date" v-model="form.fp1_dob" class="form-control" required />
          </div>
          <div class="col-md-6 mb-3">
            <label class="form-label">Gender</label>
            <select v-model="form.fp1_gender" class="form-select" required>
              <option>Man</option>
              <option>Woman</option>
              <option>Nonbinary</option>
              <option>Other</option>
            </select>
          </div>
        </div>

        <h5 class="text-primary border-bottom pb-2 mb-3 mt-4">Login Details</h5>

        <div class="mb-3">
          <label class="form-label">Login Email</label>
          <input type="email" v-model="form.email" class="form-control" required />
        </div>

        <div class="mb-3">
          <label class="form-label">Password</label>
          <input type="password" v-model="form.password" class="form-control" required />
        </div>

        <div class="d-grid gap-2 mt-4">
          <button type="submit" class="btn btn-primary btn-lg" :disabled="loading">
            {{ loading ? 'Creating Account...' : 'Sign Up' }}
          </button>
        </div>

        <div v-if="message" class="alert mt-3" :class="isError ? 'alert-danger' : 'alert-success'">
          {{ message }}
        </div>
      </form>
    </div>
  </div>
</template>

<script>
import Api from '../services/Api'

export default {
  data() {
    return {
      loading: false,
      message: '',
      isError: false,
      locationOptions: [
        'Beirut', 'Mount Lebanon', 'Akkar', 'Batroun', 'Kesserwan', 'Jbeil',
        'Baalbeck', 'Bekaa', 'Nabatieh', 'Saida', 'Iqlim al Kharroub el Chemali',
        'Iqlim al Kharroub el Janoubi', 'South', 'Other'
      ],
      form: {
        entity_type: '',
        locations: [],
        address: '',
        entity_name: '',
        fp1_name: '',
        fp1_email: '',
        fp1_dob: '',
        fp1_gender: 'Man',
        email: '',
        password: ''
      }
    }
  },
  methods: {
    async submitForm() {
      this.loading = true
      this.message = ''
      try {
        await Api.signUp(this.form)
        this.isError = false
        this.message = 'Account created successfully! (Login will be added next.)'
        // you can redirect after adding login
      } catch (error) {
        this.isError = true
        this.message = error.response?.data?.detail || 'An error occurred.'
      } finally {
        this.loading = false
      }
    }
  }
}
</script>

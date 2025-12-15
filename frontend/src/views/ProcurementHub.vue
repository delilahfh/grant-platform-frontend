<template>
  <div class="container mt-4">
    <h2>Implementation Hub</h2>
    <ul class="nav nav-tabs mb-4">
      <li class="nav-item"><a class="nav-link" :class="{active: tab==='contract'}" @click="tab='contract'" href="#">1. Contract</a></li>
      <li class="nav-item"><a class="nav-link" :class="{active: tab==='procurement'}" @click="tab='procurement'" href="#">2. Procurement</a></li>
    </ul>

    <div v-if="tab === 'contract'" class="card p-4">
      <div v-if="!contractSigned">
        <h4>Submit Contract Information</h4>
        <p class="text-muted">Please provide your details so the Admin can generate your contract.</p>
        <div class="row">
          <div class="col-md-6 mb-3">
            <label>Signatory Full Name</label>
            <input v-model="contractForm.signatory_name" class="form-control">
          </div>
          <div class="col-md-6 mb-3">
            <label>Passport Number</label>
            <input v-model="contractForm.passport_number" class="form-control">
          </div>
          <div class="col-md-6 mb-3">
            <label>Entity Registration Number</label>
            <input v-model="contractForm.reg_number" class="form-control">
          </div>
        </div>
        <button @click="submitContractInfo" class="btn btn-primary">Submit Info to Admin</button>
      </div>
      
      <div v-else>
        <div class="alert alert-success">
          <h5>Contract Generated</h5>
          <p>The admin has generated your contract. Please download, sign, and upload below.</p>
        </div>
        <button class="btn btn-success me-2">Download Contract PDF</button>
        <button class="btn btn-warning">Upload Signed Scan</button>
      </div>
    </div>

    <div v-if="tab === 'procurement'" class="card p-4">
      <h4>Launch New Procurement</h4>
      <div class="row g-3 align-items-end mb-4 border-bottom pb-4">
        <div class="col-md-3">
            <label>Method</label>
            <select v-model="procForm.method" class="form-select">
                <option value="SQ">Single Quote (SQ)</option>
                <option value="2Q">2 Quotations (2Q)</option> <option value="3Q">3 Quotations (3Q)</option>
                <option value="OLT">Open Tender (OLT)</option>
            </select>
        </div>
        <div class="col-md-3">
            <label>Type</label>
            <select v-model="procForm.type" class="form-select">
                <option>Service</option>
                <option>Product</option>
                <option>Works</option>
                <option>Consultancy</option>
            </select>
        </div>
        <div class="col-md-4">
            <label>Description</label>
            <input v-model="procForm.description" class="form-control" placeholder="e.g. Laptops">
        </div>
        <div class="col-md-2">
            <button @click="createProcurement" class="btn btn-primary w-100">Create</button>
        </div>
      </div>
      </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  data() {
    return {
      tab: 'contract',
      contractSigned: false, // In real app, check DB status
      contractForm: { signatory_name: '', passport_number: '', reg_number: '' },
      procForm: { method: 'SQ', type: 'Product', description: '' },
      procurements: []
    }
  },
  methods: {
    async submitContractInfo() {
        // Send to backend
        alert("Info submitted! Waiting for Admin to generate contract.");
        this.contractSigned = true; // Fake state change for demo
    },
    async createProcurement() {
        // User ID is handled by backend session in real app
        await axios.post('https://grant-platform-api.onrender.com/procurement/create', {
            ...this.procForm,
            user_id: 1, // Hardcoded for MVP, real app uses token
            budget_line_id: 1 
        });
        alert("Procurement Created");
    }
  }
}
</script>
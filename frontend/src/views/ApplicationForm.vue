<template>
  <div class="container mt-4">
    <h2 class="mb-4">Grant Application</h2>

    <ul class="nav nav-tabs mb-4">
      <li class="nav-item">
        <a class="nav-link" :class="{active: tab==='financial'}" @click="tab='financial'" href="#">Financial Proposal</a>
      </li>
      <li class="nav-item">
        <a class="nav-link" :class="{active: tab==='narrative'}" @click="tab='narrative'" href="#">Narrative Proposal</a>
      </li>
    </ul>

    <div v-if="tab === 'financial'">
      <div v-if="headings.length === 0" class="alert alert-warning">
        Loading budget headings... (If this takes too long, ensure Backend is running)
      </div>

      <div v-for="(heading, index) in headings" :key="heading.id" class="card mb-4 shadow-sm">
        <div class="card-header bg-light fw-bold">
          {{ index + 1 }}. {{ heading.name }}
        </div>
        <div class="card-body p-0">
          <table class="table table-bordered mb-0">
            <thead class="table-light">
              <tr>
                <th style="width: 5%">#</th>
                <th style="width: 35%">Item Name</th>
                <th style="width: 15%">Unit Amt</th>
                <th style="width: 15%">Price/Unit</th>
                <th style="width: 15%">Total</th>
                <th style="width: 15%">Action</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(line, lineIndex) in getLinesForHeading(heading.id)" :key="lineIndex">
                <td>{{ index + 1 }}.{{ lineIndex + 1 }}</td>
                <td><input v-model="line.item_name" class="form-control form-control-sm" placeholder="Description"></td>
                <td><input v-model.number="line.unit_amount" type="number" class="form-control form-control-sm"></td>
                <td><input v-model.number="line.price_per_unit" type="number" class="form-control form-control-sm"></td>
                <td>${{ (line.unit_amount * line.price_per_unit).toFixed(2) }}</td>
                <td><button @click="saveLine(line)" class="btn btn-sm btn-success">Save</button></td>
              </tr>
              <tr v-if="getLinesForHeading(heading.id).length === 0">
                <td colspan="6" class="text-center text-muted p-3">No budget lines yet. Add one below.</td>
              </tr>
            </tbody>
          </table>
          <div class="p-3 bg-light border-top">
              <button @click="addLine(heading.id)" class="btn btn-outline-primary btn-sm">+ Add Line Item</button>
          </div>
        </div>
      </div>
    </div>

    <div v-if="tab === 'narrative'">
      <div class="card p-4">
        <h4>Project Narrative</h4>
        <div class="mb-3">
          <label class="form-label fw-bold">1. Project Summary</label>
          <textarea class="form-control" rows="4" placeholder="Describe your project..."></textarea>
        </div>
        
        <label class="form-label fw-bold mt-3">2. Activities & KPIs</label>
        <table class="table table-bordered">
          <thead>
            <tr><th>Activity Description</th><th>Associated KPI</th><th>Timeline (Month 1-12)</th></tr>
          </thead>
          <tbody>
            <tr>
              <td><input class="form-control" placeholder="Activity 1"></td>
              <td><input class="form-control" placeholder="KPI 1"></td>
              <td><input type="checkbox"> M1 <input type="checkbox"> M2</td>
            </tr>
          </tbody>
        </table>
        <button class="btn btn-outline-primary btn-sm">+ Add Activity</button>
      </div>
    </div>

  </div>
</template>

<script>
import axios from 'axios'

export default {
  data() {
    return {
      tab: 'financial',
      headings: [],
      budgetLines: [] 
    }
  },
  async mounted() {
    // UPDATED: Using the full URL to ensure it hits your Render backend
    try {
      const response = await axios.get('https://grant-platform-api.onrender.com/budget-headings');
      this.headings = response.data;
    } catch (e) {
      console.error("Failed to load headings", e);
      // Fallback data so the UI doesn't look broken during testing
      this.headings = [{id: 1, name: "Machineries (Fallback)"}, {id: 2, name: "Works (Fallback)"}];
    }
  },
  methods: {
    getLinesForHeading(headingId) {
        return this.budgetLines.filter(l => l.heading_id === headingId);
    },
    addLine(headingId) {
        this.budgetLines.push({
            heading_id: headingId,
            item_name: '',
            unit_amount: 0,
            price_per_unit: 0,
            co_financing_percent: 0
        });
    },
    async saveLine(line) {
        try {
            await axios.post('https://grant-platform-api.onrender.com/save-budget-line', line);
            alert('Saved!');
        } catch (err) {
            alert('Error saving. Is backend running?');
        }
    }
  }
}
</script>
<template>
  <div class="emp-perf">
    <div class="kpi-grid">
      <div class="kpi-card"><div class="kpi-label">Completed</div><div class="kpi-value">{{ counts.completed }}</div></div>
      <div class="kpi-card"><div class="kpi-label">In Progress</div><div class="kpi-value">{{ counts.in_progress }}</div></div>
      <div class="kpi-card"><div class="kpi-label">Open</div><div class="kpi-value">{{ counts.open }}</div></div>
      <div class="kpi-card"><div class="kpi-label">Total Hours</div><div class="kpi-value">{{ time.total_hours }}</div></div>
      <div class="kpi-card"><div class="kpi-label">Busy Days</div><div class="kpi-value">{{ time.days_busy }}</div></div>
    </div>
    <div class="charts-grid">
      <div class="chart-card"><div class="chart-title">Daily Hours (last 14 days)</div><div class="chart-container"><canvas ref="hoursChart"></canvas></div></div>
      <div class="chart-card"><div class="chart-title">Ticket Status</div><div class="chart-container"><canvas ref="statusChart"></canvas></div></div>
    </div>
    <div class="current-ticket" v-if="current_ticket">
      <div class="ct-header">Current Ticket</div>
      <div class="ct-body">
        <div class="ct-title">{{ current_ticket.title }}</div>
        <div class="ct-meta">
          <span class="badge" :class="'badge-' + (current_ticket.priority === 'high' || current_ticket.priority === 'urgent' ? 'red' : current_ticket.priority === 'medium' ? 'amber' : 'blue')">{{ current_ticket.priority }}</span>
          <span class="badge badge-gray">{{ current_ticket.department }}</span>
          <span class="elapsed">{{ formatDuration(current_ticket.elapsed_seconds) }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { Chart, registerables } from 'chart.js'
import { performanceAPI } from '../api'
Chart.register(...registerables)

export default {
  name: 'EmployeePerformance',
  props: {
    userId: { type: [Number, String], default: null }
  },
  data() {
    return {
      loading: false,
      counts: { completed: 0, in_progress: 0, open: 0, failed: 0, assigned: 0 },
      time: { total_hours: 0, days_busy: 0 },
      daily_hours: { labels: [], values: [] },
      current_ticket: null,
      charts: {}
    }
  },
  async mounted() {
    await this.load()
  },
  beforeUnmount() {
    Object.values(this.charts).forEach(c => c && c.destroy())
  },
  methods: {
    async load() {
      try {
        this.loading = true
        const res = this.userId ? await performanceAPI.getForUser(this.userId) : await performanceAPI.getMine()
        const data = res.data || {}
        this.counts = data.counts || this.counts
        this.time = data.time || this.time
        this.daily_hours = data.daily_hours || this.daily_hours
        this.current_ticket = data.current_ticket || null
        await this.$nextTick()
        this.drawCharts()
      } catch (e) {
        console.error('Failed to load performance', e)
      } finally {
        this.loading = false
      }
    },
    drawCharts() {
      
      const hoursEl = this.$refs.hoursChart
      if (hoursEl) {
        if (this.charts.hours) this.charts.hours.destroy()
        this.charts.hours = new Chart(hoursEl, {
          type: 'line',
          data: {
            labels: this.daily_hours.labels,
            datasets: [{
              label: 'Hours',
              data: this.daily_hours.values,
              fill: true,
              backgroundColor: 'rgba(59,130,246,0.15)',
              borderColor: '#3B82F6',
              tension: 0.35,
              pointRadius: 2
            }]
          },
          options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: { legend: { display: false } },
            scales: {
              y: { beginAtZero: true }
            }
          }
        })
      }
      
      const statusEl = this.$refs.statusChart
      if (statusEl) {
        if (this.charts.status) this.charts.status.destroy()
        this.charts.status = new Chart(statusEl, {
          type: 'doughnut',
          data: {
            labels: ['Completed', 'In Progress', 'Open', 'Failed'],
            datasets: [{
              data: [
                this.counts.completed || 0,
                this.counts.in_progress || 0,
                this.counts.open || 0,
                this.counts.failed || 0
              ],
              backgroundColor: ['#22C55E','#F59E0B','#3B82F6','#EF4444'],
              borderWidth: 2,
              borderColor: '#0f172a'
            }]
          },
          options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: { legend: { position: 'bottom' } }
          }
        })
      }
    },
    formatDuration(seconds) {
      const s = Number(seconds || 0)
      const h = Math.floor(s / 3600)
      const m = Math.floor((s % 3600) / 60)
      return `${h}h ${m}m`
    }
  }
}
</script>
<style scoped>
.emp-perf { display:flex; flex-direction:column; gap:1rem; }
.kpi-grid { display:grid; grid-template-columns:repeat(auto-fill,minmax(140px,1fr)); gap:.75rem; }
.kpi-card { background:#fff; border:1px solid var(--border-color); border-radius:var(--radius-md); padding:.75rem 1rem; }
.kpi-label { font-size:.6875rem; color:var(--gray-500); text-transform:uppercase; letter-spacing:.04em; }
.kpi-value { font-size:1.375rem; font-weight:700; color:var(--gray-900); }
.charts-grid { display:grid; grid-template-columns:1.5fr 1fr; gap:1rem; }
.chart-card { background:#fff; border:1px solid var(--border-color); border-radius:var(--radius-md); padding:1rem; min-height:260px; }
.chart-title { font-weight:600; font-size:.8125rem; color:var(--gray-900); margin-bottom:.5rem; }
.chart-container { position:relative; height:220px; }
.current-ticket { background:#fff; border:1px solid var(--border-color); border-radius:var(--radius-md); padding:1rem; }
.ct-header { font-weight:600; font-size:.8125rem; color:var(--gray-500); text-transform:uppercase; letter-spacing:.04em; margin-bottom:.375rem; }
.ct-title { font-size:1rem; font-weight:700; color:var(--gray-900); }
.ct-meta { display:flex; gap:.5rem; align-items:center; margin-top:.375rem; }
.elapsed { font-size:.8125rem; color:var(--gray-500); font-weight:500; }
@media(max-width:768px){ .charts-grid{grid-template-columns:1fr;} }
</style>

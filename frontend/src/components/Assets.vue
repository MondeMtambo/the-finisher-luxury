<template>
  <div class="assets-page">
    <div class="page-header">
      <div>
        <h1>Asset Management (ADMP)</h1>
        <p class="page-subtitle">Track and manage company assets, equipment, and property</p>
      </div>
      <div class="header-actions">
        <select v-model="filterStatus" class="filter-select" @change="loadAssets">
          <option value="">All Status</option>
          <option value="active">Active</option>
          <option value="available">Available</option>
          <option value="maintenance">Maintenance</option>
          <option value="retired">Retired</option>
          <option value="lost">Lost/Stolen</option>
        </select>
        <select v-model="filterCategory" class="filter-select" @change="loadAssets">
          <option value="">All Categories</option>
          <option v-for="cat in categories" :key="cat.id" :value="cat.id">{{ cat.name }}</option>
        </select>
        <button v-if="canAddAssets" @click="openCreateModal" class="btn btn-primary">
          <svg width="16" height="16" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><line x1="8" y1="3" x2="8" y2="13"/><line x1="3" y1="8" x2="13" y2="8"/></svg>
          Add Asset
        </button>
      </div>
    </div>

    <div v-if="!loading && stats" class="stats-grid">
      <div class="stat-card">
        <div class="stat-icon" style="background:#eff6ff;color:var(--primary-500)">
          <svg width="20" height="20" fill="currentColor"><path d="M3 3h18v4H3V3zm0 6h18v12H3V9z"/></svg>
        </div>
        <div class="stat-content">
          <div class="stat-value">{{ stats.total_assets || 0 }}</div>
          <div class="stat-label">Total Assets</div>
        </div>
      </div>
      <div class="stat-card">
        <div class="stat-icon" style="background:#d1fae5;color:#059669">
          <svg width="20" height="20" fill="currentColor"><path d="M9 12l-3-3-3 3m0 0l3-3m-3 3h12"/></svg>
        </div>
        <div class="stat-content">
          <div class="stat-value">{{ stats.assigned || 0 }}</div>
          <div class="stat-label">Assigned</div>
        </div>
      </div>
      <div class="stat-card">
        <div class="stat-icon" style="background:#fef3c7;color:#d97706">
          <svg width="20" height="20" fill="currentColor"><circle cx="10" cy="10" r="8"/></svg>
        </div>
        <div class="stat-content">
          <div class="stat-value">{{ stats.available || 0 }}</div>
          <div class="stat-label">Available</div>
        </div>
      </div>
      <div class="stat-card">
        <div class="stat-icon" style="background:#e0e7ff;color:#4f46e5">
          <svg width="20" height="20" fill="currentColor"><path d="M12 2v10l6 6H6l6-6V2h0z"/></svg>
        </div>
        <div class="stat-content">
          <div class="stat-value">{{ formatCurrency(stats.total_current_value || 0) }}</div>
          <div class="stat-label">Total Value</div>
        </div>
      </div>
    </div>

    <div v-if="loading" class="spinner-container">
      <span class="spinner"></span>
      <p style="margin-top:1rem;color:var(--gray-500)">Loading assets...</p>
    </div>

    <div v-if="!loading && assets.length > 0" class="assets-grid">
      <div v-for="asset in assets" :key="asset.id" class="asset-card" @click="viewAsset(asset)">
        <div class="asset-header">
          <div class="asset-tag">{{ asset.asset_tag }}</div>
          <span class="badge" :class="statusBadgeClass(asset.status)">{{ asset.status_display }}</span>
        </div>
        <h3 class="asset-name">{{ asset.name }}</h3>
        <div class="asset-meta">
          <div class="meta-item">
            <svg width="14" height="14" fill="currentColor"><path d="M3 3h8v8H3z"/></svg>
            <span>{{ asset.category_name }}</span>
          </div>
          <div class="meta-item" v-if="asset.assigned_to_name">
            <svg width="14" height="14" fill="currentColor"><circle cx="7" cy="5" r="3"/><path d="M1 14s1-4 6-4 6 4 6 4"/></svg>
            <span>{{ asset.assigned_to_name }}</span>
          </div>
          <div class="meta-item" v-if="asset.location">
            <svg width="14" height="14" fill="currentColor"><path d="M7 1l4 12H3z"/></svg>
            <span>{{ asset.location }}</span>
          </div>
        </div>
        <div class="asset-footer">
          <div class="asset-value" v-if="asset.current_value">{{ formatCurrency(asset.current_value) }}</div>
          <div class="asset-condition">
            <span class="condition-dot" :class="'condition-' + asset.condition"></span>
            {{ asset.condition_display }}
          </div>
        </div>
      </div>
    </div>

    <div v-if="!loading && assets.length === 0" class="empty-state">
      <svg width="64" height="64" fill="none" stroke="var(--gray-300)" stroke-width="2">
        <rect x="8" y="8" width="48" height="48" rx="4"/>
        <line x1="24" y1="24" x2="40" y2="24"/>
        <line x1="24" y1="32" x2="32" y2="32"/>
      </svg>
      <h3>No assets found</h3>
      <p v-if="canAddAssets">Start tracking your company assets by adding the first one</p>
      <p v-else>You don't have any assets assigned to you yet</p>
      <button v-if="canAddAssets" @click="openCreateModal" class="btn btn-primary">Add First Asset</button>
    </div>

    <div v-if="showModal" class="modal-overlay" @click="closeModal">
      <div class="modal-panel modal-lg" @click.stop>
        <div class="modal-header">
          <h3>{{ isEditMode ? 'Edit Asset' : 'Add New Asset' }}</h3>
          <button class="modal-close" @click="closeModal">&times;</button>
        </div>
        <div class="modal-body">
          <form @submit.prevent="saveAsset">

            <div class="form-section">
              <h4 class="section-title">Basic Information</h4>
              <div class="form-grid-2">
                <div class="form-group">
                  <label>Asset Tag <span class="required">*</span></label>
                  <input v-model="form.asset_tag" required placeholder="e.g., LAP-001" />
                </div>
                <div class="form-group">
                  <label>Asset Name <span class="required">*</span></label>
                  <input v-model="form.name" required placeholder="e.g., Dell Latitude Laptop" />
                </div>
              </div>
              <div class="form-grid-2">
                <div class="form-group">
                  <label>Category <span class="required">*</span></label>
                  <select v-model="form.category" required>
                    <option value="">Select category</option>
                    <option v-for="cat in categories" :key="cat.id" :value="cat.id">{{ cat.name }}</option>
                  </select>
                </div>
                <div class="form-group">
                  <label>Serial Number</label>
                  <input v-model="form.serial_number" placeholder="Manufacturer serial number" />
                </div>
              </div>
              <div class="form-grid-2">
                <div class="form-group">
                  <label>Model</label>
                  <input v-model="form.model" placeholder="e.g., Latitude 5420" />
                </div>
                <div class="form-group">
                  <label>Manufacturer</label>
                  <input v-model="form.manufacturer" placeholder="e.g., Dell" />
                </div>
              </div>
            </div>

            <div class="form-section">
              <h4 class="section-title">Financial Information</h4>
              <div class="form-grid-2">
                <div class="form-group">
                  <label>Purchase Date</label>
                  <input type="date" v-model="form.purchase_date" />
                </div>
                <div class="form-group">
                  <label>Purchase Cost (ZAR)</label>
                  <input type="number" step="0.01" v-model="form.purchase_cost" placeholder="0.00" />
                </div>
              </div>
              <div class="form-grid-2">
                <div class="form-group">
                  <label>Current Value (ZAR)</label>
                  <input type="number" step="0.01" v-model="form.current_value" placeholder="0.00" />
                </div>
                <div class="form-group">
                  <label>Warranty Expiry</label>
                  <input type="date" v-model="form.warranty_expiry" />
                </div>
              </div>
            </div>

            <div class="form-section">
              <h4 class="section-title">Status & Assignment</h4>
              <div class="form-grid-2">
                <div class="form-group">
                  <label>Status</label>
                  <select v-model="form.status">
                    <option value="active">Active/In Use</option>
                    <option value="available">Available</option>
                    <option value="maintenance">Under Maintenance</option>
                    <option value="retired">Retired/Disposed</option>
                    <option value="lost">Lost/Stolen</option>
                  </select>
                </div>
                <div class="form-group">
                  <label>Condition</label>
                  <select v-model="form.condition">
                    <option value="excellent">Excellent</option>
                    <option value="good">Good</option>
                    <option value="fair">Fair</option>
                    <option value="poor">Poor</option>
                    <option value="damaged">Damaged</option>
                  </select>
                </div>
              </div>
              <div class="form-grid-2">
                <div class="form-group">
                  <label>Assigned To (Employee)</label>
                  <select v-model="form.assigned_to">
                    <option value="">Not assigned</option>
                    <option v-for="emp in employees" :key="emp.user" :value="emp.user">
                      {{ emp.full_name || emp.username }}
                    </option>
                  </select>
                </div>
                <div class="form-group">
                  <label>Division</label>
                  <select v-model="form.division">
                    <option value="">No division</option>
                    <option v-for="div in divisions" :key="div.id" :value="div.id">
                      {{ div.name }}
                    </option>
                  </select>
                </div>
              </div>
              <div class="form-group">
                <label>Location</label>
                <input v-model="form.location" placeholder="e.g., HQ Office - Floor 2 - Desk 12" />
              </div>
            </div>

            <div class="form-section">
              <div class="form-group">
                <label>Notes</label>
                <textarea v-model="form.notes" rows="3" placeholder="Additional notes, maintenance history, etc."></textarea>
              </div>
            </div>

            <div class="modal-actions">
              <button type="button" @click="closeModal" class="btn btn-secondary">Cancel</button>
              <button type="submit" class="btn btn-primary" :disabled="saving">
                {{ saving ? 'Saving...' : (isEditMode ? 'Update Asset' : 'Create Asset') }}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>

    <div v-if="showViewModal && selectedAsset" class="modal-overlay" @click="closeViewModal">
      <div class="modal-panel modal-lg" @click.stop>
        <div class="modal-header">
          <h3>{{ selectedAsset.name }}</h3>
          <button class="modal-close" @click="closeViewModal">&times;</button>
        </div>
        <div class="modal-body">
          <div class="asset-detail">
            <div class="detail-section">
              <h4>Basic Information</h4>
              <div class="detail-grid">
                <div class="detail-item"><span class="label">Asset Tag:</span><span class="value">{{ selectedAsset.asset_tag }}</span></div>
                <div class="detail-item"><span class="label">Category:</span><span class="value">{{ selectedAsset.category_name }}</span></div>
                <div class="detail-item"><span class="label">Serial Number:</span><span class="value">{{ selectedAsset.serial_number || '-' }}</span></div>
                <div class="detail-item"><span class="label">Model:</span><span class="value">{{ selectedAsset.model || '-' }}</span></div>
                <div class="detail-item"><span class="label">Manufacturer:</span><span class="value">{{ selectedAsset.manufacturer || '-' }}</span></div>
              </div>
            </div>
            <div class="detail-section">
              <h4>Financial</h4>
              <div class="detail-grid">
                <div class="detail-item"><span class="label">Purchase Date:</span><span class="value">{{ formatDate(selectedAsset.purchase_date) }}</span></div>
                <div class="detail-item"><span class="label">Purchase Cost:</span><span class="value">{{ formatCurrency(selectedAsset.purchase_cost) }}</span></div>
                <div class="detail-item"><span class="label">Current Value:</span><span class="value">{{ formatCurrency(selectedAsset.current_value) }}</span></div>
                <div class="detail-item"><span class="label">Depreciation:</span><span class="value">{{ formatCurrency(selectedAsset.depreciation) }}</span></div>
                <div class="detail-item"><span class="label">Warranty:</span><span class="value">{{ selectedAsset.warranty_status }} {{ selectedAsset.warranty_expiry ? '(expires ' + formatDate(selectedAsset.warranty_expiry) + ')' : '' }}</span></div>
              </div>
            </div>
            <div class="detail-section">
              <h4>Status & Assignment</h4>
              <div class="detail-grid">
                <div class="detail-item"><span class="label">Status:</span><span class="value"><span class="badge" :class="statusBadgeClass(selectedAsset.status)">{{ selectedAsset.status_display }}</span></span></div>
                <div class="detail-item"><span class="label">Condition:</span><span class="value">{{ selectedAsset.condition_display }}</span></div>
                <div class="detail-item"><span class="label">Assigned To:</span><span class="value">{{ selectedAsset.assigned_to_name || 'Not assigned' }}</span></div>
                <div class="detail-item"><span class="label">Division:</span><span class="value">{{ selectedAsset.division_name || '-' }}</span></div>
                <div class="detail-item"><span class="label">Location:</span><span class="value">{{ selectedAsset.location || '-' }}</span></div>
              </div>
            </div>
            <div class="detail-section" v-if="selectedAsset.notes">
              <h4>Notes</h4>
              <p style="color:var(--gray-600);line-height:1.6">{{ selectedAsset.notes }}</p>
            </div>
          </div>
          <div class="modal-actions">
            <button @click="editAsset(selectedAsset)" class="btn btn-secondary">Edit</button>
            <button @click="confirmDelete(selectedAsset)" class="btn btn-danger">Delete</button>
            <button @click="closeViewModal" class="btn btn-primary">Close</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { assetsAPI, assetCategoriesAPI, divisionsAPI, employeesAPI } from '../api'
import toast from '../utils/toast'
import modal from '../utils/modal'
import authService from '../services/auth'

export default {
  name: 'Assets',
  data() {
    return {
      assets: [],
      categories: [],
      divisions: [],
      employees: [],
      stats: null,
      loading: false,
      saving: false,
      showModal: false,
      showViewModal: false,
      isEditMode: false,
      selectedAsset: null,
      filterStatus: '',
      filterCategory: '',
      form: this.getEmptyForm()
    }
  },
  computed: {
    canAddAssets() {
      const user = authService.getUser() || {}
      
      if (user.is_superuser || user.is_staff) return true
      const role = user.role || user.profile?.role
      return role === 'admin' || role === 'manager'
    }
  },
  mounted() {
    this.loadData()
  },
  methods: {
    async loadData() {
      this.loadAssets()
      this.loadCategories()
      this.loadDivisions()
      this.loadEmployees()
      this.loadStats()
    },
    async loadAssets() {
      this.loading = true
      try {
        const params = {}
        if (this.filterStatus) params.status = this.filterStatus
        if (this.filterCategory) params.category = this.filterCategory
        const response = await assetsAPI.getAll(params)
        this.assets = response.data
      } catch (error) {
        console.error('Error loading assets:', error)
        toast.error('Failed to load assets')
      } finally {
        this.loading = false
      }
    },
    async loadCategories() {
      try {
        const response = await assetCategoriesAPI.getAll()
        this.categories = response.data
        
        
        if (this.categories.length === 0) {
          console.log('No categories found, seeding defaults...')
          try {
            const seedResponse = await assetCategoriesAPI.seedDefaults()
            this.categories = seedResponse.data.categories || []
            this.$notify({ type: 'success', text: `Created ${this.categories.length} default asset categories` })
          } catch (seedError) {
            console.warn('Category seeding skipped:', seedError.response?.data?.message || seedError.message)
          }
        }
      } catch (error) {
        console.error('Error loading categories:', error)
      }
    },
    async loadDivisions() {
      try {
        const response = await divisionsAPI.getAll()
        this.divisions = response.data
      } catch (error) {
        console.error('Error loading divisions:', error)
      }
    },
    async loadEmployees() {
      try {
        const response = await employeesAPI.getAll()
        this.employees = response.data
      } catch (error) {
        console.error('Error loading employees:', error)
      }
    },
    async loadStats() {
      try {
        const response = await assetsAPI.getStats()
        this.stats = response.data
      } catch (error) {
        console.error('Error loading stats:', error)
      }
    },
    getEmptyForm() {
      return {
        asset_tag: '',
        name: '',
        category: '',
        serial_number: '',
        model: '',
        manufacturer: '',
        purchase_date: null,
        purchase_cost: null,
        current_value: null,
        warranty_expiry: null,
        status: 'available',
        condition: 'good',
        assigned_to: '',
        division: '',
        location: '',
        notes: ''
      }
    },
    openCreateModal() {
      this.isEditMode = false
      this.form = this.getEmptyForm()
      this.showModal = true
    },
    editAsset(asset) {
      this.isEditMode = true
      this.form = {
        id: asset.id,
        asset_tag: asset.asset_tag,
        name: asset.name,
        category: asset.category,
        serial_number: asset.serial_number || '',
        model: asset.model || '',
        manufacturer: asset.manufacturer || '',
        purchase_date: asset.purchase_date || null,
        purchase_cost: asset.purchase_cost || null,
        current_value: asset.current_value || null,
        warranty_expiry: asset.warranty_expiry || null,
        status: asset.status,
        condition: asset.condition,
        assigned_to: asset.assigned_to || '',
        division: asset.division || '',
        location: asset.location || '',
        notes: asset.notes || ''
      }
      this.closeViewModal()
      this.showModal = true
    },
    viewAsset(asset) {
      this.selectedAsset = asset
      this.showViewModal = true
    },
    closeModal() {
      this.showModal = false
      this.form = this.getEmptyForm()
    },
    closeViewModal() {
      this.showViewModal = false
      this.selectedAsset = null
    },
    async saveAsset() {
      this.saving = true
      try {
        const payload = { ...this.form }
        
        if (!payload.assigned_to) payload.assigned_to = null
        if (!payload.division) payload.division = null
        if (!payload.purchase_cost) payload.purchase_cost = null
        if (!payload.current_value) payload.current_value = null

        if (this.isEditMode) {
          await assetsAPI.update(this.form.id, payload)
          toast.success('Asset updated successfully')
        } else {
          await assetsAPI.create(payload)
          toast.success('Asset created successfully')
        }
        this.closeModal()
        this.loadData()
      } catch (error) {
        console.error('Error saving asset:', error)
        const msg = error.response?.data?.message || error.response?.data?.error || 'Failed to save asset'
        toast.error(msg)
      } finally {
        this.saving = false
      }
    },
    confirmDelete(asset) {
      modal.confirm(
        'Delete Asset',
        `Are you sure you want to delete "${asset.name}" (${asset.asset_tag})? This action cannot be undone.`,
        async () => {
          try {
            await assetsAPI.delete(asset.id)
            toast.success('Asset deleted successfully')
            this.closeViewModal()
            this.loadData()
          } catch (error) {
            console.error('Error deleting asset:', error)
            toast.error('Failed to delete asset')
          }
        }
      )
    },
    statusBadgeClass(status) {
      const map = {
        active: 'badge-green',
        available: 'badge-blue',
        maintenance: 'badge-amber',
        retired: 'badge-gray',
        lost: 'badge-red'
      }
      return map[status] || 'badge-gray'
    },
    formatCurrency(value) {
      if (!value) return 'R 0.00'
      return 'R ' + parseFloat(value).toLocaleString('en-ZA', { minimumFractionDigits: 2, maximumFractionDigits: 2 })
    },
    formatDate(date) {
      if (!date) return '-'
      return new Date(date).toLocaleDateString('en-ZA', { year: 'numeric', month: 'short', day: 'numeric' })
    }
  }
}
</script>

<style scoped>
.assets-page { padding: 2rem; }
.page-header { display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 2rem; }
.page-header h1 { font-size: 1.75rem; font-weight: 700; color: var(--gray-900); margin: 0 0 0.25rem 0; }
.page-subtitle { color: var(--gray-600); font-size: 0.9375rem; margin: 0; }
.header-actions { display: flex; gap: 0.75rem; align-items: center; }
.filter-select { padding: 0.5rem 2rem 0.5rem 0.75rem; border: 1px solid var(--border-color); border-radius: var(--radius-md); background: white; font-size: 0.875rem; }

.stats-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 1rem; margin-bottom: 2rem; }
.stat-card { background: white; border: 1px solid var(--border-color); border-radius: var(--radius-lg); padding: 1.25rem; display: flex; gap: 1rem; align-items: center; }
.stat-icon { width: 48px; height: 48px; border-radius: var(--radius-md); display: flex; align-items: center; justify-content: center; flex-shrink: 0; }
.stat-content { flex: 1; }
.stat-value { font-size: 1.5rem; font-weight: 700; color: var(--gray-900); }
.stat-label { font-size: 0.8125rem; color: var(--gray-600); margin-top: 0.125rem; }

.assets-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(320px, 1fr)); gap: 1rem; }
.asset-card { background: white; border: 1px solid var(--border-color); border-radius: var(--radius-lg); padding: 1.25rem; cursor: pointer; transition: box-shadow 0.2s, border-color 0.2s; }
.asset-card:hover { box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08); border-color: var(--primary-300); }
.asset-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.75rem; }
.asset-tag { font-size: 0.75rem; font-weight: 600; color: var(--gray-500); background: var(--gray-100); padding: 0.25rem 0.5rem; border-radius: var(--radius-sm); }
.asset-name { font-size: 1.125rem; font-weight: 600; color: var(--gray-900); margin: 0 0 0.75rem 0; }
.asset-meta { display: flex; flex-direction: column; gap: 0.5rem; margin-bottom: 0.75rem; }
.meta-item { display: flex; align-items: center; gap: 0.5rem; font-size: 0.8125rem; color: var(--gray-600); }
.meta-item svg { flex-shrink: 0; }
.asset-footer { display: flex; justify-content: space-between; align-items: center; padding-top: 0.75rem; border-top: 1px solid var(--border-color); }
.asset-value { font-size: 1rem; font-weight: 600; color: var(--primary-600); }
.asset-condition { display: flex; align-items: center; gap: 0.375rem; font-size: 0.75rem; color: var(--gray-600); }
.condition-dot { width: 8px; height: 8px; border-radius: 50%; }
.condition-excellent { background: #10b981; }
.condition-good { background: #3b82f6; }
.condition-fair { background: #f59e0b; }
.condition-poor { background: #ef4444; }
.condition-damaged { background: #dc2626; }

.spinner-container { text-align: center; padding: 4rem 2rem; }
.empty-state { text-align: center; padding: 4rem 2rem; }
.empty-state svg { margin-bottom: 1rem; }
.empty-state h3 { font-size: 1.25rem; font-weight: 600; color: var(--gray-700); margin: 0 0 0.5rem 0; }
.empty-state p { color: var(--gray-500); margin: 0 0 1.5rem 0; }

.modal-overlay { position: fixed; top: 0; left: 0; right: 0; bottom: 0; background: rgba(0, 0, 0, 0.5); display: flex; align-items: center; justify-content: center; z-index: 9999; padding: 1rem; }
.modal-panel { background: white; border-radius: var(--radius-lg); max-width: 600px; width: 100%; max-height: 90vh; overflow: auto; }
.modal-lg { max-width: 800px; }
.modal-header { padding: 1.25rem 1.5rem; border-bottom: 1px solid var(--border-color); display: flex; justify-content: space-between; align-items: center; }
.modal-header h3 { margin: 0; font-size: 1.25rem; font-weight: 600; }
.modal-close { background: none; border: none; font-size: 1.5rem; color: var(--gray-400); cursor: pointer; line-height: 1; padding: 0; width: 32px; height: 32px; display: flex; align-items: center; justify-content: center; }
.modal-close:hover { color: var(--gray-600); }
.modal-body { padding: 1.5rem; }
.modal-actions { display: flex; gap: 0.75rem; justify-content: flex-end; margin-top: 1.5rem; }

.form-section { margin-bottom: 1.5rem; padding-bottom: 1.5rem; border-bottom: 1px solid var(--border-color); }
.form-section:last-of-type { border-bottom: none; margin-bottom: 0; }
.section-title { font-size: 1rem; font-weight: 600; color: var(--gray-800); margin: 0 0 1rem 0; }
.form-grid-2 { display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; }
.form-group { margin-bottom: 1rem; }
.form-group label { display: block; font-size: 0.875rem; font-weight: 500; color: var(--gray-700); margin-bottom: 0.375rem; }
.required { color: var(--red-500); }
.form-group input, .form-group select, .form-group textarea { width: 100%; padding: 0.625rem 0.75rem; border: 1px solid var(--border-color); border-radius: var(--radius-md); font-size: 0.875rem; }
.form-group textarea { resize: vertical; font-family: inherit; }

.detail-section { margin-bottom: 1.5rem; }
.detail-section h4 { font-size: 1rem; font-weight: 600; color: var(--gray-800); margin: 0 0 0.75rem 0; }
.detail-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 0.75rem; }
.detail-item { display: flex; justify-content: space-between; padding: 0.5rem 0; border-bottom: 1px solid var(--border-color); }
.detail-item .label { font-size: 0.8125rem; color: var(--gray-600); font-weight: 500; }
.detail-item .value { font-size: 0.8125rem; color: var(--gray-900); text-align: right; }

@media (max-width: 768px) {
  .page-header { flex-direction: column; gap: 1rem; }
  .header-actions { width: 100%; justify-content: stretch; }
  .filter-select { flex: 1; }
  .stats-grid { grid-template-columns: 1fr; }
  .assets-grid { grid-template-columns: 1fr; }
  .form-grid-2 { grid-template-columns: 1fr; }
  .detail-grid { grid-template-columns: 1fr; }
}
</style>

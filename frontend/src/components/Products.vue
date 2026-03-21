<template>
  <div class="page-wrap">
    <div class="page-header">
      <div>
        <h1>Product Catalog</h1>
        <p class="page-subtitle">Manage your products &amp; services for deals and quotes</p>
      </div>
      <button class="btn btn-primary" @click="openAdd">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/></svg>
        Add Product
      </button>
    </div>

    <div class="stats-row">
      <div class="stat-card">
        <div class="stat-value">{{ products.length }}</div>
        <div class="stat-label">Total Products</div>
      </div>
      <div class="stat-card">
        <div class="stat-value">{{ activeCount }}</div>
        <div class="stat-label">Active</div>
      </div>
      <div class="stat-card">
        <div class="stat-value">{{ categories.length }}</div>
        <div class="stat-label">Categories</div>
      </div>
      <div class="stat-card">
        <div class="stat-value">R{{ formatNumber(totalValue) }}</div>
        <div class="stat-label">Total Value</div>
      </div>
    </div>

    <div class="filter-bar">
      <input v-model="search" placeholder="Search products..." class="form-input search-input" />
      <select v-model="filterCategory" class="form-input filter-select">
        <option value="">All Categories</option>
        <option v-for="cat in categories" :key="cat" :value="cat">{{ cat }}</option>
      </select>
      <select v-model="filterStatus" class="form-input filter-select">
        <option value="">All Status</option>
        <option value="active">Active</option>
        <option value="inactive">Inactive</option>
      </select>
    </div>

    <div class="table-wrap" v-if="!loading">
      <table class="data-table">
        <thead>
          <tr>
            <th>Product</th>
            <th>SKU</th>
            <th>Category</th>
            <th>Price (excl)</th>
            <th>Price (incl)</th>
            <th>Margin</th>
            <th>Status</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="product in filteredProducts" :key="product.id">
            <td>
              <div class="product-name">{{ product.name }}</div>
              <div class="product-desc">{{ product.description || '—' }}</div>
            </td>
            <td><code>{{ product.sku || '—' }}</code></td>
            <td><span class="badge badge-blue">{{ product.category || 'Uncategorized' }}</span></td>
            <td class="text-right">R{{ formatNumber(product.price) }}</td>
            <td class="text-right">R{{ formatNumber(product.price_incl_tax) }}</td>
            <td class="text-right">
              <span v-if="product.margin !== null" :class="['badge', product.margin >= 30 ? 'badge-green' : product.margin >= 15 ? 'badge-yellow' : 'badge-red']">
                {{ product.margin.toFixed(1) }}%
              </span>
              <span v-else class="text-muted">—</span>
            </td>
            <td>
              <span :class="['badge', product.is_active ? 'badge-green' : 'badge-red']">
                {{ product.is_active ? 'Active' : 'Inactive' }}
              </span>
            </td>
            <td>
              <div class="action-btns">
                <button class="btn btn-sm btn-secondary" @click="editProduct(product)">Edit</button>
                <button class="btn btn-sm btn-danger" @click="deleteProduct(product)">Delete</button>
              </div>
            </td>
          </tr>
          <tr v-if="filteredProducts.length === 0">
            <td colspan="8" class="text-center text-muted">No products found</td>
          </tr>
        </tbody>
      </table>
    </div>

    <div v-else class="loading-state">
      <div class="spinner"></div>
      <p>Loading products...</p>
    </div>

    <div v-if="showModal" class="modal-overlay" @click="closeModal">
      <div class="modal-panel modal-lg" @click.stop>
        <div class="modal-header">
          <h3>{{ isEditing ? 'Edit Product' : 'Add New Product' }}</h3>
          <button class="modal-close" @click="closeModal">&times;</button>
        </div>
        <div class="modal-body">
          <form @submit.prevent="saveProduct">
            <div class="form-row">
              <div class="form-group flex-2">
                <label class="form-label">Product Name *</label>
                <input class="form-input" v-model="form.name" required placeholder="e.g. Premium CRM Licence">
              </div>
              <div class="form-group flex-1">
                <label class="form-label">SKU</label>
                <input class="form-input" v-model="form.sku" placeholder="e.g. CRM-PRO-001">
              </div>
            </div>
            <div class="form-group">
              <label class="form-label">Description</label>
              <textarea class="form-input" v-model="form.description" rows="2" placeholder="Product description..."></textarea>
            </div>
            <div class="form-row">
              <div class="form-group flex-1">
                <label class="form-label">Category</label>
                <input class="form-input" v-model="form.category" placeholder="e.g. Software, Service" list="categories-list">
                <datalist id="categories-list">
                  <option v-for="cat in categories" :key="cat" :value="cat" />
                </datalist>
              </div>
              <div class="form-group flex-1">
                <label class="form-label">Unit</label>
                <select class="form-input" v-model="form.unit">
                  <option value="each">Each</option>
                  <option value="hour">Hour</option>
                  <option value="month">Month</option>
                  <option value="licence">Licence</option>
                  <option value="project">Project</option>
                </select>
              </div>
            </div>
            <div class="form-row">
              <div class="form-group flex-1">
                <label class="form-label">Price (excl. VAT) *</label>
                <input class="form-input" v-model="form.price" type="number" step="0.01" min="0" required>
              </div>
              <div class="form-group flex-1">
                <label class="form-label">VAT Rate (%)</label>
                <input class="form-input" v-model="form.tax_rate" type="number" step="0.01" min="0" max="100">
              </div>
              <div class="form-group flex-1">
                <label class="form-label">Price (incl. VAT)</label>
                <input class="form-input" :value="calculatedPriceInclVat" disabled style="background: rgba(255, 255, 255, 0.05); color: #D4AF37; border-color: rgba(212, 175, 55, 0.3); cursor: not-allowed;">
              </div>
              <div class="form-group flex-1">
                <label class="form-label">Cost Price</label>
                <input class="form-input" v-model="form.cost" type="number" step="0.01" min="0" placeholder="For margin calc">
              </div>
            </div>
            <div class="form-group">
              <label class="form-label checkbox-label">
                <input type="checkbox" v-model="form.is_active"> Active (available for selection in deals)
              </label>
            </div>
            <div class="form-actions">
              <button type="button" class="btn btn-secondary" @click="closeModal">Cancel</button>
              <button type="submit" class="btn btn-primary" :disabled="saving">
                {{ saving ? 'Saving...' : (isEditing ? 'Update Product' : 'Add Product') }}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { productsAPI } from '../api'
import toast from '../utils/toast'

export default {
  name: 'Products',
  data() {
    return {
      products: [],
      loading: true,
      saving: false,
      showModal: false,
      isEditing: false,
      editId: null,
      search: '',
      filterCategory: '',
      filterStatus: '',
      form: this.emptyForm()
    }
  },
  computed: {
    activeCount() {
      return this.products.filter(p => p.is_active).length
    },
    categories() {
      return [...new Set(this.products.map(p => p.category).filter(Boolean))].sort()
    },
    totalValue() {
      if (!this.filteredProducts.length) return 0
      return this.filteredProducts.reduce((sum, p) => sum + parseFloat(p.price || 0), 0)
    },
    calculatedPriceInclVat() {
      const price = parseFloat(this.form.price) || 0;
      const tax = parseFloat(this.form.tax_rate) || 0;
      return (price * (1 + tax / 100)).toFixed(2);
    },
    filteredProducts() {
      return this.products.filter(p => {
        const matchSearch = !this.search ||
          p.name.toLowerCase().includes(this.search.toLowerCase()) ||
          (p.sku && p.sku.toLowerCase().includes(this.search.toLowerCase())) ||
          (p.description && p.description.toLowerCase().includes(this.search.toLowerCase()))
        const matchCategory = !this.filterCategory || p.category === this.filterCategory
        const matchStatus = !this.filterStatus ||
          (this.filterStatus === 'active' && p.is_active) ||
          (this.filterStatus === 'inactive' && !p.is_active)
        return matchSearch && matchCategory && matchStatus
      })
    }
  },
  mounted() {
    this.fetchProducts()
  },
  methods: {
    emptyForm() {
      return {
        name: '', description: '', sku: '', price: '', cost: '',
        tax_rate: 15, category: '', unit: 'each', is_active: true
      }
    },
    formatNumber(n) {
      return parseFloat(n || 0).toLocaleString('en-ZA', { minimumFractionDigits: 2, maximumFractionDigits: 2 })
    },
    async fetchProducts() {
      this.loading = true
      try {
        const res = await productsAPI.getAll()
        this.products = (res.data.results || res.data || []).map(p => ({
          ...p,
          price_incl_tax: parseFloat(p.price) * (1 + parseFloat(p.tax_rate) / 100),
          margin: p.cost ? ((parseFloat(p.price) - parseFloat(p.cost)) / parseFloat(p.price) * 100) : null
        }))
      } catch (e) {
        toast.error('Failed to load products')
      } finally {
        this.loading = false
      }
    },
    openAdd() {
      this.form = this.emptyForm()
      this.isEditing = false
      this.editId = null
      this.showModal = true
    },
    editProduct(product) {
      this.form = {
        name: product.name,
        description: product.description || '',
        sku: product.sku || '',
        price: product.price,
        cost: product.cost || '',
        tax_rate: product.tax_rate,
        category: product.category || '',
        unit: product.unit || 'each',
        is_active: product.is_active
      }
      this.isEditing = true
      this.editId = product.id
      this.showModal = true
    },
    closeModal() {
      this.showModal = false
      this.isEditing = false
      this.editId = null
    },
    async saveProduct() {
      this.saving = true
      try {
        const payload = { ...this.form }
        if (!payload.cost) delete payload.cost
        if (this.isEditing) {
          await productsAPI.update(this.editId, payload)
          toast.success('Product updated')
        } else {
          await productsAPI.create(payload)
          toast.success('Product created')
        }
        this.closeModal()
        this.fetchProducts()
      } catch (e) {
        toast.error(e.message || 'Failed to save product')
      } finally {
        this.saving = false
      }
    },
    async deleteProduct(product) {
      if (!confirm(`Delete "${product.name}"? This cannot be undone.`)) return
      try {
        await productsAPI.delete(product.id)
        toast.success('Product deleted')
        this.fetchProducts()
      } catch (e) {
        toast.error(e.message || 'Failed to delete product')
      }
    }
  }
}
</script>

<style scoped>
.page-wrap { padding: 24px; max-width: 1400px; margin: 0 auto; }
.page-header { display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 24px; flex-wrap: wrap; gap: 12px; }
.page-header h1 { font-size: 24px; font-weight: 700; color: #fff; margin: 0; }
.page-subtitle { color: #9ca3af; font-size: 14px; margin-top: 4px; }

.stats-row { display: grid; grid-template-columns: repeat(auto-fit, minmax(160px, 1fr)); gap: 16px; margin-bottom: 24px; }
.stat-card { background: rgba(17, 20, 24, 0.85); border: 1px solid rgba(212, 175, 55, 0.2); border-radius: 12px; padding: 20px; text-align: center; box-shadow: 0 4px 6px rgba(0,0,0,0.3); transition: all 0.3s; }
.stat-card:hover { transform: translateY(-2px); border-color: rgba(212, 175, 55, 0.5); box-shadow: 0 10px 25px rgba(0,0,0,0.5), inset 0 0 15px rgba(212,175,55,0.05); }
.stat-value { font-size: 28px; font-weight: 700; color: #D4AF37; }
.stat-label { font-size: 12px; color: #9ca3af; text-transform: uppercase; letter-spacing: 0.05em; margin-top: 4px; }

.filter-bar { display: flex; gap: 12px; margin-bottom: 20px; flex-wrap: wrap; }
.search-input { flex: 1; min-width: 200px; }
.filter-select { width: 180px; }

.table-wrap { overflow-x: auto; background: rgba(17, 20, 24, 0.85); border: 1px solid rgba(212, 175, 55, 0.2); border-radius: 12px; box-shadow: 0 10px 25px rgba(0,0,0,0.5); }
.data-table { width: 100%; border-collapse: collapse; }
.data-table th { text-align: left; padding: 12px 16px; font-size: 11px; text-transform: uppercase; letter-spacing: 0.05em; color: #9ca3af; border-bottom: 2px solid rgba(212, 175, 55, 0.2); background: rgba(0,0,0,0.2); }
.data-table td { padding: 12px 16px; border-bottom: 1px solid rgba(255,255,255,0.05); font-size: 14px; color: #fff; }
.data-table tr:last-child td { border-bottom: none; }
.data-table tr:hover { background: rgba(212, 175, 55, 0.05); }

.product-name { font-weight: 600; color: #fff; }
.product-desc { font-size: 12px; color: #9ca3af; max-width: 250px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.text-right { text-align: right; }
.text-center { text-align: center; }
.text-muted { color: #6b7280; }

.action-btns { display: flex; gap: 6px; }

.badge { display: inline-block; padding: 2px 10px; border-radius: 20px; font-size: 11px; font-weight: 600; }
.badge-green { background: rgba(34, 197, 94, 0.15); color: #4ade80; border: 1px solid rgba(34, 197, 94, 0.3); }
.badge-yellow { background: rgba(245, 158, 11, 0.15); color: #fbbf24; border: 1px solid rgba(245, 158, 11, 0.3); }
.badge-red { background: rgba(239, 68, 68, 0.15); color: #f87171; border: 1px solid rgba(239, 68, 68, 0.3); }
.badge-blue { background: rgba(212, 175, 55, 0.15); color: #D4AF37; border: 1px solid rgba(212, 175, 55, 0.3); }
.badge-gray { background: rgba(255, 255, 255, 0.05); color: #d1d5db; border: 1px solid rgba(255, 255, 255, 0.1); }

code { background: rgba(0,0,0,0.3); color: #D4AF37; padding: 2px 6px; border-radius: 4px; font-size: 12px; border: 1px solid rgba(212,175,55,0.2); }

.btn { display: inline-flex; align-items: center; gap: 6px; padding: 8px 16px; border-radius: 8px; font-size: 14px; font-weight: 600; cursor: pointer; border: none; transition: all 0.2s; text-transform: uppercase; letter-spacing: 0.5px; }
.btn-primary { background: linear-gradient(135deg, #D4AF37, #B49015); color: #000; box-shadow: 0 4px 10px rgba(212,175,55,0.3); }
.btn-primary:hover { transform: translateY(-2px); box-shadow: 0 6px 15px rgba(212,175,55,0.4); }
.btn-secondary { background: transparent; color: #fff; border: 1px solid rgba(255,255,255,0.2); }
.btn-secondary:hover { border-color: #D4AF37; color: #D4AF37; }
.btn-danger { background: rgba(239, 68, 68, 0.1); color: #ef4444; border: 1px solid rgba(239, 68, 68, 0.3); }
.btn-danger:hover { background: rgba(239, 68, 68, 0.2); }
.btn-sm { padding: 4px 10px; font-size: 12px; }

.modal-overlay { position: fixed; inset: 0; background: rgba(0,0,0,0.5); display: flex; align-items: center; justify-content: center; z-index: 1000; }
.modal-panel { background: rgba(17, 20, 24, 0.95); backdrop-filter: blur(10px); border: 1px solid rgba(212, 175, 55, 0.3); box-shadow: 0 25px 50px -12px rgba(0,0,0,0.8); border-radius: 16px; width: 95%; max-width: 640px; max-height: 90vh; overflow-y: auto; color: #fff; }
.modal-lg { max-width: 700px; }
.modal-header { display: flex; justify-content: space-between; align-items: center; padding: 20px 24px; border-bottom: 1px solid rgba(255,255,255,0.1); }
.modal-header h3 { font-size: 18px; font-weight: 600; margin: 0; color: #fff; }
.modal-close { background: none; border: none; font-size: 24px; cursor: pointer; color: #9ca3af; transition: color 0.2s; }
.modal-close:hover { color: #fff; }
.modal-body { padding: 24px; }

.form-group { margin-bottom: 16px; }
.form-label { display: block; font-size: 13px; font-weight: 600; color: #d1d5db; margin-bottom: 6px; }
.form-input { width: 100%; padding: 10px 12px; border: 1px solid rgba(255,255,255,0.1); border-radius: 8px; font-size: 14px; background: rgba(0,0,0,0.2); color: #fff; transition: all 0.2s; }
.form-input:focus { outline: none; border-color: #D4AF37; box-shadow: 0 0 0 3px rgba(212,175,55,0.2); }

.form-row { display: flex; gap: 16px; }
.form-row .form-group { flex: 1; }
.flex-1 { flex: 1; }
.flex-2 { flex: 2; }

.form-actions { display: flex; justify-content: flex-end; gap: 12px; margin-top: 24px; padding-top: 16px; border-top: 1px solid rgba(255,255,255,0.1); }

.checkbox-label { display: flex; align-items: center; gap: 8px; cursor: pointer; }
.checkbox-label input[type="checkbox"] { width: 16px; height: 16px; accent-color: #D4AF37; }

.loading-state { display: flex; flex-direction: column; align-items: center; padding: 60px; color: var(--gray-500); }
.spinner { width: 32px; height: 32px; border: 3px solid rgba(255,255,255,0.1); border-top-color: #D4AF37; border-radius: 50%; animation: spin 0.8s linear infinite; }
@keyframes spin { to { transform: rotate(360deg); } }

@media (max-width: 768px) {
  .form-row { flex-direction: column; gap: 0; }
  .stats-row { grid-template-columns: repeat(2, 1fr); }
  .filter-bar { flex-direction: column; }
  .filter-select { width: 100%; }
}
</style>

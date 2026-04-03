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
      <select v-if="isAdmin" v-model="filterCompany" class="form-input filter-select">
        <option value="">All Companies</option>
        <option v-for="comp in companies" :key="comp" :value="comp">{{ comp }}</option>
      </select>
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

    <div v-if="isAdmin" class="catalog-switcher">
      <button class="switch-btn" :class="{ active: catalogView === 'all' }" @click="catalogView = 'all'">All</button>
      <button class="switch-btn" :class="{ active: catalogView === 'master' }" @click="catalogView = 'master'">MTAMBO Holdings</button>
      <button class="switch-btn" :class="{ active: catalogView === 'company' }" @click="catalogView = 'company'">Company Products</button>
    </div>

    <div v-if="!loading" class="catalog-container">
      <template v-if="filteredProducts.length > 0">
        <div v-if="isAdmin && catalogView === 'all'" class="split-catalog">
          <section class="catalog-section">
            <div class="section-header">
              <h2>MTAMBO Holdings</h2>
              <span class="badge badge-gray">{{ masterProducts.length }} items</span>
            </div>
            <div v-if="masterProducts.length > 0" class="product-grid">
              <article v-for="product in masterProducts" :key="product.id" :class="['product-card', getMarginClass(product)]">
                <div class="card-header">
                  <div class="header-main">
                    <div class="product-name">{{ product.name }}</div>
                    <div class="product-sku">{{ product.sku || 'No SKU' }}</div>
                  </div>
                  <div class="header-badges">
                    <span class="badge badge-blue">{{ product.category || 'Uncategorized' }}</span>
                    <span :class="['badge', product.is_active ? 'badge-green' : 'badge-red']">
                      {{ product.is_active ? 'Active' : 'Inactive' }}
                    </span>
                  </div>
                </div>
                <div class="card-body">
                  <div class="product-desc">{{ product.description || 'No description provided.' }}</div>
                  <div class="product-metrics">
                    <div class="metric">
                      <span class="metric-lbl">Price excl</span>
                      <span class="metric-val text-gold">R{{ formatNumber(product.price) }}</span>
                    </div>
                    <div class="metric">
                      <span class="metric-lbl">Price incl</span>
                      <span class="metric-val text-blue">R{{ formatNumber(product.price_incl_tax) }}</span>
                    </div>
                    <div class="metric">
                      <span class="metric-lbl">Margin</span>
                      <span v-if="product.margin !== null" class="metric-val" :class="product.margin >= 30 ? 'text-gold' : product.margin >= 15 ? 'text-blue' : 'text-red'">{{ product.margin.toFixed(1) }}%</span>
                      <span v-else class="metric-val text-muted">—</span>
                    </div>
                  </div>
                </div>
                <div class="card-footer">
                  <div class="audit-trail">
                    <div class="audit-avatar">{{ (product.created_by_name || 'S').charAt(0).toUpperCase() }}</div>
                    <div class="audit-info">
                      <div class="audit-name">{{ product.created_by_name || 'System' }}</div>
                      <div class="audit-date">{{ formatDate(product.created_at) }}</div>
                    </div>
                    <div class="audit-company">{{ product.company_name || 'MTAMBO HOLDINGS' }}</div>
                  </div>
                  <div class="action-btns">
                    <button class="btn-icon" @click="editProduct(product)" title="Edit">✎</button>
                    <button class="btn-icon danger" @click="deleteProduct(product)" title="Delete">×</button>
                  </div>
                </div>
              </article>
            </div>
            <div v-else class="empty-state">No MTAMBO Holdings products match the current filters.</div>
          </section>

          <section class="catalog-section">
            <div class="section-header">
              <h2>Company Products</h2>
              <span class="badge badge-gray">{{ tenantProducts.length }} items</span>
            </div>
            <div v-if="tenantProducts.length > 0" class="product-grid">
              <article v-for="product in tenantProducts" :key="product.id" :class="['product-card', getMarginClass(product)]">
                <div class="card-header">
                  <div class="header-main">
                    <div class="product-name">{{ product.name }}</div>
                    <div class="product-sku">{{ product.sku || 'No SKU' }}</div>
                  </div>
                  <div class="header-badges">
                    <span class="badge badge-blue">{{ product.category || 'Uncategorized' }}</span>
                    <span :class="['badge', product.is_active ? 'badge-green' : 'badge-red']">
                      {{ product.is_active ? 'Active' : 'Inactive' }}
                    </span>
                  </div>
                </div>
                <div class="card-body">
                  <div class="product-desc">{{ product.description || 'No description provided.' }}</div>
                  <div class="product-metrics">
                    <div class="metric">
                      <span class="metric-lbl">Price excl</span>
                      <span class="metric-val text-gold">R{{ formatNumber(product.price) }}</span>
                    </div>
                    <div class="metric">
                      <span class="metric-lbl">Price incl</span>
                      <span class="metric-val text-blue">R{{ formatNumber(product.price_incl_tax) }}</span>
                    </div>
                    <div class="metric">
                      <span class="metric-lbl">Margin</span>
                      <span v-if="product.margin !== null" class="metric-val" :class="product.margin >= 30 ? 'text-gold' : product.margin >= 15 ? 'text-blue' : 'text-red'">{{ product.margin.toFixed(1) }}%</span>
                      <span v-else class="metric-val text-muted">—</span>
                    </div>
                  </div>
                </div>
                <div class="card-footer">
                  <div class="audit-trail">
                    <div class="audit-avatar">{{ (product.created_by_name || 'S').charAt(0).toUpperCase() }}</div>
                    <div class="audit-info">
                      <div class="audit-name">{{ product.created_by_name || 'System' }}</div>
                      <div class="audit-date">{{ formatDate(product.created_at) }}</div>
                    </div>
                    <div class="audit-company">{{ product.company_name || 'Other Company' }}</div>
                  </div>
                  <div class="action-btns">
                    <button class="btn-icon" @click="editProduct(product)" title="Edit">✎</button>
                    <button class="btn-icon danger" @click="deleteProduct(product)" title="Delete">×</button>
                  </div>
                </div>
              </article>
            </div>
            <div v-else class="empty-state">No company products match the current filters.</div>
          </section>
        </div>

        <div v-else-if="isAdmin && catalogView === 'master'" class="split-catalog">
          <section class="catalog-section">
            <div class="section-header">
              <h2>MTAMBO Holdings</h2>
              <span class="badge badge-gray">{{ masterProducts.length }} items</span>
            </div>
            <div v-if="masterProducts.length > 0" class="product-grid">
              <article v-for="product in masterProducts" :key="product.id" :class="['product-card', getMarginClass(product)]">
                <div class="card-header">
                  <div class="header-main">
                    <div class="product-name">{{ product.name }}</div>
                    <div class="product-sku">{{ product.sku || 'No SKU' }}</div>
                  </div>
                  <div class="header-badges">
                    <span class="badge badge-blue">{{ product.category || 'Uncategorized' }}</span>
                    <span :class="['badge', product.is_active ? 'badge-green' : 'badge-red']">{{ product.is_active ? 'Active' : 'Inactive' }}</span>
                  </div>
                </div>
                <div class="card-body">
                  <div class="product-desc">{{ product.description || 'No description provided.' }}</div>
                  <div class="product-metrics">
                    <div class="metric"><span class="metric-lbl">Price excl</span><span class="metric-val text-gold">R{{ formatNumber(product.price) }}</span></div>
                    <div class="metric"><span class="metric-lbl">Price incl</span><span class="metric-val text-blue">R{{ formatNumber(product.price_incl_tax) }}</span></div>
                    <div class="metric"><span class="metric-lbl">Margin</span><span v-if="product.margin !== null" class="metric-val" :class="product.margin >= 30 ? 'text-gold' : product.margin >= 15 ? 'text-blue' : 'text-red'">{{ product.margin.toFixed(1) }}%</span><span v-else class="metric-val text-muted">—</span></div>
                  </div>
                </div>
                <div class="card-footer">
                  <div class="audit-trail">
                    <div class="audit-avatar">{{ (product.created_by_name || 'S').charAt(0).toUpperCase() }}</div>
                    <div class="audit-info">
                      <div class="audit-name">{{ product.created_by_name || 'System' }}</div>
                      <div class="audit-date">{{ formatDate(product.created_at) }}</div>
                    </div>
                    <div class="audit-company">{{ product.company_name || 'MTAMBO HOLDINGS' }}</div>
                  </div>
                  <div class="action-btns">
                    <button class="btn-icon" @click="editProduct(product)" title="Edit">✎</button>
                    <button class="btn-icon danger" @click="deleteProduct(product)" title="Delete">×</button>
                  </div>
                </div>
              </article>
            </div>
            <div v-else class="empty-state">No MTAMBO Holdings products match the current filters.</div>
          </section>
        </div>

        <div v-else-if="isAdmin && catalogView === 'company'" class="split-catalog">
          <section class="catalog-section">
            <div class="section-header">
              <h2>Company Products</h2>
              <span class="badge badge-gray">{{ tenantProducts.length }} items</span>
            </div>
            <div v-if="tenantProducts.length > 0" class="product-grid">
              <article v-for="product in tenantProducts" :key="product.id" :class="['product-card', getMarginClass(product)]">
                <div class="card-header">
                  <div class="header-main">
                    <div class="product-name">{{ product.name }}</div>
                    <div class="product-sku">{{ product.sku || 'No SKU' }}</div>
                  </div>
                  <div class="header-badges">
                    <span class="badge badge-blue">{{ product.category || 'Uncategorized' }}</span>
                    <span :class="['badge', product.is_active ? 'badge-green' : 'badge-red']">{{ product.is_active ? 'Active' : 'Inactive' }}</span>
                  </div>
                </div>
                <div class="card-body">
                  <div class="product-desc">{{ product.description || 'No description provided.' }}</div>
                  <div class="product-metrics">
                    <div class="metric"><span class="metric-lbl">Price excl</span><span class="metric-val text-gold">R{{ formatNumber(product.price) }}</span></div>
                    <div class="metric"><span class="metric-lbl">Price incl</span><span class="metric-val text-blue">R{{ formatNumber(product.price_incl_tax) }}</span></div>
                    <div class="metric"><span class="metric-lbl">Margin</span><span v-if="product.margin !== null" class="metric-val" :class="product.margin >= 30 ? 'text-gold' : product.margin >= 15 ? 'text-blue' : 'text-red'">{{ product.margin.toFixed(1) }}%</span><span v-else class="metric-val text-muted">—</span></div>
                  </div>
                </div>
                <div class="card-footer">
                  <div class="audit-trail">
                    <div class="audit-avatar">{{ (product.created_by_name || 'S').charAt(0).toUpperCase() }}</div>
                    <div class="audit-info">
                      <div class="audit-name">{{ product.created_by_name || 'System' }}</div>
                      <div class="audit-date">{{ formatDate(product.created_at) }}</div>
                    </div>
                    <div class="audit-company">{{ product.company_name || 'Other Company' }}</div>
                  </div>
                  <div class="action-btns">
                    <button class="btn-icon" @click="editProduct(product)" title="Edit">✎</button>
                    <button class="btn-icon danger" @click="deleteProduct(product)" title="Delete">×</button>
                  </div>
                </div>
              </article>
            </div>
            <div v-else class="empty-state">No company products match the current filters.</div>
          </section>
        </div>

        <div v-else class="split-catalog">
          <section class="catalog-section">
            <div class="section-header">
              <h2>Product Library</h2>
              <span class="badge badge-gray">{{ filteredProducts.length }} items</span>
            </div>
            <div class="product-grid">
              <article v-for="product in filteredProducts" :key="product.id" :class="['product-card', getMarginClass(product)]">
                <div class="card-header">
                  <div class="header-main">
                    <div class="product-name">{{ product.name }}</div>
                    <div class="product-sku">{{ product.sku || 'No SKU' }}</div>
                  </div>
                  <div class="header-badges">
                    <span class="badge badge-blue">{{ product.category || 'Uncategorized' }}</span>
                    <span :class="['badge', product.is_active ? 'badge-green' : 'badge-red']">
                      {{ product.is_active ? 'Active' : 'Inactive' }}
                    </span>
                  </div>
                </div>
                <div class="card-body">
                  <div class="product-desc">{{ product.description || 'No description provided.' }}</div>
                  <div class="product-metrics">
                    <div class="metric">
                      <span class="metric-lbl">Price excl</span>
                      <span class="metric-val text-gold">R{{ formatNumber(product.price) }}</span>
                    </div>
                    <div class="metric">
                      <span class="metric-lbl">Price incl</span>
                      <span class="metric-val text-blue">R{{ formatNumber(product.price_incl_tax) }}</span>
                    </div>
                    <div class="metric">
                      <span class="metric-lbl">Margin</span>
                      <span v-if="product.margin !== null" class="metric-val" :class="product.margin >= 30 ? 'text-gold' : product.margin >= 15 ? 'text-blue' : 'text-red'">{{ product.margin.toFixed(1) }}%</span>
                      <span v-else class="metric-val text-muted">—</span>
                    </div>
                  </div>
                </div>
                <div class="card-footer">
                  <div class="audit-trail">
                    <div class="audit-avatar">{{ (product.created_by_name || 'S').charAt(0).toUpperCase() }}</div>
                    <div class="audit-info">
                      <div class="audit-name">{{ product.created_by_name || 'System' }}</div>
                      <div class="audit-date">{{ formatDate(product.created_at) }}</div>
                    </div>
                    <div class="audit-company">{{ product.company_name || 'MTAMBO HOLDINGS' }}</div>
                  </div>
                  <div class="action-btns">
                    <button class="btn-icon" @click="editProduct(product)" title="Edit">✎</button>
                    <button class="btn-icon danger" @click="deleteProduct(product)" title="Delete">×</button>
                  </div>
                </div>
              </article>
            </div>
          </section>
        </div>
      </template>
      <div v-else class="empty-state">No products found</div>
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
      catalogView: 'all',
      search: '',
      filterCategory: '',
      filterStatus: '',
      filterCompany: '',
      form: this.emptyForm()
    }
  },
  computed: {
    isAdmin() {
      try {
        const user = JSON.parse(localStorage.getItem('thefinisher_user') || '{}');
        return user.is_superuser || (user.username || '').toLowerCase() === 'adminluxury';
      } catch(e) { return false; }
    },
    activeCount() {
      return this.products.filter(p => p.is_active).length
    },
    categories() {
      return [...new Set(this.products.map(p => p.category).filter(Boolean))].sort()
    },
    companies() {
      return [...new Set(this.products.map(p => p.company_name).filter(Boolean))].sort()
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
        const matchCompany = !this.filterCompany || p.company_name === this.filterCompany
        return matchSearch && matchCategory && matchStatus && matchCompany
      })
    },
    masterProducts() {
      return this.filteredProducts.filter(p => !p.company_name || p.company_name.toUpperCase() === 'MTAMBO HOLDINGS')
    },
    tenantProducts() {
      return this.filteredProducts.filter(p => p.company_name && p.company_name.toUpperCase() !== 'MTAMBO HOLDINGS')
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
    formatDate(val) {
      if (!val) return '—';
      return new Date(val).toLocaleDateString('en-ZA', { day: 'numeric', month: 'short', year: 'numeric', hour: '2-digit', minute: '2-digit' })
    },
    getMarginClass(product) {
      if (product.margin === null) return 'margin-glow-none'
      if (product.margin >= 30) return 'margin-glow-high'
      if (product.margin >= 15) return 'margin-glow-mid'
      return 'margin-glow-low'
    },
    duplicateProduct(product) {
      this.form = {
        name: product.name + ' (Copy)',
        description: product.description || '',
        sku: product.sku ? product.sku + '-COPY' : '',
        price: product.price,
        cost: product.cost || '',
        tax_rate: product.tax_rate,
        category: product.category || '',
        unit: product.unit || 'each',
        is_active: product.is_active
      }
      this.isEditing = false
      this.editId = null
      this.showModal = true
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

.catalog-switcher {
  display: inline-flex;
  gap: 8px;
  padding: 6px;
  margin-bottom: 22px;
  background: rgba(0, 0, 0, 0.28);
  border: 1px solid rgba(212, 175, 55, 0.18);
  border-radius: 14px;
  flex-wrap: wrap;
}
.switch-btn {
  border: 1px solid transparent;
  background: transparent;
  color: #cbd5e1;
  padding: 8px 14px;
  border-radius: 10px;
  cursor: pointer;
  font-size: 12px;
  font-weight: 700;
  letter-spacing: 0.04em;
  text-transform: uppercase;
  transition: all 0.2s ease;
}
.switch-btn:hover {
  border-color: rgba(212, 175, 55, 0.28);
  color: #fff;
}
.switch-btn.active {
  background: rgba(212, 175, 55, 0.14);
  color: #D4AF37;
  border-color: rgba(212, 175, 55, 0.38);
}

.catalog-container { margin-top: 10px; }
.split-catalog { display: flex; flex-direction: column; gap: 40px; }
.catalog-section { margin-bottom: 20px; }
.section-header { display: flex; align-items: center; gap: 12px; margin-bottom: 20px; padding-bottom: 10px; border-bottom: 1px solid rgba(212, 175, 55, 0.2); }
.section-header h2 { font-size: 20px; font-weight: 700; color: #D4AF37; margin: 0; text-transform: uppercase; letter-spacing: 1px; }

.product-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(340px, 1fr)); gap: 20px; }
.product-card { background: rgba(15, 15, 15, 0.85); backdrop-filter: blur(10px); border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 12px; display: flex; flex-direction: column; transition: all 0.3s ease; overflow: hidden; position: relative; }
.product-card:hover { transform: translateY(-4px); }

.margin-glow-high { border-top: 3px solid #D4AF37; box-shadow: 0 4px 20px rgba(212, 175, 55, 0.15); }
.margin-glow-high:hover { box-shadow: 0 8px 30px rgba(212, 175, 55, 0.3); }
.margin-glow-mid { border-top: 3px solid #3b82f6; box-shadow: 0 4px 20px rgba(59, 130, 246, 0.15); }
.margin-glow-mid:hover { box-shadow: 0 8px 30px rgba(59, 130, 246, 0.3); }
.margin-glow-low { border-top: 3px solid #ef4444; box-shadow: 0 4px 20px rgba(239, 68, 68, 0.15); }
.margin-glow-low:hover { box-shadow: 0 8px 30px rgba(239, 68, 68, 0.3); }
.margin-glow-none { border-top: 3px solid rgba(255, 255, 255, 0.1); }

.card-header { padding: 20px; border-bottom: 1px solid rgba(255, 255, 255, 0.05); display: flex; justify-content: space-between; align-items: flex-start; gap: 15px; }
.header-main { flex: 1; min-width: 0; }
.product-name { margin: 0 0 5px 0; font-size: 16px; font-weight: 700; color: #fff; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.product-sku { background: rgba(0,0,0,0.4); color: #9ca3af; padding: 2px 6px; border-radius: 4px; font-size: 11px; border: 1px solid rgba(255,255,255,0.1); }
.header-badges { display: flex; flex-direction: column; gap: 6px; align-items: flex-end; }

.card-body { padding: 20px; flex: 1; }
.product-desc { margin: 0 0 20px 0; font-size: 13px; color: #9ca3af; line-height: 1.5; display: -webkit-box; line-clamp: 2; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden; }

.product-metrics { display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px; background: rgba(0,0,0,0.3); padding: 15px; border-radius: 8px; border: 1px solid rgba(255, 255, 255, 0.03); }
.metric { display: flex; flex-direction: column; gap: 4px; }
.metric-lbl { font-size: 10px; text-transform: uppercase; color: #6b7280; font-weight: 600; letter-spacing: 0.5px; }
.metric-val { font-size: 14px; font-weight: 700; color: #f3f4f6; }
.text-gold { color: #D4AF37 !important; }
.text-blue { color: #60a5fa !important; }
.text-red { color: #f87171 !important; }

.card-footer { padding: 15px 20px; background: rgba(0,0,0,0.4); border-top: 1px solid rgba(255, 255, 255, 0.05); display: flex; justify-content: space-between; align-items: center; gap: 15px; }
.audit-trail { display: flex; align-items: center; gap: 10px; flex: 1; min-width: 0; }
.audit-avatar { width: 32px; height: 32px; border-radius: 8px; background: linear-gradient(135deg, #1f2937, #111827); border: 1px solid rgba(255,255,255,0.1); display: flex; align-items: center; justify-content: center; font-weight: 700; font-size: 14px; color: #D4AF37; flex-shrink: 0; }
.audit-info { display: flex; flex-direction: column; }
.audit-name { font-size: 12px; font-weight: 600; color: #e5e7eb; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; max-width: 120px; }
.audit-date { font-size: 10px; color: #6b7280; margin-top: 2px; }
.audit-company { margin-left: auto; font-size: 11px; padding: 3px 8px; background: rgba(255,255,255,0.05); border-radius: 4px; color: #9ca3af; white-space: nowrap; border: 1px solid rgba(255,255,255,0.1); }

.action-btns { display: flex; gap: 6px; }
.btn-icon { background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.1); color: #fff; width: 32px; height: 32px; border-radius: 8px; display: flex; align-items: center; justify-content: center; cursor: pointer; transition: all 0.2s; font-size: 14px; }
.btn-icon:hover { background: rgba(212, 175, 55, 0.1); border-color: #D4AF37; transform: translateY(-2px); }
.btn-icon.danger:hover { background: rgba(239, 68, 68, 0.1); border-color: #ef4444; }

.empty-state { grid-column: 1 / -1; padding: 40px; text-align: center; background: rgba(0,0,0,0.2); border: 2px dashed rgba(255,255,255,0.1); border-radius: 12px; color: #9ca3af; font-size: 14px; }
.text-muted { color: #6b7280; }

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

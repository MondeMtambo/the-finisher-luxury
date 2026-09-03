<template>
  <div class="admin-master-page luxury-theme">
    <div class="page-header">
      <div class="header-title-row">
        <h1>Admin Control Deck</h1>
        <div class="live-badge"><span class="pulse-dot"></span> SYSTEM OWNER</div>
      </div>
      <div class="header-sub-row">
        <p class="page-subtitle">Orchestrate workspaces, unlock insights, and manage every client.</p>
        <div class="header-actions">
          <button class="btn btn-secondary" @click="loadAllData" :disabled="loading">
            🔄 Refresh Sync
          </button>
          <button class="btn btn-danger" @click="showQuickDeleteModal = true">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 6h18M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path></svg>
            Quick Delete User
          </button>
        </div>
      </div>
    </div>

    <div v-if="loading" class="loading-state">
      <div class="spinner"></div>
      <p>Establishing secure connection to intelligence matrix...</p>
    </div>

    <div v-else-if="error" class="error-state">
      ⚠️ {{ error }}
    </div>

    <template v-else>
      <!-- Financial & Pipeline Intelligence -->
      <div class="section-container">
        <h2 class="section-title">Revenue & Pipeline Oversight</h2>
        <div class="kpi-grid">
          <div class="kpi-card">
            <div class="kpi-val">{{ overview.analytics.total_deals || 0 }}</div>
            <div class="kpi-lbl">Total Deals</div>
          </div>
          <div class="kpi-card">
            <div class="kpi-val text-blue">{{ overview.analytics.active_deals || 0 }}</div>
            <div class="kpi-lbl">Active Pipeline</div>
          </div>
          <div class="kpi-card">
            <div class="kpi-val text-amber">{{ formatCurrency(overview.analytics.pipeline_value) }}</div>
            <div class="kpi-lbl">Pipeline Value</div>
          </div>
          <div class="kpi-card">
            <div class="kpi-val text-green">{{ formatCurrency(overview.analytics.won_value) }}</div>
            <div class="kpi-lbl">Closed Won</div>
          </div>
        </div>
      </div>

      <!-- User Management (Fleet Command) -->
      <div class="section-container">
        <h2 class="section-title">Fleet Command & User Access</h2>
        <div class="kpi-grid six-cols">
          <div class="kpi-card mini"><div class="kpi-val-mini">{{ userSummary.total_users }}</div><div class="kpi-lbl-mini">Total Users</div></div>
          <div class="kpi-card mini"><div class="kpi-val-mini text-green">{{ userSummary.active_users }}</div><div class="kpi-lbl-mini">Active</div></div>
          <div class="kpi-card mini"><div class="kpi-val-mini text-blue">{{ userSummary.trial_users }}</div><div class="kpi-lbl-mini">Trial</div></div>
          <div class="kpi-card mini"><div class="kpi-val-mini text-amber">{{ userSummary.paid_users }}</div><div class="kpi-lbl-mini">Paid</div></div>
          <div class="kpi-card mini"><div class="kpi-val-mini text-yellow">{{ userSummary.overdue_users }}</div><div class="kpi-lbl-mini">Overdue</div></div>
          <div class="kpi-card mini"><div class="kpi-val-mini text-red">{{ userSummary.banned_users }}</div><div class="kpi-lbl-mini">Banned</div></div>
        </div>

        <div class="table-container">
          <table class="luxury-table">
            <thead>
              <tr>
                <th>User</th>
                <th>Email</th>
                <th>Joined</th>
                <th>Reg IP / Login IP</th>
                <th>Payment</th>
                <th>Status</th>
                <th>Activity</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="u in users" :key="u.id" :class="{ 'row-banned': u.is_banned, 'row-warn': u.warning }">
                <td>
                  <div class="user-main">{{ u.full_name }}</div>
                  <div class="user-sub">@{{ u.username }}</div>
                  <span v-if="u.is_superuser" class="badge badge-primary">ADMIN</span>
                  <span v-if="u.is_staff && !u.is_superuser" class="badge badge-gray">STAFF</span>
                  <span v-if="u.warning" class="badge badge-danger ml-1">{{ u.warning.type === 're_registration' ? 'RE-REG' : 'DUP IP' }}</span>
                </td>
                <td>{{ u.email }}<br/><span class="text-muted">{{ u.company_name || 'No Company' }}</span></td>
                <td class="date-cell">{{ formatDate(u.date_joined) }}</td>
                <td class="ip-cell">
                  <code class="d-block">{{ u.registration_ip || '—' }} (Reg)</code>
                  <code class="d-block mt-1">{{ u.last_login_ip || '—' }} (Login)</code>
                </td>
                <td>
                  <span class="badge" :class="paymentClass(u.payment_status)">{{ formatPaymentStatus(u.payment_status) }}</span>
                  <div v-if="u.payment_status === 'trial'" class="text-muted text-sm mt-1">{{ u.days_until_trial_end }}d left</div>
                </td>
                <td>
                  <span v-if="u.is_banned" class="badge badge-danger">Banned</span>
                  <span v-else-if="u.is_active" class="badge badge-success">Active</span>
                  <span v-else class="badge badge-gray">Inactive</span>
                </td>
                <td>
                  <div class="act-total">{{ u.total_activity }} items</div>
                  <div class="act-sub">{{ u.contact_count }}c · {{ u.company_count }}co · {{ u.deal_count }}d</div>
                </td>
                <td>
                  <div class="action-flex">
                    <button v-if="!u.is_banned && !u.is_superuser" @click="openBanModal(u)" class="btn-icon danger" title="Ban User">🚫</button>
                    <button v-if="u.is_banned" @click="unbanUser(u.id)" class="btn-icon success" title="Unban User">✅</button>
                    <button v-if="!u.is_superuser" @click="openPaymentModal(u)" class="btn-icon warning" title="Update Payment Status">💳</button>
                    <button v-if="!u.is_superuser && !u.is_staff" @click="triggerDelete(u)" class="btn-icon danger" title="Permanently Delete">🗑️</button>
                    <button v-if="u.warning" @click="showWarningDetails(u)" class="btn-icon warning" title="View Security Warning">⚠️</button>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- Client & Employee Roster -->
      <div class="section-container">
        <h2 class="section-title">Tenant & Employee Roster</h2>
        <div class="tenant-roster" v-for="company in clientsEmployeesData" :key="company.company_name">
           <div class="tenant-header">
               <h3>{{ company.company_name }}</h3>
               <div class="tenant-badges">
                   <span class="badge badge-gray">{{ company.total_users }} Users</span>
                   <span class="badge badge-primary">{{ company.admins }} Admins</span>
                   <span class="badge badge-success">{{ company.employees }} Emp</span>
               </div>
           </div>
           <div class="luxury-table-wrapper" style="margin-bottom: 2rem;">
               <table class="luxury-table">
                   <tbody>
                       <tr v-for="emp in company.users" :key="emp.id" :class="{'row-banned': emp.is_banned}">
                           <td style="width: 25%;">
                               <div class="user-main">{{ emp.full_name }}</div>
                               <div class="user-sub">{{ emp.email }}</div>
                           </td>
                           <td style="width: 15%;"><span class="badge badge-primary">{{ formatRole(emp.role) }}</span></td>
                           <td style="width: 25%;">
                              <div class="user-main">{{ emp.phone || 'No Phone' }}</div>
                              <div class="user-sub">{{ emp.job_title || 'No Title' }}</div>
                           </td>
                           <td style="width: 15%;">
                              <div class="user-main">{{ emp.data_counts.contacts }}c · {{ emp.data_counts.deals }}d</div>
                              <div class="user-sub">{{ emp.data_counts.tickets }} tickets</div>
                           </td>
                           <td style="width: 10%;">
                              <span v-if="emp.is_active" class="badge badge-success">Active</span>
                              <span v-else class="badge badge-gray">Inactive</span>
                           </td>
                           <td style="width: 10%;">
                              <div class="action-flex">
                                 <button class="btn-icon" @click="resetPassword(emp)" title="Force Reset Password">🔑</button>
                                 <button class="btn-icon" @click="toggleActive(emp)" title="Toggle Active Status">⚡</button>
                              </div>
                           </td>
                       </tr>
                   </tbody>
               </table>
           </div>
        </div>
      </div>

      <!-- Client Workspaces Cards -->
      <div class="section-container">
        <h2 class="section-title">Client Workspaces Directory</h2>
        <div class="client-grid">
          <div v-for="client in overview.clients" :key="client.user_id" class="client-card">
            <div class="cc-header">
              <h3>{{ client.username }}</h3>
              <span class="cc-email">{{ client.email }}</span>
            </div>
            <div class="cc-stats">
              <span class="badge badge-gray">{{ client.companies.length }} Orgs</span>
              <span class="badge badge-primary">{{ client.total_contacts }} Contacts</span>
              <span class="badge badge-success">{{ client.total_deals }} Deals</span>
            </div>
            <div class="company-list">
              <div v-for="comp in client.companies" :key="comp.id" class="comp-item">
                <div class="comp-name">{{ comp.name }}</div>
                <div class="comp-metrics text-muted">{{ comp.contact_count }}c · {{ comp.deal_count }}d · {{ formatCurrency(comp.pipeline_value) }}</div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Assist Drive Playbook -->
      <div class="section-container">
         <h2 class="section-title">Assist Drive Playbook</h2>
         <p class="text-muted mb-4">Showcase how THE FINISHER backs partner growth.</p>
         <div class="playbook-grid">
             <div class="playbook-card" v-for="item in overview.support_catalog" :key="item.name">
                 <div class="pb-header">{{ item.name }}</div>
                 <div class="pb-meta badge badge-gray mb-2">{{ item.industry }}</div>
                 <p class="pb-focus">{{ item.focus }}</p>
                 <div class="pb-next"><strong>Next Action:</strong> {{ item.next_step }}</div>
                 <button class="btn btn-secondary mt-4 w-100" @click="notifyComingSoon">Initiate Assist (Soon)</button>
             </div>
         </div>
      </div>
    </template>

    <!-- MODALS -->
    <!-- Quick Delete Modal -->
    <div v-if="showQuickDelete" class="modal-overlay" @click.self="closeQuickDelete">
        <div class="modal-panel luxury-modal">
            <div class="modal-header">
                <h3>Critical Action: Quick Delete</h3>
                <button class="modal-close" @click="closeQuickDelete">×</button>
            </div>
            <div class="modal-body">
                <p class="text-muted mb-3">Immediate action for policy violators.</p>
                <div class="form-group">
                    <label class="form-label">Search User</label>
                    <input type="text" class="form-input" v-model="quickDeleteSearch" @input="filterUsersForDelete" placeholder="Type username or email..." />
                </div>
                <div class="suggestions-list" v-if="filteredDeleteUsers.length > 0">
                    <div class="suggestion-item" v-for="u in filteredDeleteUsers.slice(0,5)" :key="u.id" @click="selectUserForQuickDelete(u)" :class="{'selected': quickDeleteUser?.id === u.id}">
                        <strong>{{ u.full_name }}</strong> (@{{ u.username }})
                        <div class="text-muted text-sm">{{ u.email }} · {{ u.total_activity }} items</div>
                    </div>
                </div>
                
                <div v-if="quickDeleteUser" class="selected-user-box mt-4">
                    <h4 class="text-danger mb-2">Confirm Deletion:</h4>
                    <p><strong>User:</strong> {{ quickDeleteUser.full_name }} (@{{ quickDeleteUser.username }})</p>
                    <p><strong>Email:</strong> {{ quickDeleteUser.email }}</p>
                    <p><strong>Activity:</strong> {{ quickDeleteUser.contact_count }}c, {{ quickDeleteUser.company_count }}co, {{ quickDeleteUser.deal_count }}d</p>
                    
                    <div class="form-group mt-3">
                        <label class="form-label">Reason (Required)</label>
                        <select class="form-input" v-model="quickDeleteReason">
                            <option value="">-- Select Reason --</option>
                            <option value="Terms of Service Violation">Terms of Service Violation</option>
                            <option value="Fraudulent Activity">Fraudulent Activity</option>
                            <option value="Payment Fraud">Payment Fraud</option>
                            <option value="Abuse of Platform">Abuse of Platform</option>
                            <option value="Other Policy Violation">Other Policy Violation</option>
                        </select>
                    </div>
                    <div class="form-group mt-2" v-if="quickDeleteReason === 'Other Policy Violation'">
                        <input type="text" class="form-input" v-model="quickDeleteCustomReason" placeholder="Specify reason..." />
                    </div>
                </div>
            </div>
            <div class="modal-footer">
                <button class="btn btn-secondary" @click="closeQuickDelete">Cancel</button>
                <button class="btn btn-danger" :disabled="!quickDeleteUser || !quickDeleteReason" @click="executeQuickDelete">Permanently Delete</button>
            </div>
        </div>
    </div>

    <!-- Ban Modal -->
    <div v-if="showBanModal" class="modal-overlay" @click.self="closeBanModal">
        <div class="modal-panel luxury-modal">
            <div class="modal-header">
                <h3>Ban User: {{ selectedUser?.full_name }}</h3>
                <button class="modal-close" @click="closeBanModal">×</button>
            </div>
            <div class="modal-body">
                <div class="form-group">
                    <label class="form-label">Reason</label>
                    <select class="form-input" v-model="banReason">
                        <option value="Unpaid subscription">Unpaid subscription</option>
                        <option value="Payment overdue">Payment overdue</option>
                        <option value="Terms of service violation">Terms of service violation</option>
                        <option value="Fraudulent activity">Fraudulent activity</option>
                        <option value="Other">Other</option>
                    </select>
                </div>
                <div class="form-group mt-2" v-if="banReason === 'Other'">
                    <label class="form-label">Custom Reason</label>
                    <input type="text" class="form-input" v-model="customBanReason" placeholder="Enter reason..." />
                </div>
            </div>
            <div class="modal-footer">
                <button class="btn btn-secondary" @click="closeBanModal">Cancel</button>
                <button class="btn btn-danger" @click="confirmBan">Confirm Ban</button>
            </div>
        </div>
    </div>

    <!-- Payment Modal -->
    <div v-if="showPaymentModal" class="modal-overlay" @click.self="closePaymentModal">
        <div class="modal-panel luxury-modal">
            <div class="modal-header">
                <h3>Update Payment: {{ selectedUser?.full_name }}</h3>
                <button class="modal-close" @click="closePaymentModal">×</button>
            </div>
            <div class="modal-body">
                <div class="form-group">
                    <label class="form-label">Payment Status</label>
                    <select class="form-input" v-model="newPaymentStatus">
                        <option value="pending">Pending Payment</option>
                        <option value="trial">Trial Period (14 days)</option>
                        <option value="paid">Paid</option>
                        <option value="overdue">Overdue</option>
                    </select>
                </div>
            </div>
            <div class="modal-footer">
                <button class="btn btn-secondary" @click="closePaymentModal">Cancel</button>
                <button class="btn btn-primary" @click="confirmPaymentUpdate">Update Status</button>
            </div>
        </div>
    </div>

    <!-- Warning Modal -->
    <div v-if="showWarningDetailsModal" class="modal-overlay" @click.self="closeWarningDetails">
        <div class="modal-panel luxury-modal">
            <div class="modal-header">
                <h3>Security Alert: {{ selectedUser?.full_name }}</h3>
                <button class="modal-close" @click="closeWarningDetails">×</button>
            </div>
            <div class="modal-body">
                <div v-if="selectedUser?.warning?.type === 're_registration'">
                    <div class="alert-box warning-box mb-3">⚠️ User Re-Registered After Deletion</div>
                    <p><strong>Previous Username:</strong> {{ selectedUser.warning.previous_username }}</p>
                    <p><strong>Reason:</strong> {{ selectedUser.warning.deleted_reason || 'Not specified' }}</p>
                    <p><strong>Message:</strong> {{ selectedUser.warning.message }}</p>
                </div>
                <div v-if="selectedUser?.warning?.type === 'duplicate_ip'">
                    <div class="alert-box danger-box mb-3">🚨 Duplicate IP Address Detected</div>
                    <p><strong>IP Address:</strong> {{ selectedUser.registration_ip }}</p>
                    <p class="mt-3"><strong>Previously Deleted Users on this IP:</strong></p>
                    <ul class="text-muted text-sm pl-4">
                        <li v-for="u in selectedUser.warning.deleted_users" :key="u.username">
                            <strong>{{ u.username }}</strong> ({{ u.email }})<br/>Reason: {{ u.deleted_reason }}
                        </li>
                    </ul>
                </div>
            </div>
            <div class="modal-footer">
                <button class="btn btn-secondary" @click="closeWarningDetails">Acknowledge</button>
            </div>
        </div>
    </div>

  </div>
</template>

<script>
export default {
  name: 'AdminConsole',
  data() {
    return {
      loading: true,
      error: '',
      overview: {
        analytics: { total_deals: 0, active_deals: 0, pipeline_value: '0', won_value: '0' },
        clients: [],
        support_catalog: []
      },
      users: [],
      userSummary: { total_users: 0, active_users: 0, banned_users: 0, trial_users: 0, paid_users: 0, overdue_users: 0 },
      loadingClientsEmployees: false,
      clientsEmployeesData: [],
      clientEmployeeStats: { total_companies: 0, total_clients: 0, total_admins: 0, total_employees: 0 },
      showBanModal: false,
      showPaymentModal: false,
      showWarningDetailsModal: false,
      showQuickDelete: false,
      selectedUser: null,
      banReason: 'Unpaid subscription',
      customBanReason: '',
      newPaymentStatus: 'paid',
      quickDeleteSearch: '',
      quickDeleteUser: null,
      quickDeleteReason: '',
      quickDeleteCustomReason: '',
      filteredDeleteUsers: []
    }
  },
  computed: {
    apiBase() {
      const isLocal = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1';
      return isLocal ? 'http://localhost:8000/api' : 'https://the-finisher-luxury-api.onrender.com/api';
    },
    token() {
      return localStorage.getItem('thefinisher_access_token');
    }
  },
  async mounted() {
    await this.loadAllData();
  },
  methods: {
    async fetchApi(endpoint, options = {}) {
      const url = `${this.apiBase}${endpoint}`;
      const headers = {
        'Authorization': `Bearer ${this.token}`,
        'Content-Type': 'application/json',
        ...options.headers
      };
      const response = await fetch(url, { ...options, headers });
      if (!response.ok) {
        const err = await response.json().catch(() => ({}));
        throw new Error(err.error || err.detail || 'API request failed');
      }
      return response.json();
    },
    async loadAllData() {
      this.loading = true;
      this.error = '';
      try {
        const [overviewRes, usersRes, ceRes] = await Promise.all([
          this.fetchApi('/admin/overview/'),
          this.fetchApi('/admin/users/'),
          this.fetchApi('/admin/clients-employees/')
        ]);
        this.overview = overviewRes;
        this.users = usersRes.users || [];
        this.userSummary = usersRes.summary || this.userSummary;
        this.clientsEmployeesData = ceRes.companies || [];
        this.clientEmployeeStats = ceRes.stats || this.clientEmployeeStats;
      } catch (err) {
        this.error = err.message;
        this.dispatchEvent('show-toast', { message: err.message, type: 'error' });
      } finally {
        this.loading = false;
      }
    },
    async actionUsers(action, payload) {
        await this.fetchApi('/admin/users/', { method: 'POST', body: JSON.stringify({ action, ...payload }) });
        await this.loadAllData();
    },
    async actionClients(action, payload) {
        const res = await this.fetchApi('/admin/clients-employees/', { method: 'POST', body: JSON.stringify({ action, ...payload }) });
        await this.loadAllData();
        return res;
    },
    // Formatting Helpers
    formatDate(dateStr) {
        if (!dateStr) return '—';
        return new Date(dateStr).toLocaleDateString('en-ZA', { year: 'numeric', month: 'short', day: 'numeric' });
    },
    formatCurrency(val) {
        return `R${Number(val || 0).toLocaleString('en-ZA', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`;
    },
    formatPaymentStatus(status) {
        const map = { pending: '⏳ Pending', paid: '✅ Paid', overdue: '⚠️ Overdue', trial: '⏱️ Trial' };
        return map[status] || status;
    },
    paymentClass(status) {
        const map = { pending: 'badge-warning', paid: 'badge-success', overdue: 'badge-danger', trial: 'badge-primary' };
        return map[status] || 'badge-gray';
    },
    formatRole(role) {
        const map = { admin: 'Admin', manager: 'Manager', supervisor: 'Supervisor', user: 'User' };
        return map[role] || role;
    },
    dispatchEvent(name, detail) {
        window.dispatchEvent(new CustomEvent(name, { detail }));
    },
    notifyComingSoon() {
        alert("This assist workflow is being finalised. Full orchestration launches soon!");
    },
    
    // User Actions
    async unbanUser(userId) {
        if(!confirm("Are you sure you want to unban this user?")) return;
        try {
            await this.actionUsers('unban', { user_id: userId });
            this.dispatchEvent('show-toast', { message: 'User unbanned successfully', type: 'success' });
        } catch(e) { this.dispatchEvent('show-toast', { message: e.message, type: 'error' }); }
    },
    async triggerDelete(user) {
        const reason = prompt(`Provide a reason for deleting ${user.username}:`);
        if(!reason) return;
        if(confirm(`WARNING: Permanently delete ${user.username}? This CANNOT be undone.`)) {
            try {
                await this.actionUsers('delete', { user_id: user.id, delete_reason: reason });
                this.dispatchEvent('show-toast', { message: 'User permanently deleted', type: 'success' });
            } catch(e) { this.dispatchEvent('show-toast', { message: e.message, type: 'error' }); }
        }
    },
    async resetPassword(user) {
        if(!confirm(`Force password reset for ${user.full_name || user.username}?`)) return;
        try {
            const res = await this.actionClients('reset_password', { user_id: user.id });
            alert(`Password reset successfully!\n\nUsername: ${res.username}\nTemporary Password: ${res.temporary_password}\n\nPlease share this with the user securely.`);
        } catch(e) { this.dispatchEvent('show-toast', { message: e.message, type: 'error' }); }
    },
    async toggleActive(user) {
        try {
            await this.actionClients('toggle_active', { user_id: user.id });
            this.dispatchEvent('show-toast', { message: 'User status toggled', type: 'success' });
        } catch(e) { this.dispatchEvent('show-toast', { message: e.message, type: 'error' }); }
    },

    // Modals
    openBanModal(user) { this.selectedUser = user; this.banReason = 'Unpaid subscription'; this.customBanReason = ''; this.showBanModal = true; },
    closeBanModal() { this.showBanModal = false; this.selectedUser = null; },
    async confirmBan() {
        const reason = this.banReason === 'Other' ? this.customBanReason : this.banReason;
        if(!reason) { alert('Reason required'); return; }
        try {
            await this.actionUsers('ban', { user_id: this.selectedUser.id, reason });
            this.dispatchEvent('show-toast', { message: 'User banned', type: 'success' });
            this.closeBanModal();
        } catch(e) { this.dispatchEvent('show-toast', { message: e.message, type: 'error' }); }
    },

    openPaymentModal(user) { this.selectedUser = user; this.newPaymentStatus = user.payment_status; this.showPaymentModal = true; },
    closePaymentModal() { this.showPaymentModal = false; this.selectedUser = null; },
    async confirmPaymentUpdate() {
        try {
            await this.actionUsers('update_payment', { user_id: this.selectedUser.id, payment_status: this.newPaymentStatus });
            this.dispatchEvent('show-toast', { message: 'Payment status updated', type: 'success' });
            this.closePaymentModal();
        } catch(e) { this.dispatchEvent('show-toast', { message: e.message, type: 'error' }); }
    },

    showWarningDetails(user) { this.selectedUser = user; this.showWarningDetailsModal = true; },
    closeWarningDetails() { this.showWarningDetailsModal = false; },

    // Quick Delete
    filterUsersForDelete() {
        const q = this.quickDeleteSearch.toLowerCase().trim();
        if(q.length < 2) { this.filteredDeleteUsers = []; return; }
        this.filteredDeleteUsers = this.users.filter(u => !u.is_superuser && (u.username.toLowerCase().includes(q) || u.email.toLowerCase().includes(q) || u.full_name.toLowerCase().includes(q)));
    },
    selectUserForQuickDelete(user) { this.quickDeleteUser = user; },
    async executeQuickDelete() {
        if(!this.quickDeleteUser || !this.quickDeleteReason) return;
        const reason = this.quickDeleteReason === 'Other Policy Violation' ? this.quickDeleteCustomReason : this.quickDeleteReason;
        if(confirm(`Permanently delete ${this.quickDeleteUser.username}?`)) {
            try {
                await this.actionUsers('delete', { user_id: this.quickDeleteUser.id, delete_reason: reason });
                this.dispatchEvent('show-toast', { message: 'User deleted via Quick Delete', type: 'success' });
                this.showQuickDelete = false;
            } catch(e) { this.dispatchEvent('show-toast', { message: e.message, type: 'error' }); }
        }
    }
  }
}
</script>

<style scoped>
.luxury-theme { color: #fff; min-height: 100vh; }
.admin-master-page { padding: 2rem; max-width: 1600px; margin: 0 auto; }
.page-header { margin-bottom: 3rem; border-bottom: 1px solid rgba(212, 175, 55, 0.2); padding-bottom: 2rem; }
.header-title-row { display: flex; align-items: center; gap: 1rem; margin-bottom: 0.5rem; }
.header-title-row h1 { font-size: 2rem; color: #D4AF37; margin: 0; font-weight: 800; letter-spacing: 1px; }
.header-sub-row { display: flex; justify-content: space-between; align-items: flex-start; }
.page-subtitle { color: #9ca3af; font-size: 1rem; margin: 0; }
.header-actions { display: flex; gap: 1rem; }
.live-badge { display: flex; align-items: center; gap: 0.5rem; background: rgba(212, 175, 55, 0.1); border: 1px solid rgba(212, 175, 55, 0.3); padding: 0.25rem 0.75rem; border-radius: 999px; color: #D4AF37; font-size: 0.75rem; font-weight: 700; letter-spacing: 1px; }
.pulse-dot { width: 8px; height: 8px; background-color: #D4AF37; border-radius: 50%; animation: pulse-animation 1.5s infinite; }
@keyframes pulse-animation { 0% { box-shadow: 0 0 0 0 rgba(212, 175, 55, 0.7); } 70% { box-shadow: 0 0 0 10px rgba(212, 175, 55, 0); } 100% { box-shadow: 0 0 0 0 rgba(212, 175, 55, 0); } }

.section-container { margin-bottom: 4rem; }
.section-header-flex { display: flex; justify-content: space-between; align-items: center; margin-bottom: 1.5rem; }
.section-title { color: #D4AF37; font-size: 1.3rem; margin-bottom: 1.5rem; text-transform: uppercase; letter-spacing: 2px; border-left: 4px solid #D4AF37; padding-left: 1rem; }
.section-title.mb-0 { margin-bottom: 0; }

.kpi-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 1.5rem; margin-bottom: 2rem; }
.kpi-grid.six-cols { grid-template-columns: repeat(6, 1fr); }
.kpi-card { background: linear-gradient(145deg, #111, #0a0a0a); border: 1px solid rgba(212, 175, 55, 0.15); border-radius: 12px; padding: 1.5rem; box-shadow: 0 8px 30px rgba(0,0,0,0.5); transition: transform 0.3s; }
.kpi-card:hover { transform: translateY(-4px); border-color: rgba(212, 175, 55, 0.4); }
.kpi-card.mini { padding: 1rem; text-align: center; }
.kpi-val { font-size: 2.2rem; font-weight: 700; color: #fff; margin-bottom: 0.5rem; }
.kpi-lbl { color: #a0aec0; font-size: 0.85rem; text-transform: uppercase; letter-spacing: 1px; }
.kpi-val-mini { font-size: 1.5rem; font-weight: 700; margin-bottom: 0.25rem; }
.kpi-lbl-mini { color: #a0aec0; font-size: 0.75rem; text-transform: uppercase; letter-spacing: 1px; }

.text-blue { color: #60a5fa !important; }
.text-amber { color: #fbbf24 !important; }
.text-green { color: #34d399 !important; }
.text-yellow { color: #facc15 !important; }
.text-red { color: #f87171 !important; }
.text-muted { color: #9ca3af !important; }

.table-container { background: rgba(10,10,10,0.6); backdrop-filter: blur(10px); border: 1px solid rgba(212,175,55,0.2); border-radius: 12px; overflow-x: auto; box-shadow: 0 10px 40px rgba(0,0,0,0.6); }
.luxury-table { width: 100%; border-collapse: collapse; text-align: left; }
.luxury-table th { background: rgba(212,175,55,0.05); padding: 1.25rem 1rem; color: #D4AF37; font-size: 0.75rem; text-transform: uppercase; letter-spacing: 1.5px; border-bottom: 1px solid rgba(212, 175, 55, 0.2); }
.luxury-table td { padding: 1.25rem 1rem; border-bottom: 1px solid rgba(255, 255, 255, 0.05); color: #d1d5db; font-size: 0.9rem; vertical-align: middle; }
.luxury-table tr:hover td { background: rgba(212, 175, 55, 0.05); }
.row-banned td { opacity: 0.5; background: rgba(239,68,68,0.05); }
.row-warn td { background: rgba(245,158,11,0.05); }

.user-main { font-weight: 600; color: #fff; margin-bottom: 0.25rem; }
.user-sub { font-size: 0.8rem; color: #9ca3af; }
.date-cell, .ip-cell { font-size: 0.85rem; color: #a0aec0; }
.act-total { font-weight: 600; color: #D4AF37; font-size: 0.95rem; }
.act-sub { font-size: 0.75rem; color: #6b7280; margin-top: 0.25rem; }

.action-flex { display: flex; gap: 0.5rem; align-items: center; }
.btn-icon { background: none; border: none; font-size: 1.2rem; cursor: pointer; transition: transform 0.2s; padding: 0.25rem; }
.btn-icon:hover { transform: scale(1.2); }
.btn-icon.danger { filter: drop-shadow(0 0 5px rgba(239,68,68,0.5)); }
.btn-icon.warning { filter: drop-shadow(0 0 5px rgba(245,158,11,0.5)); }
.btn-icon.success { filter: drop-shadow(0 0 5px rgba(16,185,129,0.5)); }

.btn { display: flex; align-items: center; justify-content: center; gap: 0.5rem; padding: 0.75rem 1.5rem; border-radius: 8px; cursor: pointer; font-weight: 600; font-size: 0.9375rem; transition: all 0.3s ease; border: none; text-transform: uppercase; letter-spacing: 1px; }
.btn-primary { background: linear-gradient(135deg, #D4AF37 0%, #AA8010 100%); color: #000; box-shadow: 0 4px 15px rgba(212, 175, 55, 0.3); }
.btn-primary:hover:not(:disabled) { transform: translateY(-2px); box-shadow: 0 6px 20px rgba(212, 175, 55, 0.4); }
.btn-secondary { background: rgba(255, 255, 255, 0.05); color: #fff; border: 1px solid rgba(255, 255, 255, 0.1); }
.btn-secondary:hover:not(:disabled) { background: rgba(255, 255, 255, 0.1); border-color: #D4AF37; color: #D4AF37; }
.btn-danger { background: rgba(239, 68, 68, 0.1); color: #ef4444; border: 1px solid rgba(239, 68, 68, 0.3); }
.btn-danger:hover:not(:disabled) { background: rgba(239, 68, 68, 0.2); box-shadow: 0 0 15px rgba(239, 68, 68, 0.3); }
.btn:disabled { opacity: 0.5; cursor: not-allowed; }

/* Badges */
.badge { padding: 0.35rem 0.75rem; border-radius: 999px; font-size: 0.7rem; font-weight: 700; letter-spacing: 0.5px; text-transform: uppercase; display: inline-block; }
.badge-primary { background: rgba(212, 175, 55, 0.15); border: 1px solid rgba(212, 175, 55, 0.4); color: #D4AF37; }
.badge-danger { background: rgba(239, 68, 68, 0.15); border: 1px solid rgba(239, 68, 68, 0.4); color: #f87171; }
.badge-success { background: rgba(16, 185, 129, 0.15); border: 1px solid rgba(16, 185, 129, 0.4); color: #34d399; }
.badge-gray { background: rgba(156, 163, 175, 0.15); border: 1px solid rgba(156, 163, 175, 0.4); color: #9ca3af; }
.badge-warning { background: rgba(245, 158, 11, 0.15); border: 1px solid rgba(245, 158, 11, 0.4); color: #fbbf24; }

/* Directories */
.tenant-roster { background: linear-gradient(145deg, #161616, #0c0c0c); border: 1px solid rgba(212, 175, 55, 0.2); border-radius: 12px; margin-bottom: 2rem; overflow: hidden; box-shadow: 0 5px 20px rgba(0,0,0,0.5); }
.tenant-header { padding: 1.5rem; border-bottom: 1px solid rgba(212, 175, 55, 0.2); display: flex; justify-content: space-between; align-items: center; background: rgba(0,0,0,0.3); }
.tenant-header h3 { color: #fff; margin: 0; font-size: 1.2rem; letter-spacing: 1px; }
.tenant-badges { display: flex; gap: 0.5rem; }

.client-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(350px, 1fr)); gap: 1.5rem; }
.client-card { background: linear-gradient(145deg, #1a1a1a, #0d0d0d); border-left: 3px solid rgba(212, 175, 55, 0.5); padding: 1.5rem; border-radius: 12px; box-shadow: 0 5px 15px rgba(0,0,0,0.4); transition: transform 0.3s; }
.client-card:hover { transform: translateY(-4px); }
.cc-header h3 { color: #D4AF37; margin: 0 0 0.25rem 0; font-size: 1.25rem; }
.cc-email { font-size: 0.85rem; color: #9ca3af; }
.cc-stats { display: flex; gap: 0.5rem; margin: 1rem 0; }
.comp-item { background: rgba(255,255,255,0.03); padding: 0.75rem; border-radius: 8px; margin-bottom: 0.5rem; }
.comp-name { font-weight: 600; color: #fff; font-size: 0.95rem; margin-bottom: 0.25rem; }
.comp-metrics { font-size: 0.8rem; }

/* Playbook */
.playbook-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 1.5rem; }
.playbook-card { background: rgba(10,10,10,0.6); border: 1px solid rgba(255,255,255,0.1); border-radius: 12px; padding: 1.5rem; transition: border-color 0.3s; }
.playbook-card:hover { border-color: #D4AF37; }
.pb-header { font-size: 1.2rem; font-weight: 700; color: #fff; margin-bottom: 0.5rem; }
.pb-focus { color: #d1d5db; font-size: 0.9rem; margin-bottom: 1rem; line-height: 1.5; }
.pb-next { font-size: 0.85rem; color: #D4AF37; background: rgba(212, 175, 55, 0.1); padding: 0.75rem; border-radius: 6px; }

/* Alerts & Modals */
.alert-box { padding: 1rem; border-radius: 8px; font-weight: 600; }
.warning-box { background: rgba(245, 158, 11, 0.15); color: #fbbf24; border-left: 4px solid #fbbf24; }
.danger-box { background: rgba(239, 68, 68, 0.15); color: #f87171; border-left: 4px solid #ef4444; }

.suggestions-list { max-height: 200px; overflow-y: auto; border: 1px solid rgba(255,255,255,0.1); border-radius: 8px; margin-top: 0.5rem; background: #111; }
.suggestion-item { padding: 0.75rem; border-bottom: 1px solid rgba(255,255,255,0.05); cursor: pointer; transition: background 0.2s; }
.suggestion-item:hover, .suggestion-item.selected { background: rgba(212, 175, 55, 0.1); }
.selected-user-box { background: rgba(239, 68, 68, 0.05); border: 1px solid rgba(239, 68, 68, 0.3); padding: 1rem; border-radius: 8px; }
</style>
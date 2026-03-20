<template>
  <div class="admin-page">
    <div class="page-header">
      <div>
        <h1>Admin Control Deck</h1>
        <p class="page-subtitle">Orchestrate workspaces, unlock insights, and manage every client.</p>
      </div>
      <div class="header-right">
        <a href="#user-management" class="btn btn-sm btn-secondary">Users</a>
        <a href="#client-directory" class="btn btn-sm btn-secondary">Clients</a>
        <a href="#analytics" class="btn btn-sm btn-secondary">Analytics</a>
        <a href="#support" class="btn btn-sm btn-secondary">Assist</a>
      </div>
    </div>

    <section id="user-management" v-if="!loading" class="section-block">
      <div class="section-top">
        <div>
          <h2 class="section-heading">User Management</h2>
          <p class="section-sub">Monitor users, track payments, manage access, and ban IPs</p>
        </div>
        <div style="text-align:right">
          <button @click="showQuickDeleteModal" class="btn btn-sm btn-danger">Quick Delete User</button>
          <p style="font-size:.6875rem;color:var(--gray-500);margin:.25rem 0 0">For immediate violation response</p>
        </div>
      </div>

      <div class="stat-row-6">
        <div class="stat-mini"><span class="sm-val">{{ userSummary.total_users }}</span><span class="sm-lbl">Total Users</span></div>
        <div class="stat-mini"><span class="sm-val">{{ userSummary.active_users }}</span><span class="sm-lbl">Active</span></div>
        <div class="stat-mini"><span class="sm-val">{{ userSummary.trial_users }}</span><span class="sm-lbl">Trial</span></div>
        <div class="stat-mini"><span class="sm-val">{{ userSummary.paid_users }}</span><span class="sm-lbl">Paid</span></div>
        <div class="stat-mini"><span class="sm-val">{{ userSummary.overdue_users }}</span><span class="sm-lbl">Overdue</span></div>
        <div class="stat-mini"><span class="sm-val">{{ userSummary.banned_users }}</span><span class="sm-lbl">Banned</span></div>
      </div>

      <div class="table-wrap">
        <table class="data-table">
          <thead>
            <tr>
              <th>User</th><th>Email</th><th>Company</th><th>Joined</th><th>Reg IP</th><th>Login IP</th><th>Payment</th><th>Status</th><th>Activity</th><th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="user in users" :key="user.id" :class="{ 'row-banned': user.is_banned, 'row-warn': user.warning }">
              <td>
                <div style="font-weight:600;font-size:.8125rem">{{ user.full_name }}</div>
                <div style="font-size:.75rem;color:var(--gray-500)">@{{ user.username }}</div>
                <span v-if="user.is_superuser" class="badge badge-blue" style="font-size:.5625rem">ADMIN</span>
                <span v-else-if="user.is_staff" class="badge badge-gray" style="font-size:.5625rem">STAFF</span>
                <span v-if="user.warning" class="badge badge-amber" style="font-size:.5625rem">
                  <template v-if="user.warning.type === 're_registration'">RE-REG</template>
                  <template v-else-if="user.warning.type === 'duplicate_ip'">DUP IP</template>
                </span>
              </td>
              <td>{{ user.email }}</td>
              <td>{{ user.company_name || '\u2014' }}</td>
              <td style="white-space:nowrap">{{ formatDate(user.date_joined) }}</td>
              <td><code style="font-size:.75rem">{{ user.registration_ip || '\u2014' }}</code></td>
              <td><code style="font-size:.75rem">{{ user.last_login_ip || '\u2014' }}</code></td>
              <td>
                <span class="badge" :class="'pay-' + user.payment_status">{{ formatPaymentStatus(user.payment_status) }}</span>
                <div v-if="user.payment_status === 'trial'" style="font-size:.6875rem;color:var(--gray-500)">{{ user.days_until_trial_end }}d left</div>
              </td>
              <td>
                <span v-if="user.is_banned" class="badge badge-red">Banned</span>
                <span v-else-if="!user.is_active" class="badge badge-gray">Inactive</span>
                <span v-else class="badge badge-green">Active</span>
              </td>
              <td style="text-align:center">
                <div style="font-weight:600;font-size:.8125rem">{{ user.total_activity }}</div>
                <div style="font-size:.6875rem;color:var(--gray-500)">{{ user.contact_count }}c &middot; {{ user.company_count }}co &middot; {{ user.deal_count }}d</div>
              </td>
              <td>
                <div style="display:flex;gap:.25rem;flex-wrap:wrap">
                  <button v-if="!user.is_banned && !user.is_superuser" @click="openBanModal(user)" class="btn btn-sm btn-danger" title="Ban">Ban</button>
                  <button v-if="user.is_banned" @click="unbanUser(user.id)" class="btn btn-sm btn-success" title="Unban">Unban</button>
                  <button v-if="!user.is_superuser" @click="openPaymentModal(user)" class="btn btn-sm btn-secondary" title="Payment">Pay</button>
                  <button v-if="!user.is_superuser && !user.is_staff" @click="confirmDelete(user)" class="btn btn-sm btn-danger" title="Delete">Del</button>
                  <button v-if="user.warning" @click="showWarningDetails(user)" class="btn btn-sm btn-secondary" title="Warning">Warn</button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <div v-if="showWarningDetailsModal" class="modal-overlay" @click="closeWarningDetails">
        <div class="modal-panel" @click.stop ref="warningModal" tabindex="-1">
          <div class="modal-header"><h3>Warning Details: {{ selectedUser?.full_name }}</h3><button class="modal-close" @click="closeWarningDetails">&times;</button></div>
          <div class="modal-body">
            <div v-if="selectedUser?.warning?.type === 're_registration'">
              <div class="info-bar" style="background:#fffbeb;color:var(--amber-500);margin-bottom:1rem"><strong>User Re-Registered After Deletion</strong></div>
              <p style="font-size:.8125rem"><strong>Previous Username:</strong> {{ selectedUser.warning.previous_username }}</p>
              <p style="font-size:.8125rem"><strong>Deleted:</strong> {{ selectedUser.warning.message.split('deleted on ')[1] }}</p>
              <p style="font-size:.8125rem"><strong>Reason:</strong> {{ selectedUser.warning.deleted_reason || 'Not specified' }}</p>
              <div v-if="selectedUser.warning.previous_activity" style="margin:.75rem 0">
                <h4 style="font-size:.75rem;font-weight:600;color:var(--gray-500);margin:0 0 .25rem">Previous Activity:</h4>
                <ul style="font-size:.8125rem;color:var(--gray-600);margin:0;padding-left:1.25rem">
                  <li>Contacts: {{ selectedUser.warning.previous_activity.contacts }}</li>
                  <li>Companies: {{ selectedUser.warning.previous_activity.companies }}</li>
                  <li>Deals: {{ selectedUser.warning.previous_activity.deals }}</li>
                </ul>
              </div>
              <p class="form-hint">Monitor their activity closely or consider blocking again.</p>
            </div>
            <div v-else-if="selectedUser?.warning?.type === 'duplicate_ip'">
              <div class="info-bar" style="background:#fef2f2;color:var(--red-500);margin-bottom:1rem"><strong>Duplicate IP Address Detected</strong></div>
              <p style="font-size:.8125rem"><strong>IP:</strong> {{ selectedUser.registration_ip }}</p>
              <div v-if="selectedUser.warning.deleted_users" style="margin:.75rem 0">
                <h4 style="font-size:.75rem;font-weight:600;color:var(--gray-500);margin:0 0 .25rem">Previously Deleted Users:</h4>
                <ul style="font-size:.8125rem;color:var(--gray-600);margin:0;padding-left:1.25rem">
                  <li v-for="(del, idx) in selectedUser.warning.deleted_users" :key="idx"><strong>{{ del.username }}</strong> ({{ del.email }}) - Deleted: {{ formatDate(del.deleted_at) }}<br><small>Reason: {{ del.deleted_reason || 'Not specified' }}</small></li>
                </ul>
              </div>
              <p class="form-hint">Could indicate multi-accounting or IP sharing. Investigate before allowing full access.</p>
            </div>
          </div>
          <div class="modal-footer"><button @click="closeWarningDetails" class="btn btn-secondary">Close</button></div>
        </div>
      </div>

      <div v-if="showQuickDelete" class="modal-overlay" @click="closeQuickDelete">
        <div class="modal-panel" @click.stop ref="quickDeleteModal" tabindex="-1">
          <div class="modal-header"><h3>Quick Delete User</h3><button class="modal-close" @click="closeQuickDelete">&times;</button></div>
          <div class="modal-body">
            <p style="font-size:.8125rem;color:var(--gray-600);margin-bottom:1rem">Immediate action for policy violators.</p>
            <div class="form-group">
              <label class="form-label">Search User</label>
              <input v-model="quickDeleteSearch" type="text" placeholder="Type username or email..." class="form-input" @input="filterUsersForDelete" />
            </div>
            <div v-if="filteredDeleteUsers.length > 0" style="max-height:200px;overflow-y:auto;border:1px solid var(--border-color);border-radius:var(--radius-md);margin-bottom:1rem">
              <div v-for="user in filteredDeleteUsers.slice(0, 8)" :key="user.id" @click="selectUserForQuickDelete(user)" style="padding:.5rem .75rem;cursor:pointer;border-bottom:1px solid var(--gray-100);font-size:.8125rem" :style="quickDeleteUser?.id === user.id ? 'background:var(--gray-100)' : ''">
                <strong>{{ user.full_name }}</strong> (@{{ user.username }})<br><small style="color:var(--gray-500)">{{ user.email }} &middot; {{ user.total_activity }} items</small>
              </div>
            </div>
            <div v-if="quickDeleteUser" style="background:var(--gray-50);border-radius:var(--radius-md);padding:.75rem 1rem;margin-bottom:1rem">
              <h4 style="font-size:.8125rem;font-weight:600;color:var(--red-500);margin:0 0 .5rem">Confirm Deletion:</h4>
              <p style="font-size:.8125rem;margin:.125rem 0"><strong>User:</strong> {{ quickDeleteUser.full_name }} (@{{ quickDeleteUser.username }})</p>
              <p style="font-size:.8125rem;margin:.125rem 0"><strong>Email:</strong> {{ quickDeleteUser.email }}</p>
              <p style="font-size:.8125rem;margin:.125rem 0"><strong>Activity:</strong> {{ quickDeleteUser.contact_count }} contacts, {{ quickDeleteUser.company_count }} companies, {{ quickDeleteUser.deal_count }} deals</p>
              <div class="form-group" style="margin-top:.75rem">
                <label class="form-label">Reason (Required)</label>
                <select v-model="quickDeleteReason" class="form-input">
                  <option value="">-- Select Reason --</option>
                  <option value="Terms of Service Violation">Terms of Service Violation</option>
                  <option value="Fraudulent Activity">Fraudulent Activity</option>
                  <option value="Payment Fraud">Payment Fraud</option>
                  <option value="Abuse of Platform">Abuse of Platform</option>
                  <option value="Harassment">Harassment</option>
                  <option value="Spam/Bot Activity">Spam/Bot Activity</option>
                  <option value="Data Manipulation">Data Manipulation</option>
                  <option value="Other Policy Violation">Other Policy Violation</option>
                </select>
              </div>
              <div v-if="quickDeleteReason === 'Other Policy Violation'" class="form-group">
                <label class="form-label">Specify Reason</label>
                <input v-model="quickDeleteCustomReason" type="text" class="form-input" placeholder="Enter specific violation..." />
              </div>
            </div>
          </div>
          <div class="modal-footer">
            <button @click="closeQuickDelete" class="btn btn-secondary">Cancel</button>
            <button @click="executeQuickDelete" :disabled="!quickDeleteUser || !quickDeleteReason" class="btn btn-danger">Permanently Delete</button>
          </div>
        </div>
      </div>

      <div v-if="showBanModal" class="modal-overlay" @click="closeBanModal">
        <div class="modal-panel" @click.stop ref="banModal" tabindex="-1">
          <div class="modal-header"><h3>Ban User: {{ selectedUser?.full_name }}</h3><button class="modal-close" @click="closeBanModal">&times;</button></div>
          <div class="modal-body">
            <p style="font-size:.8125rem;color:var(--gray-600);margin-bottom:1rem">This will immediately block access and deactivate their account.</p>
            <div class="form-group">
              <label class="form-label">Reason</label>
              <select v-model="banReason" class="form-input">
                <option value="Unpaid subscription">Unpaid subscription</option>
                <option value="Payment overdue">Payment overdue</option>
                <option value="Terms of service violation">Terms of service violation</option>
                <option value="Fraudulent activity">Fraudulent activity</option>
                <option value="Abuse of platform">Abuse of platform</option>
                <option value="Other">Other</option>
              </select>
            </div>
            <div v-if="banReason === 'Other'" class="form-group">
              <label class="form-label">Custom Reason</label>
              <input v-model="customBanReason" type="text" class="form-input" placeholder="Enter reason..." />
            </div>
            <div style="font-size:.8125rem;color:var(--gray-500);margin-top:.5rem">
              <p><strong>Email:</strong> {{ selectedUser?.email }}</p>
              <p><strong>Reg IP:</strong> {{ selectedUser?.registration_ip }}</p>
              <p><strong>Last IP:</strong> {{ selectedUser?.last_login_ip }}</p>
            </div>
          </div>
          <div class="modal-footer">
            <button @click="closeBanModal" class="btn btn-secondary">Cancel</button>
            <button @click="confirmBan" class="btn btn-danger">Confirm Ban</button>
          </div>
        </div>
      </div>

      <div v-if="showPaymentModal" class="modal-overlay" @click="closePaymentModal">
        <div class="modal-panel" @click.stop ref="paymentModal" tabindex="-1">
          <div class="modal-header"><h3>Update Payment: {{ selectedUser?.full_name }}</h3><button class="modal-close" @click="closePaymentModal">&times;</button></div>
          <div class="modal-body">
            <div class="form-group">
              <label class="form-label">Payment Status</label>
              <select v-model="newPaymentStatus" class="form-input">
                <option value="pending">Pending Payment</option>
                <option value="trial">Trial Period (14 days)</option>
                <option value="paid">Paid</option>
                <option value="overdue">Overdue</option>
              </select>
            </div>
            <p style="font-size:.8125rem;color:var(--gray-500);margin-top:.5rem">
              <span v-if="newPaymentStatus === 'paid'">User will have full access.</span>
              <span v-if="newPaymentStatus === 'trial'">User will have 14 days trial access.</span>
              <span v-if="newPaymentStatus === 'overdue'">Consider banning if payment not received.</span>
              <span v-if="newPaymentStatus === 'pending'">Awaiting payment confirmation.</span>
            </p>
          </div>
          <div class="modal-footer">
            <button @click="closePaymentModal" class="btn btn-secondary">Cancel</button>
            <button @click="confirmPaymentUpdate" class="btn btn-primary">Update Status</button>
          </div>
        </div>
      </div>
    </section>

    <section id="analytics" class="section-block" v-if="!loading">
      <h2 class="section-heading">Company Performance</h2>
      <div class="stat-row-4">
        <div class="stat-mini"><span class="sm-val">{{ overview.analytics.total_deals }}</span><span class="sm-lbl">Total Deals</span></div>
        <div class="stat-mini"><span class="sm-val">{{ overview.analytics.active_deals }}</span><span class="sm-lbl">Active Pipeline</span></div>
        <div class="stat-mini"><span class="sm-val">{{ formatCurrency(overview.analytics.pipeline_value) }}</span><span class="sm-lbl">Pipeline Value</span></div>
        <div class="stat-mini"><span class="sm-val">{{ formatCurrency(overview.analytics.won_value) }}</span><span class="sm-lbl">Closed Won</span></div>
      </div>
    </section>

    <section v-if="loading" style="text-align:center;padding:3rem"><span class="spinner"></span><p style="color:var(--gray-500);margin-top:.75rem">Loading admin intelligence...</p></section>
    <section v-if="error" class="info-bar" style="background:#fef2f2;color:var(--red-500);margin-bottom:1rem">{{ error }}</section>

    <section id="client-employee-mgmt" class="section-block" v-if="!loadingClientsEmployees">
      <div class="section-top">
        <div>
          <h2 class="section-heading">Client &amp; Employee Management</h2>
          <p class="section-sub">View all client companies and their employees</p>
        </div>
        <button @click="refreshClientsEmployees" class="btn btn-sm btn-secondary">Refresh</button>
      </div>

      <div class="stat-row-4" style="margin-bottom:1.25rem">
        <div class="stat-mini"><span class="sm-val">{{ clientEmployeeStats.total_companies }}</span><span class="sm-lbl">Companies</span></div>
        <div class="stat-mini"><span class="sm-val">{{ clientEmployeeStats.total_clients }}</span><span class="sm-lbl">Total Users</span></div>
        <div class="stat-mini"><span class="sm-val">{{ clientEmployeeStats.total_admins }}</span><span class="sm-lbl">Admins</span></div>
        <div class="stat-mini"><span class="sm-val">{{ clientEmployeeStats.total_employees }}</span><span class="sm-lbl">Employees</span></div>
      </div>

      <div class="companies-list">
        <div v-for="company in clientsEmployeesData" :key="company.company_name" class="card" style="padding:0;margin-bottom:.75rem;overflow:hidden">
          <div style="padding:.75rem 1.25rem;border-bottom:1px solid var(--border-color);display:flex;align-items:center;justify-content:space-between">
            <h3 style="font-size:.9375rem;font-weight:600;color:var(--gray-900);margin:0">{{ company.company_name }}</h3>
            <div style="display:flex;gap:.375rem">
              <span class="badge badge-gray">{{ company.total_users }} users</span>
              <span class="badge badge-blue">{{ company.admins }} admins</span>
              <span class="badge badge-green">{{ company.employees }} emp</span>
            </div>
          </div>
          <div style="padding:.5rem 1.25rem">
            <div v-for="employee in company.users" :key="employee.id" style="display:flex;align-items:center;gap:.75rem;padding:.5rem 0;border-bottom:1px solid var(--gray-100);font-size:.8125rem" :style="{ opacity: employee.is_banned ? '.5' : '1' }">
              <div style="width:32px;height:32px;border-radius:50%;background:var(--primary-500);color:#fff;display:flex;align-items:center;justify-content:center;font-weight:600;font-size:.75rem;flex-shrink:0">{{ getInitials(employee.full_name || employee.username) }}</div>
              <div style="flex:1;min-width:0">
                <div style="font-weight:600">{{ employee.full_name }}</div>
                <div style="font-size:.75rem;color:var(--gray-500)">{{ employee.email }} &middot; {{ employee.job_title || '' }}</div>
              </div>
              <span class="badge" :class="'role-' + employee.role" style="font-size:.5625rem">{{ formatRole(employee.role) }}</span>
              <div style="font-size:.6875rem;color:var(--gray-500)">{{ employee.data_counts.contacts }}c &middot; {{ employee.data_counts.deals }}d</div>
              <div style="display:flex;gap:.25rem">
                <button @click="resetPassword(employee)" class="btn btn-sm btn-secondary">Reset PW</button>
                <button @click="toggleActive(employee)" class="btn btn-sm btn-secondary">{{ employee.is_active ? 'Deactivate' : 'Activate' }}</button>
                <button v-if="!employee.is_banned" @click="banUser(employee)" class="btn btn-sm btn-danger">Ban</button>
                <button v-else @click="unbanUser(employee)" class="btn btn-sm btn-success">Unban</button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <section id="client-directory" class="section-block" v-if="!loading && overview.clients.length">
      <h2 class="section-heading">Client Directory</h2>
      <p class="section-sub">Drill into every workspace, their companies, and key contacts.</p>
      <div class="client-grid">
        <div v-for="client in overview.clients" :key="client.user_id" class="card" style="padding:1.25rem">
          <h3 style="font-size:.9375rem;font-weight:600;color:var(--gray-900);margin:0 0 .25rem">{{ client.username }}</h3>
          <p style="font-size:.8125rem;color:var(--gray-500);margin:0 0 .5rem">{{ client.email }}</p>
          <div style="display:flex;gap:.5rem;margin-bottom:.75rem">
            <span class="badge badge-gray">{{ client.companies.length }} companies</span>
            <span class="badge badge-blue">{{ client.total_contacts }} contacts</span>
            <span class="badge badge-green">{{ client.total_deals }} deals</span>
          </div>
          <div v-for="company in client.companies" :key="company.id" style="background:var(--gray-50);border-radius:var(--radius-sm);padding:.625rem;margin-bottom:.5rem">
            <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:.375rem">
              <h4 style="font-size:.8125rem;font-weight:600;margin:0">{{ company.name }}</h4>
              <span style="font-size:.6875rem;color:var(--gray-500)">{{ company.contact_count }}c &middot; {{ company.deal_count }}d &middot; {{ formatCurrency(company.pipeline_value) }}</span>
            </div>
            <ul style="margin:0;padding-left:1rem;font-size:.75rem;color:var(--gray-600)">
              <li v-for="contact in company.contacts" :key="contact.id" style="margin-bottom:.125rem">
                <strong>{{ contact.name }}</strong> <span style="color:var(--gray-400)">{{ contact.email }}</span>
                <span v-if="contact.company_hint" style="color:var(--gray-400)"> &middot; {{ contact.company_hint }}</span>
              </li>
            </ul>
          </div>
        </div>
      </div>
    </section>

    <section id="support" class="section-block" v-if="!loading">
      <h2 class="section-heading">Assist Drive Playbook</h2>
      <p class="section-sub">Three flagship companies showcase how THE FINISHER backs partner growth.</p>
      <div class="assist-grid">
        <div v-for="item in overview.support_catalog" :key="item.name" class="card" style="padding:1.25rem">
          <h3 style="font-size:.9375rem;font-weight:600;color:var(--gray-900);margin:0 0 .25rem">{{ item.name }}</h3>
          <p style="font-size:.75rem;color:var(--primary-500);margin:0 0 .375rem">{{ item.industry }}</p>
          <p style="font-size:.8125rem;color:var(--gray-600);margin:0 0 .375rem;line-height:1.4">{{ item.focus }}</p>
          <p style="font-size:.75rem;color:var(--gray-500);margin:0 0 .5rem">{{ item.next_step }}</p>
          <button @click="notifyComingSoon" class="btn btn-sm btn-secondary">Assist (Soon)</button>
        </div>
      </div>
    </section>
  </div>
</template>

<script>
import { systemAPI } from '../api'
import toast from '../utils/toast'
import modal from '../utils/modal'

export default {
  name: 'AdminConsole',
  data() {
    return {
      loading: true,
      error: '',
      overview: {
        analytics: {
          total_deals: 0,
          active_deals: 0,
          pipeline_value: '0',
          won_value: '0'
        },
        clients: [],
        support_catalog: []
      },
      users: [],
      userSummary: {
        total_users: 0,
        active_users: 0,
        banned_users: 0,
        trial_users: 0,
        paid_users: 0,
        overdue_users: 0
      },
      
      loadingClientsEmployees: false,
      clientsEmployeesData: [],
      clientEmployeeStats: {
        total_companies: 0,
        total_clients: 0,
        total_admins: 0,
        total_employees: 0
      },
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
      filteredDeleteUsers: [],
    }
  },
  async mounted() {
    await Promise.all([
      this.loadOverview(),
      this.loadUsers(),
      this.loadClientsEmployees()
    ])
  },
  methods: {
    focusModal(refName) {
      this.$nextTick(() => {
        const target = this.$refs[refName]
        const modal = Array.isArray(target) ? target[0] : target
        if (!modal) {
          return
        }
        if (typeof modal.scrollTo === 'function') {
          modal.scrollTo({ top: 0, behavior: 'auto' })
        } else {
          modal.scrollTop = 0
        }
        if (typeof modal.focus === 'function') {
          modal.focus()
        }
      })
    },
    async loadUsers() {
      try {
        const response = await systemAPI.getUserManagement()
        this.users = response.data.users || []
        this.userSummary = response.data.summary || this.userSummary
      } catch (err) {
        console.error('Failed to load users:', err)
        this.error = 'Unable to load user data.'
      }
    },
    async loadOverview() {
      this.loading = true
      this.error = ''
      try {
        const response = await systemAPI.getAdminOverview()
        const payload = response.data || {}
        this.overview = {
          analytics: {
            total_deals: payload.analytics?.total_deals ?? 0,
            active_deals: payload.analytics?.active_deals ?? 0,
            pipeline_value: payload.analytics?.pipeline_value ?? '0',
            won_value: payload.analytics?.won_value ?? '0'
          },
          clients: payload.clients || [],
          support_catalog: payload.support_catalog || []
        }
      } catch (err) {
        console.error('Failed to load admin overview:', err)
        this.error = err.message || 'Unable to load admin intelligence.'
      } finally {
        this.loading = false
      }
    },
    async loadClientsEmployees() {
      try {
        this.loadingClientsEmployees = true
        const response = await systemAPI.getClientsEmployees()
        this.clientsEmployeesData = response.data.companies || []
        this.clientEmployeeStats = response.data.stats || this.clientEmployeeStats
      } catch (error) {
        console.error('Error loading clients & employees:', error)
        this.error = 'Failed to load client & employee data'
      } finally {
        this.loadingClientsEmployees = false
      }
    },
    async refreshClientsEmployees() {
      await this.loadClientsEmployees()
    },
    getInitials(name) {
      if (!name) return '??'
      const words = name.trim().split(' ')
      if (words.length >= 2) {
        return (words[0][0] + words[words.length - 1][0]).toUpperCase()
      }
      return name.substring(0, 2).toUpperCase()
    },
    formatRole(role) {
      const map = {
        'admin': 'Administrator',
        'manager': 'Manager',
        'supervisor': 'Supervisor',
        'user': 'User'
      }
      return map[role] || role
    },
    async resetPassword(employee) {
      const ok = await modal.confirm('Reset Password', `Reset password for ${employee.full_name || employee.username}?`, 'warning', { confirmText: 'Reset' })
      if (!ok) return
      
      try {
        const response = await systemAPI.resetUserPassword(employee.id)
        await modal.alert('Password Reset', `Password reset successfully!\n\nUsername: ${response.data.username}\nTemporary Password: ${response.data.temporary_password}\n\nPlease share this with the user securely.`, 'success')
        await this.loadClientsEmployees()
      } catch (error) {
        console.error('Error resetting password:', error)
        toast.error('Reset Failed', 'Failed to reset password: ' + (error.response?.data?.error || error.message))
      }
    },
    async toggleActive(employee) {
      try {
        const response = await systemAPI.toggleUserActive(employee.id)
        toast.success('Status Updated', response.data.message)
        await this.loadClientsEmployees()
      } catch (error) {
        console.error('Error toggling user status:', error)
        toast.error('Toggle Failed', 'Failed to toggle user status')
      }
    },
    async banUser(employee) {
      const reason = await modal.prompt('Ban User', `Ban reason for ${employee.full_name || employee.username}:`, { defaultValue: 'Violation of terms', confirmText: 'Ban User' })
      if (!reason) return
      
      try {
        await systemAPI.banClient(employee.id, reason)
        toast.success('User Banned', 'User has been banned successfully.')
        await this.loadClientsEmployees()
      } catch (error) {
        console.error('Error banning user:', error)
        toast.error('Ban Failed', 'Failed to ban user')
      }
    },
    async unbanUser(employee) {
      const ok = await modal.confirm('Unban User', `Unban ${employee.full_name || employee.username}?`, 'info', { confirmText: 'Unban' })
      if (!ok) return
      
      try {
        await systemAPI.unbanClient(employee.id)
        toast.success('User Unbanned', 'User has been unbanned successfully.')
        await this.loadClientsEmployees()
      } catch (error) {
        console.error('Error unbanning user:', error)
        toast.error('Unban Failed', 'Failed to unban user')
      }
    },
    formatCurrency(value) {
      const numeric = Number(value || 0)
      return `R${new Intl.NumberFormat('en-ZA', { maximumFractionDigits: 2 }).format(numeric)}`
    },
    formatDate(dateString) {
      if (!dateString) return '—'
      const date = new Date(dateString)
      return date.toLocaleDateString('en-ZA', { year: 'numeric', month: 'short', day: 'numeric' })
    },
    formatPaymentStatus(status) {
      const map = {
        'pending': '⏳ Pending',
        'paid': '✅ Paid',
        'overdue': '⚠️ Overdue',
        'trial': '⏱️ Trial'
      }
      return map[status] || status
    },
    openBanModal(user) {
      this.selectedUser = user
      this.banReason = 'Unpaid subscription'
      this.customBanReason = ''
      this.showBanModal = true
      this.focusModal('banModal')
    },
    closeBanModal() {
      this.showBanModal = false
      this.selectedUser = null
    },
    async confirmBan() {
      const reason = this.banReason === 'Other' ? this.customBanReason : this.banReason
      
      if (!reason) {
        toast.warning('Reason Required', 'Please provide a reason for banning this user.')
        return
      }
      
      try {
        await systemAPI.banUser(this.selectedUser.id, reason)
        toast.success('User Banned', `User ${this.selectedUser.username} has been banned.`)
        this.closeBanModal()
        await this.loadUsers()
      } catch (err) {
        console.error('Ban failed:', err)
        toast.error('Ban Failed', 'Failed to ban user. Please try again.')
      }
    },
    async unbanUser(userId) {
      const ok = await modal.confirm('Unban User', 'Are you sure you want to unban this user?', 'info', { confirmText: 'Unban' })
      if (!ok) return
      
      try {
        await systemAPI.unbanUser(userId)
        toast.success('User Unbanned', 'User has been unbanned.')
        await this.loadUsers()
      } catch (err) {
        console.error('Unban failed:', err)
        toast.error('Unban Failed', 'Failed to unban user. Please try again.')
      }
    },
    openPaymentModal(user) {
      this.selectedUser = user
      this.newPaymentStatus = user.payment_status
      this.showPaymentModal = true
      this.focusModal('paymentModal')
    },
    closePaymentModal() {
      this.showPaymentModal = false
      this.selectedUser = null
    },
    async confirmPaymentUpdate() {
      try {
        await systemAPI.updatePaymentStatus(this.selectedUser.id, this.newPaymentStatus)
        toast.success('Payment Updated', 'Payment status updated successfully.')
        this.closePaymentModal()
        await this.loadUsers()
      } catch (err) {
        console.error('Payment update failed:', err)
        toast.error('Update Failed', 'Failed to update payment status. Please try again.')
      }
    },
    async confirmDelete(user) {
      if (!user) {
        return
      }

      const reasonInput = await modal.prompt('Delete User', `Provide a reason for deleting ${user.username}:`, { confirmText: 'Continue' })
      const reason = reasonInput?.trim()
      if (!reason) {
        toast.warning('Cancelled', 'Deletion cancelled. A reason is required.')
        return
      }

      const details = [
        `User: ${user.full_name || user.username}`,
        `Contacts: ${user.contact_count || 0}`,
        `Companies: ${user.company_count || 0}`,
        `Deals: ${user.deal_count || 0}`
      ].join('\n')

      const confirmed = await modal.danger('Permanently Delete User', `${details}\n\nReason: ${reason}\n\nThis action cannot be undone.`, { confirmText: 'Delete Permanently' })

      if (!confirmed) {
        return
      }

      try {
        await systemAPI.deleteUser(user.id, reason)
        toast.success('User Deleted', `User ${user.username} has been deleted.`)
        await this.loadUsers()
      } catch (err) {
        console.error('Delete failed:', err)
        toast.error('Delete Failed', 'Failed to delete user. Please try again.')
      }
    },
    showWarningDetails(user) {
      this.selectedUser = user
      this.showWarningDetailsModal = true
      this.focusModal('warningModal')
    },
    closeWarningDetails() {
      this.showWarningDetailsModal = false
    },
    showQuickDeleteModal() {
      this.showQuickDelete = true
      this.quickDeleteSearch = ''
      this.quickDeleteUser = null
      this.quickDeleteReason = ''
      this.quickDeleteCustomReason = ''
      this.filteredDeleteUsers = []
      this.focusModal('quickDeleteModal')
    },
    closeQuickDelete() {
      this.showQuickDelete = false
      this.quickDeleteSearch = ''
      this.quickDeleteUser = null
      this.quickDeleteReason = ''
      this.quickDeleteCustomReason = ''
      this.filteredDeleteUsers = []
    },
    filterUsersForDelete() {
      const search = this.quickDeleteSearch.toLowerCase().trim()
      if (search.length < 2) {
        this.filteredDeleteUsers = []
        return
      }
      
      this.filteredDeleteUsers = this.users.filter(user => 
        !user.is_superuser && 
        (user.username.toLowerCase().includes(search) ||
         user.email.toLowerCase().includes(search) ||
         user.full_name.toLowerCase().includes(search))
      )
    },
    selectUserForQuickDelete(user) {
      this.quickDeleteUser = user
    },
    async executeQuickDelete() {
      if (!this.quickDeleteUser || !this.quickDeleteReason) {
        toast.warning('Incomplete', 'Please select a user and provide a reason.')
        return
      }

      const finalReason = this.quickDeleteReason === 'Other Policy Violation' 
        ? this.quickDeleteCustomReason 
        : this.quickDeleteReason

      if (!finalReason.trim()) {
        toast.warning('Reason Required', 'Please specify the violation reason.')
        return
      }

      const confirmed = await modal.danger('Critical Action', 
        `Permanently delete ${this.quickDeleteUser.username}?\n\n` +
        `User: ${this.quickDeleteUser.full_name}\n` +
        `Email: ${this.quickDeleteUser.email}\n` +
        `Contacts: ${this.quickDeleteUser.contact_count}\n` +
        `Companies: ${this.quickDeleteUser.company_count}\n` +
        `Deals: ${this.quickDeleteUser.deal_count}\n\n` +
        `Reason: ${finalReason}\n\n` +
        `This action CANNOT be undone!`,
        { confirmText: 'Delete Permanently' }
      )

      if (!confirmed) {
        return
      }

      try {
        await systemAPI.deleteUser(this.quickDeleteUser.id, finalReason)
        toast.success('User Deleted', `User ${this.quickDeleteUser.username} has been permanently deleted.`)
        this.closeQuickDelete()
        await this.loadUsers()
      } catch (err) {
        console.error('Quick delete failed:', err)
        toast.error('Delete Failed', 'Failed to delete user. Please try again.')
      }
    },
    notifyComingSoon() {
      modal.alert('Coming Soon', 'This assist workflow is being finalised. Full orchestration launches soon!', 'info')
    }
  }
}
</script>
<style scoped>
.admin-page { padding: 0; }

.section-block { margin-bottom: 2rem; }
.section-top { display: flex; justify-content: space-between; align-items: flex-start; gap: 1rem; margin-bottom: 1rem; flex-wrap: wrap; }
.header-right { display: flex; gap: .5rem; flex-wrap: wrap; }
.section-heading { font-size: 1.125rem; font-weight: 700; color: var(--gray-900); margin: 0 0 .25rem; }
.section-sub { font-size: .8125rem; color: var(--gray-500); margin: 0; }

.stat-row-6 { display: grid; grid-template-columns: repeat(6, 1fr); gap: .75rem; margin-bottom: 1.25rem; }
.stat-row-4 { display: grid; grid-template-columns: repeat(4, 1fr); gap: .75rem; margin-bottom: 1.25rem; }
.stat-mini { background: #fff; border: 1px solid var(--border-color); border-radius: var(--radius-md); padding: .75rem; text-align: center; }
.sm-val { display: block; font-size: 1.25rem; font-weight: 700; color: var(--gray-900); }
.sm-lbl { display: block; font-size: .6875rem; color: var(--gray-500); text-transform: uppercase; letter-spacing: .04em; }

.table-wrap { overflow-x: auto; overflow-y: visible; border: 1px solid var(--border-color); border-radius: var(--radius-md); -webkit-overflow-scrolling: touch; }
.table-wrap::-webkit-scrollbar { height: 8px; }
.table-wrap::-webkit-scrollbar-track { background: var(--gray-100); }
.table-wrap::-webkit-scrollbar-thumb { background: var(--gray-400); border-radius: 4px; }
.table-wrap .data-table { min-width: 0; width: 100%; }
.row-banned { background: #fef2f2; }
.row-warn { background: #fffbeb; }

.pay-pending { background: var(--gray-100); color: var(--gray-600); }
.pay-trial { background: #eff6ff; color: var(--primary-500); }
.pay-paid { background: #ecfdf5; color: var(--green-500); }
.pay-overdue { background: #fef2f2; color: var(--red-500); }

.info-bar { background: #eff6ff; color: var(--primary-500); padding: .75rem 1rem; border-radius: var(--radius-md); font-size: .8125rem; line-height: 1.5; }

.role-admin { background: #fef2f2; color: var(--red-500); }
.role-manager { background: #fffbeb; color: var(--amber-500); }
.role-supervisor { background: #eff6ff; color: var(--primary-500); }
.role-user, .role-employee { background: var(--gray-100); color: var(--gray-600); }

.client-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(400px, 1fr)); gap: 1rem; }
.assist-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 1rem; }

@media (max-width: 1024px) {
  .section-top { flex-direction: column; align-items: flex-start; }
  .stat-row-6 { grid-template-columns: repeat(3, 1fr); }
  .stat-row-4 { grid-template-columns: repeat(2, 1fr); }
  .client-grid { grid-template-columns: 1fr; }
  .table-wrap .data-table { min-width: 980px; }
}

@media (max-width: 768px) {
  .stat-row-6 { grid-template-columns: repeat(2, 1fr); }
  .stat-row-4 { grid-template-columns: repeat(2, 1fr); }
  .page-header { flex-direction: column; align-items: flex-start; gap: 0.75rem; }
  .header-right { width: 100%; }
  .section-heading { font-size: 1rem; }
  .table-wrap .data-table { min-width: 820px; }
}

@media (max-width: 640px) {
  .stat-row-6 { grid-template-columns: repeat(2, 1fr); gap: 0.5rem; }
  .stat-row-4 { grid-template-columns: 1fr; gap: 0.5rem; }
  .sm-val { font-size: 1.125rem; }
  .sm-lbl { font-size: 0.625rem; }
  .assist-grid { grid-template-columns: 1fr; }
  .table-wrap .data-table { min-width: 760px; }
}
</style>

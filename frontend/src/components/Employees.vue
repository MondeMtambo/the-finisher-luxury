<template>
  <div class="employees-page">

    <div class="page-header">
      <div>
        <h1>Employee Directory <span class="admp-badge">ADMP</span></h1>
        <p class="page-subtitle">
          {{ isSystemAdmin ? 'System-wide employee management' : 'Manage your organisation\'s employees' }}
        </p>
      </div>
      <div class="header-right">
        <span class="badge badge-gray" style="font-size:.8125rem">{{ remainingSlots ?? '-' }} / {{ maxUsers }} slots</span>
      </div>
    </div>

    <div class="stats-bar" v-if="!loading">
      <div class="stat-card">
        <div class="stat-value">{{ employees.length }}</div>
        <div class="stat-label">Total Employees</div>
      </div>
      <div class="stat-card">
        <div class="stat-value">{{ countByRole('admin') }}</div>
        <div class="stat-label">CEO / Admins</div>
      </div>
      <div class="stat-card">
        <div class="stat-value">{{ countByRole('executive') }}</div>
        <div class="stat-label">Executives</div>
      </div>
      <div class="stat-card">
        <div class="stat-value">{{ pendingOffboardCount }}</div>
        <div class="stat-label">Pending Offboard</div>
      </div>
    </div>

    <div class="tab-nav">
      <button @click="activeTab = 'directory'" :class="{ active: activeTab === 'directory' }">
        <svg width="16" height="16" fill="none" stroke="currentColor" stroke-width="2"><circle cx="8" cy="5" r="3"/><path d="M2 15c0-3.3 2.7-6 6-6s6 2.7 6 6"/></svg>
        Directory
      </button>
      <button v-if="canOnboard" @click="activeTab = 'onboard'" :class="{ active: activeTab === 'onboard' }">
        <svg width="16" height="16" fill="none" stroke="currentColor" stroke-width="2"><line x1="8" y1="3" x2="8" y2="13"/><line x1="3" y1="8" x2="13" y2="8"/></svg>
        Onboard
      </button>
      <button @click="activeTab = 'offboarding'" :class="{ active: activeTab === 'offboarding' }">
        <svg width="16" height="16" fill="none" stroke="currentColor" stroke-width="2"><path d="M9 3H4a1 1 0 00-1 1v8a1 1 0 001 1h5M7 8h6m0 0l-2-2m2 2l-2 2"/></svg>
        Offboarding
      </button>
      <button @click="activeTab = 'logs'" :class="{ active: activeTab === 'logs' }">
        <svg width="16" height="16" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 3h10v10H3z"/><path d="M5 7h6M5 9h4"/></svg>
        Activity Log
      </button>
    </div>

    <div v-if="loading" style="text-align:center;padding:3rem"><span class="spinner"></span></div>

    <div v-else-if="activeTab === 'directory'">

      <div class="filter-bar">
        <input v-model="searchQuery" type="text" class="form-input search-input" placeholder="Search employees...">
        <select v-model="roleFilter" class="form-input filter-select">
          <option value="">All Roles</option>
          <option value="admin">CEO / Administrator</option>
          <option value="executive">Executive</option>
          <option value="manager">Manager</option>
          <option value="supervisor">Supervisor</option>
          <option value="user">Standard Employee</option>
        </select>
      </div>

      <div v-if="filteredEmployees.length === 0" class="empty-state">
        <svg width="48" height="48" fill="none" stroke="var(--gray-400)" stroke-width="1.5"><circle cx="24" cy="16" r="8"/><path d="M8 42c0-8.8 7.2-16 16-16s16 7.2 16 16"/></svg>
        <h3>No Employees Found</h3>
        <p>{{ searchQuery || roleFilter ? 'Try adjusting your search or filter' : 'Add your first team member to get started' }}</p>
      </div>

      <div v-else class="emp-grid">
        <div v-for="employee in filteredEmployees" :key="employee.id" class="emp-card card" :class="{ 'emp-inactive': !employee.is_active, 'emp-banned': employee.is_banned }">
          <div class="emp-top">
            <div class="avatar" :class="'avatar-' + getRoleValue(employee.role)">{{ getInitials(employee) }}</div>
            <div class="emp-identity">
              <h3 class="emp-name">{{ employee.full_name || employee.username }}</h3>
              <p class="emp-email">{{ employee.email }}</p>
            </div>
            <span class="badge" :class="roleBadge(employee.role)">{{ getRoleLabel(employee.role) }}</span>
            <span class="badge status-badge" :class="onboardingStatusBadge(employee.onboarding_status)">{{ employee.onboarding_status_label || 'Onboarded' }}</span>
          </div>
          <div class="emp-details">
            <div v-if="isSystemAdmin && employee.company_name" class="detail-row">
              <span class="detail-label">Company</span>
              <span class="detail-value">{{ employee.company_name }}</span>
            </div>
            <div v-if="employee.job_title" class="detail-row">
              <span class="detail-label">Position</span>
              <span class="detail-value">{{ employee.job_title }}</span>
            </div>
            <div v-if="employee.department" class="detail-row">
              <span class="detail-label">Department</span>
              <span class="detail-value">{{ employee.department }}</span>
            </div>
            <div v-if="employee.employee_id" class="detail-row">
              <span class="detail-label">Employee ID</span>
              <span class="detail-value">{{ employee.employee_id }}</span>
            </div>
            <div v-if="employee.reports_to_name" class="detail-row">
              <span class="detail-label">Reports To</span>
              <span class="detail-value">{{ employee.reports_to_name }}</span>
            </div>
            <div v-if="employee.phone" class="detail-row">
              <span class="detail-label">Phone</span>
              <span class="detail-value">{{ employee.phone }}</span>
            </div>
            <div v-if="employee.start_date" class="detail-row">
              <span class="detail-label">Start Date</span>
              <span class="detail-value">{{ formatDate(employee.start_date) }}</span>
            </div>
            <div v-if="employee.direct_reports_count > 0" class="detail-row">
              <span class="detail-label">Direct Reports</span>
              <span class="detail-value">{{ employee.direct_reports_count }} employee{{ employee.direct_reports_count > 1 ? 's' : '' }}</span>
            </div>
            <div v-if="employee.onboarded_by_name" class="detail-row">
              <span class="detail-label">Onboarded By</span>
              <span class="detail-value">{{ employee.onboarded_by_name }}</span>
            </div>
          </div>
          <div v-if="employee.notes" class="emp-notes">
            <span class="detail-label">Notes</span>
            <p>{{ employee.notes }}</p>
          </div>
          <div class="emp-actions" v-if="canManageEmployee(employee)">
            <button @click="openEditModal(employee)" class="btn btn-sm btn-secondary">Edit</button>
            <button v-if="canOnboard && !isSystemAdmin" @click="openOffboardModal(employee)" class="btn btn-sm btn-warning">Request Offboard</button>
            <button v-if="isSystemAdmin && currentUserId !== employee.user" @click="confirmDelete(employee)" class="btn btn-sm btn-danger">Delete</button>
          </div>
        </div>
      </div>
    </div>

    <div v-else-if="activeTab === 'onboard'">
      <div class="onboard-container">
        <div class="onboard-header">
          <h2>Onboard New Employee</h2>
          <p class="text-muted">Create a new employee account. Role assignment is restricted by your hierarchy level.</p>
          <div v-if="allowedRoles.length" class="hierarchy-info">
            <svg width="16" height="16" fill="none" stroke="var(--blue-500)" stroke-width="2"><circle cx="8" cy="8" r="7"/><path d="M8 5v3M8 10h.01"/></svg>
            <span>You can onboard: <strong>{{ allowedRoles.map(r => getRoleLabel(r)).join(', ') }}</strong></span>
          </div>
        </div>

        <form @submit.prevent="saveEmployee" class="onboard-form">

          <div class="form-section">
            <h4 class="section-title">Basic Information</h4>

            <div v-if="isSystemAdmin" class="form-group" style="margin-bottom:1rem">
              <label class="form-label">Company *</label>
              <input 
                v-model="form.company_name" 
                list="company-suggestions" 
                class="form-input" 
                placeholder="Type or select a company" 
                required
              />
              <datalist id="company-suggestions">
                <option v-for="company in allCompanySuggestions" :key="company" :value="company">{{ company }}</option>
              </datalist>
              <span class="form-hint">As admin, you can onboard employees to any company (type custom name if not listed)</span>
            </div>
            <div class="form-grid-2">
              <div class="form-group">
                <label class="form-label">First Name *</label>
                <input v-model="form.first_name" type="text" class="form-input" required>
              </div>
              <div class="form-group">
                <label class="form-label">Last Name *</label>
                <input v-model="form.last_name" type="text" class="form-input" required>
              </div>
            </div>
            <div class="form-grid-2">
              <div class="form-group">
                <label class="form-label">Email *</label>
                <input v-model="form.email" @input="syncUsernameFromEmail" type="email" class="form-input" required>
              </div>
              <div class="form-group">
                <label class="form-label">Password *</label>
                <input v-model="form.password" type="password" class="form-input" required minlength="8">
                <span class="form-hint">Min 8 characters. Must be unique (cannot match your password).</span>
              </div>
            </div>
            <div class="form-grid-2">
              <div class="form-group">
                <label class="form-label">Role *</label>
                <select v-model="form.role" class="form-input" required>
                  <option v-for="role in allowedRoles" :key="role" :value="role">{{ getRoleLabel(role) }}</option>
                </select>
              </div>
              <div class="form-group">
                <label class="form-label">Reports To</label>
                <select v-model="form.reports_to" class="form-input">
                  <option :value="null">— None (auto-assign) —</option>
                  <option v-for="mgr in managerOptions" :key="mgr.user" :value="mgr.user">{{ mgr.full_name || mgr.username }} ({{ getRoleLabel(mgr.role) }})</option>
                </select>
                <span class="form-hint">Defaults to you if left empty</span>
              </div>
            </div>
          </div>

          <div class="form-section">
            <h4 class="section-title">Position Details</h4>
            <div class="form-grid-2">
              <div class="form-group">
                <label class="form-label">Job Title</label>
                <input v-model="form.job_title" type="text" class="form-input" placeholder="e.g., IT Manager">
              </div>
              <div class="form-group">
                <label class="form-label">Department</label>
                <input v-model="form.department" type="text" class="form-input" placeholder="e.g., Information Technology">
              </div>
            </div>
            <div class="form-grid-2">
              <div class="form-group">
                <label class="form-label">Division {{ form.role && ['manager', 'supervisor', 'user'].includes(form.role) ? '*' : '' }}</label>
                <select v-model="form.division" class="form-input" :required="form.role && ['manager', 'supervisor', 'user'].includes(form.role)">
                  <option :value="null">— Select Division —</option>
                  <option v-for="div in divisions" :key="div.id" :value="div.id">{{ div.name }}</option>
                </select>
                <span class="form-hint" v-if="form.role && ['manager', 'supervisor', 'user'].includes(form.role)">Required for non-admin roles</span>
              </div>
              <div class="form-group">
                <label class="form-label">Employee ID</label>
                <input v-model="form.employee_id" type="text" class="form-input" placeholder="e.g., EMP001">
              </div>
            </div>
            <div class="form-grid-2">
              <div class="form-group">
                <label class="form-label">Phone</label>
                <input v-model="form.phone" type="tel" class="form-input">
              </div>
              <div class="form-group">
                <label class="form-label">Start Date</label>
                <input v-model="form.start_date" type="date" class="form-input">
              </div>
              <div class="form-group">
                <label class="form-label">Date of Birth</label>
                <input v-model="form.date_of_birth" type="date" class="form-input">
              </div>
            </div>
          </div>

          <div class="form-section">
            <h4 class="section-title">Personal Details</h4>
            <div class="form-group">
              <label class="form-label">Address</label>
              <textarea v-model="form.address" rows="2" class="form-input" placeholder="Physical address"></textarea>
            </div>
            <div class="form-grid-2">
              <div class="form-group">
                <label class="form-label">Emergency Contact</label>
                <input v-model="form.emergency_contact_name" type="text" class="form-input" placeholder="Full name">
              </div>
              <div class="form-group">
                <label class="form-label">Emergency Phone</label>
                <input v-model="form.emergency_contact_phone" type="tel" class="form-input" placeholder="Phone number">
              </div>
            </div>
            <div class="form-group">
              <label class="form-label">Notes</label>
              <textarea v-model="form.notes" rows="2" class="form-input" placeholder="Additional information"></textarea>
            </div>
          </div>

          <div class="form-actions">
            <button type="button" @click="resetForm" class="btn btn-secondary">Clear Form</button>
            <button type="submit" class="btn btn-primary" :disabled="saving || remainingSlots === 0">
              {{ saving ? 'Onboarding...' : 'Onboard Employee' }}
            </button>
          </div>
        </form>
      </div>
    </div>

    <div v-else-if="activeTab === 'offboarding'">
      <div class="offboard-container">
        <div class="offboard-header">
          <h2>Offboarding Requests</h2>
          <p class="text-muted">
            {{ isSystemAdmin
              ? 'Process offboarding requests from company CEOs and Executives.'
              : 'Request employee offboarding — system administrators will process the request.' }}
          </p>
        </div>

        <div class="filter-bar" style="margin-bottom:1rem">
          <select v-model="offboardStatusFilter" class="form-input filter-select" @change="loadOffboardingRequests">
            <option value="">All Statuses</option>
            <option value="pending">Pending</option>
            <option value="approved">Approved</option>
            <option value="rejected">Rejected</option>
          </select>
        </div>

        <div v-if="offboardLoading" style="text-align:center;padding:2rem"><span class="spinner"></span></div>
        <div v-else-if="offboardingRequests.length === 0" class="empty-state">
          <svg width="40" height="40" fill="none" stroke="var(--gray-400)" stroke-width="1.5"><path d="M12 8h16M8 14h24M12 20h16M8 26h24"/></svg>
          <h3>No Offboarding Requests</h3>
          <p>No offboarding requests found{{ offboardStatusFilter ? ' with this status' : '' }}.</p>
        </div>
        <div v-else class="offboard-list">
          <div v-for="req in offboardingRequests" :key="req.id" class="offboard-card card">
            <div class="offboard-top">
              <div>
                <h4 class="offboard-name">{{ req.employee_name }}</h4>
                <p class="offboard-email">{{ req.employee_email }}</p>
              </div>
              <span class="badge" :class="statusBadge(req.status)">{{ req.status_display || req.status }}</span>
            </div>
            <div class="offboard-details">
              <div class="detail-row">
                <span class="detail-label">Requested By</span>
                <span class="detail-value">{{ req.requested_by_name }}</span>
              </div>
              <div class="detail-row">
                <span class="detail-label">Company</span>
                <span class="detail-value">{{ req.company_name }}</span>
              </div>
              <div class="detail-row">
                <span class="detail-label">Reason</span>
                <span class="detail-value">{{ req.reason }}</span>
              </div>
              <div class="detail-row">
                <span class="detail-label">Submitted</span>
                <span class="detail-value">{{ formatDateTime(req.created_at) }}</span>
              </div>
              <div v-if="req.processed_by_name" class="detail-row">
                <span class="detail-label">Processed By</span>
                <span class="detail-value">{{ req.processed_by_name }}</span>
              </div>
              <div v-if="req.admin_notes" class="detail-row">
                <span class="detail-label">Admin Notes</span>
                <span class="detail-value">{{ req.admin_notes }}</span>
              </div>
            </div>

            <div v-if="isSystemAdmin && req.status === 'pending'" class="offboard-actions">
              <div class="form-group" style="margin-bottom:.5rem">
                <input v-model="req._adminNotes" type="text" class="form-input" placeholder="Admin notes (optional)">
              </div>
              <div style="display:flex;gap:.5rem">
                <button @click="processOffboard(req, 'approve')" class="btn btn-sm btn-primary" :disabled="processingOffboard">Approve</button>
                <button @click="processOffboard(req, 'reject')" class="btn btn-sm btn-danger" :disabled="processingOffboard">Reject</button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div v-else-if="activeTab === 'logs'">
      <div class="logs-container">
        <div class="logs-header">
          <h2>Activity Log</h2>
          <p class="text-muted">Complete onboarding and offboarding audit trail.</p>
        </div>

        <div class="filter-bar" style="margin-bottom:1rem">
          <select v-model="logActionFilter" class="form-input filter-select" @change="loadOnboardingLogs">
            <option value="">All Actions</option>
            <option value="onboard">Onboarded</option>
            <option value="offboard">Offboarded</option>
          </select>
        </div>

        <div v-if="logsLoading" style="text-align:center;padding:2rem"><span class="spinner"></span></div>
        <div v-else-if="onboardingLogs.length === 0" class="empty-state">
          <svg width="40" height="40" fill="none" stroke="var(--gray-400)" stroke-width="1.5"><path d="M6 6h28v28H6z"/><path d="M12 14h16M12 20h10"/></svg>
          <h3>No Activity Logs</h3>
          <p>Onboarding and offboarding events will appear here.</p>
        </div>
        <div v-else class="logs-table-wrap">
          <table class="logs-table">
            <thead>
              <tr>
                <th>Action</th>
                <th>Employee</th>
                <th>Email</th>
                <th>Role</th>
                <th>Performed By</th>
                <th>Date</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="log in onboardingLogs" :key="log.id" :class="{ 'log-offboard': log.action === 'offboard' }">
                <td>
                  <span class="badge" :class="log.action === 'onboard' ? 'badge-green' : 'badge-red'">
                    {{ log.action_display || log.action }}
                  </span>
                </td>
                <td>{{ log.employee_name }}</td>
                <td>{{ log.employee_email }}</td>
                <td>{{ log.role_assigned ? getRoleLabel(log.role_assigned) : '—' }}</td>
                <td>{{ log.performed_by_name }}</td>
                <td>{{ formatDateTime(log.created_at) }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <div v-if="showEditModal" class="modal-overlay" @click="showEditModal = false">
      <div class="modal-panel modal-lg" @click.stop>
        <div class="modal-header">
          <h3>Edit Employee</h3>
          <button class="modal-close" @click="showEditModal = false">&times;</button>
        </div>
        <div class="modal-body">
          <form @submit.prevent="updateEmployee">
            <div class="form-grid-2">
              <div class="form-group">
                <label class="form-label">First Name</label>
                <input v-model="editForm.first_name" type="text" class="form-input">
              </div>
              <div class="form-group">
                <label class="form-label">Last Name</label>
                <input v-model="editForm.last_name" type="text" class="form-input">
              </div>
            </div>
            <div class="form-grid-2">
              <div class="form-group">
                <label class="form-label">Role</label>
                <select v-model="editForm.role" class="form-input">
                  <option v-for="role in editAllowedRoles" :key="role" :value="role">{{ getRoleLabel(role) }}</option>
                </select>
              </div>
              <div class="form-group">
                <label class="form-label">Job Title</label>
                <input v-model="editForm.job_title" type="text" class="form-input">
              </div>
            </div>
            <div class="form-grid-2">
              <div class="form-group">
                <label class="form-label">Department</label>
                <input v-model="editForm.department" type="text" class="form-input">
              </div>
              <div class="form-group">
                <label class="form-label">Phone</label>
                <input v-model="editForm.phone" type="tel" class="form-input">
              </div>
            </div>
            <div class="form-group">
              <label class="form-label">Notes</label>
              <textarea v-model="editForm.notes" rows="2" class="form-input"></textarea>
            </div>
            <div class="modal-footer" style="padding:0;border:none;margin-top:1.5rem">
              <button type="button" @click="showEditModal = false" class="btn btn-secondary">Cancel</button>
              <button type="submit" class="btn btn-primary" :disabled="saving">{{ saving ? 'Saving...' : 'Update' }}</button>
            </div>
          </form>
        </div>
      </div>
    </div>

    <div v-if="showDeleteConfirm" class="modal-overlay" @click="showDeleteConfirm = false">
      <div class="modal-panel modal-sm" @click.stop>
        <div class="modal-header"><h3>Confirm Delete</h3></div>
        <div class="modal-body" style="text-align:center">
          <p>Are you sure you want to delete <strong>{{ employeeToDelete?.full_name }}</strong>?</p>
          <p style="color:var(--red-500);font-size:.8125rem">This action cannot be undone. An offboarding log will be recorded.</p>
        </div>
        <div class="modal-footer">
          <button @click="showDeleteConfirm = false" class="btn btn-secondary">Cancel</button>
          <button @click="deleteEmployee" class="btn btn-danger">Delete Employee</button>
        </div>
      </div>
    </div>

    <div v-if="showOffboardModal" class="modal-overlay" @click="showOffboardModal = false">
      <div class="modal-panel modal-sm" @click.stop>
        <div class="modal-header">
          <h3>Request Offboarding</h3>
          <button class="modal-close" @click="showOffboardModal = false">&times;</button>
        </div>
        <div class="modal-body">
          <p style="font-size:.875rem;margin-bottom:1rem">
            Request offboarding for <strong>{{ offboardTarget?.full_name }}</strong>.
            A system administrator will review and process this request.
          </p>
          <div class="form-group">
            <label class="form-label">Reason *</label>
            <textarea v-model="offboardReason" rows="3" class="form-input" placeholder="Provide a reason for offboarding (minimum 10 characters)" required minlength="10"></textarea>
          </div>
        </div>
        <div class="modal-footer">
          <button @click="showOffboardModal = false" class="btn btn-secondary">Cancel</button>
          <button @click="submitOffboardRequest" class="btn btn-warning" :disabled="offboardReason.length < 10 || submittingOffboard">
            {{ submittingOffboard ? 'Submitting...' : 'Submit Request' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { employeesAPI, authAPI, divisionsAPI } from '../api'
import authService from '../services/auth'
import toast from '../utils/toast'

export default {
  name: 'Employees',
  data() {
    return {
      
      employees: [],
      divisions: [],  
      loading: false,
      saving: false,
      activeTab: 'directory',
      currentUserId: null,
      remainingSlots: 0,
      maxUsers: '-',
      
      majorSACompanies: [
        'Discovery', 'Sasol', 'MTN', 'Vodacom', 'Capitec Bank', 'Standard Bank',
        'Nedbank', 'Absa', 'FirstRand', 'Old Mutual', 'Sanlam', 'Shoprite',
        'Pick n Pay', 'Woolworths', 'Mr Price', 'Clicks', 'Dis-Chem', 'Massmart',
        'Tiger Brands', 'AVI Limited', 'RCL Foods', 'Bidvest', 'Imperial Logistics',
        'Transnet', 'Eskom', 'Telkom', 'MultiChoice', 'Naspers', 'Prosus',
        'Anglo American', 'Gold Fields', 'Sibanye-Stillwater', 'Harmony Gold',
        'AngloGold Ashanti', 'Kumba Iron Ore', 'African Rainbow Minerals',
        'Murray & Roberts', 'Aveng', 'WBHO', 'Stefanutti Stocks',
        'Liberty Holdings', 'Momentum Metropolitan', 'Alexander Forbes',
        'Rand Merchant Investment', 'Investec', 'PSG Group', 'Coronation Fund Managers',
        'Barloworld', 'Super Group', 'Grindrod', 'City Lodge Hotels', 'Sun International',
        'Tsogo Sun', 'Life Healthcare', 'Mediclinic', 'Netcare', 'Aspen Pharmacare',
        'Adcock Ingram', 'Remgro', 'PSG Konsult', 'RMB Holdings', 'Reunert',
        'Trustco Group', 'Famous Brands', 'Spur Corporation', 'Taste Holdings'
      ],
      
      searchQuery: '',
      roleFilter: '',
      
      form: this.getEmptyForm(),
      
      showEditModal: false,
      editForm: {},
      
      showDeleteConfirm: false,
      employeeToDelete: null,
      
      showOffboardModal: false,
      offboardTarget: null,
      offboardReason: '',
      submittingOffboard: false,
      
      offboardingRequests: [],
      offboardLoading: false,
      offboardStatusFilter: '',
      processingOffboard: false,
      pendingOffboardCount: 0,
      
      onboardingLogs: [],
      logsLoading: false,
      logActionFilter: '',
    }
  },
  computed: {
    isSystemAdmin() {
      const user = authService.getUser() || {}
      return user.is_superuser === true || user.is_staff === true
    },
    myRole() {
      const user = authService.getUser() || {}
      if (user.role) return typeof user.role === 'object' ? user.role.value : user.role
      if (user.profile?.role) return user.profile.role
      if (user.permissions?.is_admin) return 'admin'
      return 'user'
    },
    canOnboard() {
      if (this.isSystemAdmin) return true
      return ['admin', 'executive', 'manager'].includes(this.myRole)
    },
    allowedRoles() {
      if (this.isSystemAdmin) return ['admin', 'executive', 'manager', 'supervisor', 'user']
      const hierarchy = {
        admin: ['executive', 'manager', 'supervisor', 'user'],
        executive: ['manager', 'supervisor', 'user'],
        manager: ['supervisor', 'user'],
      }
      return hierarchy[this.myRole] || []
    },
    editAllowedRoles() {
      
      if (this.isSystemAdmin) return ['admin', 'executive', 'manager', 'supervisor', 'user']
      const base = this.allowedRoles.slice()
      if (this.editForm.role && !base.includes(this.editForm.role)) base.unshift(this.editForm.role)
      return base
    },
    allCompanySuggestions() {
      
      const companies = new Set(this.majorSACompanies)
      this.employees.forEach(e => {
        if (e.company_name) companies.add(e.company_name)
      })
      this.divisions.forEach(d => {
        if (d.company_name) companies.add(d.company_name)
      })
      return Array.from(companies).sort()
    },
    managerOptions() {
      
      const user = authService.getUser() || {}
      const myCompany = (user.company_name || '').toLowerCase()
      
      return this.employees.filter(e => {
        const role = this.getRoleValue(e.role)
        if (!['admin', 'executive', 'manager'].includes(role)) return false
        
        
        if (!user.is_superuser && !user.is_staff) {
          const empCompany = (e.company_name || '').toLowerCase()
          if (empCompany !== myCompany) return false
        }
        
        return true
      })
    },
    filteredEmployees() {
      let list = this.employees
      if (this.roleFilter) {
        list = list.filter(e => this.getRoleValue(e.role) === this.roleFilter)
      }
      if (this.searchQuery) {
        const q = this.searchQuery.toLowerCase()
        list = list.filter(e =>
          (e.full_name || '').toLowerCase().includes(q) ||
          (e.username || '').toLowerCase().includes(q) ||
          (e.email || '').toLowerCase().includes(q) ||
          (e.job_title || '').toLowerCase().includes(q) ||
          (e.department || '').toLowerCase().includes(q) ||
          (e.employee_id || '').toLowerCase().includes(q)
        )
      }
      return list
    },
  },
  watch: {
    activeTab(tab) {
      if (tab === 'offboarding') this.loadOffboardingRequests()
      if (tab === 'logs') this.loadOnboardingLogs()
    }
  },
  mounted() {
    this.loadEmployees()
    this.loadDivisions()  
    this.loadAvailableSlots()
    this.loadPendingOffboardCount()
    const user = authService.getUser() || {}
    this.currentUserId = user.id || null
    
    authAPI.getProfile().then(resp => {
      if (resp?.data) authService.setUser(resp.data)
    }).catch(() => {})
  },
  methods: {
    // ── Helpers ──
    getRoleValue(role) {
      if (typeof role === 'object' && role?.value) return role.value
      return role || 'user'
    },
    getRoleLabel(role) {
      const r = this.getRoleValue(role)
      const labels = { admin: 'CEO / Admin', executive: 'Executive', manager: 'Manager', supervisor: 'Supervisor', user: 'Standard Employee' }
      return labels[r] || r
    },
    roleBadge(role) {
      const r = this.getRoleValue(role)
      const m = { admin: 'badge-red', executive: 'badge-purple', manager: 'badge-amber', supervisor: 'badge-blue', user: 'badge-gray' }
      return m[r] || 'badge-gray'
    },
    statusBadge(status) {
      const m = { pending: 'badge-amber', approved: 'badge-green', rejected: 'badge-red' }
      return m[status] || 'badge-gray'
    },
    onboardingStatusBadge(status) {
      const m = {
        pending_first_login: 'badge-amber',
        onboarded: 'badge-green',
        offboarded: 'badge-gray'
      }
      return m[status] || 'badge-gray'
    },
    getInitials(employee) {
      if (employee.first_name && employee.last_name) return `${employee.first_name[0]}${employee.last_name[0]}`.toUpperCase()
      return (employee.username || '??').substring(0, 2).toUpperCase()
    },
    formatDate(d) {
      if (!d) return ''
      return new Date(d).toLocaleDateString('en-ZA', { year: 'numeric', month: 'short', day: 'numeric' })
    },
    formatDateTime(d) {
      if (!d) return ''
      return new Date(d).toLocaleString('en-ZA', { year: 'numeric', month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit' })
    },
    countByRole(role) {
      return this.employees.filter(e => this.getRoleValue(e.role) === role).length
    },
    canManageEmployee(employee) {
      if (this.isSystemAdmin) return true
      if (!this.canOnboard) return false
      if (employee.user === this.currentUserId) return false
      return true
    },
    getEmptyForm() {
      return {
        username: '', email: '', first_name: '', last_name: '', role: 'user', password: '',
        phone: '', job_title: '', department: '', employee_id: '', date_of_birth: null,
        address: '', emergency_contact_name: '', emergency_contact_phone: '',
        start_date: null, notes: '', reports_to: null, division: null, company_name: '',
      }
    },
    resetForm() { this.form = this.getEmptyForm() },
    syncUsernameFromEmail() { this.form.username = (this.form.email || '').trim().toLowerCase() },
    normalizeDateInput(value) {
      if (!value) return null
      if (typeof value !== 'string') return value
      return value.replace(/\//g, '-')
    },
    extractApiErrorMessage(error) {
      const data = error?.response?.data
      if (!data) return 'Failed to onboard employee'
      if (typeof data === 'string') return data
      if (data.error) return data.error
      if (data.message) return data.message

      const fieldErrors = []
      Object.entries(data).forEach(([field, value]) => {
        if (Array.isArray(value) && value.length > 0) {
          fieldErrors.push(`${field}: ${value.join(', ')}`)
        } else if (typeof value === 'string') {
          fieldErrors.push(`${field}: ${value}`)
        }
      })
      return fieldErrors.length ? fieldErrors.join(' | ') : 'Failed to onboard employee'
    },

    // ── Data Loading ──
    async loadEmployees(retryCount = 0) {
      this.loading = true
      try {
        const response = await employeesAPI.getAll()
        this.employees = response.data
      } catch (error) {
        if (retryCount < 2) {
          setTimeout(() => this.loadEmployees(retryCount + 1), 3000)
          return
        }
        toast.error('Load Failed', 'Failed to load employees')
      } finally {
        this.loading = false
      }
    },
    async loadDivisions() {
      
      try {
        const response = await divisionsAPI.getAll()
        this.divisions = response.data
      } catch (error) {
        console.error('Failed to load divisions:', error)
      }
    },
    async loadAvailableSlots() {
      try {
        const response = await employeesAPI.getAvailableSlots()
        this.remainingSlots = response.data.remaining_slots ?? '-'
        this.maxUsers = response.data.max_users
      } catch (e) { /* silent */ }
    },
    async loadPendingOffboardCount() {
      try {
        const response = await employeesAPI.getOffboardingRequests({ status: 'pending' })
        this.pendingOffboardCount = response.data.length
      } catch (e) { /* silent */ }
    },
    async loadOffboardingRequests() {
      this.offboardLoading = true
      try {
        const params = {}
        if (this.offboardStatusFilter) params.status = this.offboardStatusFilter
        const response = await employeesAPI.getOffboardingRequests(params)
        this.offboardingRequests = response.data.map(r => ({ ...r, _adminNotes: '' }))
      } catch (error) {
        toast.error('Load Failed', 'Failed to load offboarding requests')
      } finally {
        this.offboardLoading = false
      }
    },
    async loadOnboardingLogs() {
      this.logsLoading = true
      try {
        const params = {}
        if (this.logActionFilter) params.action = this.logActionFilter
        const response = await employeesAPI.getOnboardingLogs(params)
        this.onboardingLogs = response.data
      } catch (error) {
        toast.error('Load Failed', 'Failed to load activity logs')
      } finally {
        this.logsLoading = false
      }
    },

    // ── Onboarding (Create) ──
    async saveEmployee() {
      this.saving = true
      try {
        this.syncUsernameFromEmail()
        const payload = {
          ...this.form,
          date_of_birth: this.normalizeDateInput(this.form.date_of_birth),
          start_date: this.normalizeDateInput(this.form.start_date),
        }
        await employeesAPI.create(payload)
        toast.success('Employee Onboarded', 'New employee has been onboarded successfully.')
        this.resetForm()
        this.loadEmployees()
        this.loadAvailableSlots()
        this.activeTab = 'directory'
      } catch (error) {
        const msg = this.extractApiErrorMessage(error)
        toast.error('Onboarding Failed', msg)
      } finally {
        this.saving = false
      }
    },

    // ── Edit ──
    openEditModal(employee) {
      this.editForm = {
        id: employee.id,
        first_name: employee.first_name,
        last_name: employee.last_name,
        role: this.getRoleValue(employee.role),
        job_title: employee.job_title || '',
        department: employee.department || '',
        phone: employee.phone || '',
        notes: employee.notes || '',
      }
      this.showEditModal = true
    },
    async updateEmployee() {
      this.saving = true
      try {
        await employeesAPI.partialUpdate(this.editForm.id, this.editForm)
        toast.success('Updated', 'Employee details updated successfully.')
        this.showEditModal = false
        this.loadEmployees()
      } catch (error) {
        const msg = error.response?.data?.error || 'Failed to update employee'
        toast.error('Update Failed', msg)
      } finally {
        this.saving = false
      }
    },

    // ── Delete (System Admin Only) ──
    confirmDelete(employee) {
      this.employeeToDelete = employee
      this.showDeleteConfirm = true
    },
    async deleteEmployee() {
      try {
        await employeesAPI.delete(this.employeeToDelete.id)
        toast.success('Deleted', 'Employee has been removed.')
        this.showDeleteConfirm = false
        this.employeeToDelete = null
        this.loadEmployees()
        this.loadAvailableSlots()
      } catch (error) {
        toast.error('Delete Failed', error.response?.data?.error || 'Failed to delete')
      }
    },

    // ── Offboarding Request ──
    openOffboardModal(employee) {
      this.offboardTarget = employee
      this.offboardReason = ''
      this.showOffboardModal = true
    },
    async submitOffboardRequest() {
      this.submittingOffboard = true
      try {
        await employeesAPI.requestOffboarding({
          employee_id: this.offboardTarget.user,
          reason: this.offboardReason,
        })
        toast.success('Request Submitted', `Offboarding request for ${this.offboardTarget.full_name} has been submitted for review.`)
        this.showOffboardModal = false
        this.loadPendingOffboardCount()
      } catch (error) {
        const msg = error.response?.data?.error || 'Failed to submit offboarding request'
        toast.error('Request Failed', msg)
      } finally {
        this.submittingOffboard = false
      }
    },
    async processOffboard(req, action) {
      this.processingOffboard = true
      try {
        await employeesAPI.processOffboarding({
          request_id: req.id,
          action: action,
          admin_notes: req._adminNotes || '',
        })
        toast.success(action === 'approve' ? 'Approved' : 'Rejected',
          action === 'approve' ? `${req.employee_name} has been offboarded.` : `Offboarding rejected for ${req.employee_name}.`)
        this.loadOffboardingRequests()
        this.loadPendingOffboardCount()
        if (action === 'approve') this.loadEmployees()
      } catch (error) {
        toast.error('Process Failed', error.response?.data?.error || 'Failed to process request')
      } finally {
        this.processingOffboard = false
      }
    },
  }
}
</script>

<style scoped>
.employees-page { padding: 1.5rem 2rem; }
.header-right { display: flex; align-items: center; gap: .75rem; }
.admp-badge { font-size: .625rem; font-weight: 700; background: var(--primary-500); color: #fff; padding: 2px 6px; border-radius: 4px; vertical-align: middle; letter-spacing: .05em; }

/* Stats Bar */
.stats-bar { display: grid; grid-template-columns: repeat(auto-fit, minmax(140px, 1fr)); gap: .75rem; margin-bottom: 1.25rem; }
.stat-card { background: var(--card-bg, #fff); border: 1px solid var(--border-color); border-radius: 8px; padding: 1rem; text-align: center; }
.stat-value { font-size: 1.5rem; font-weight: 700; color: var(--gray-900); }
.stat-label { font-size: .75rem; color: var(--gray-500); margin-top: .25rem; text-transform: uppercase; letter-spacing: .03em; }

/* Tabs */
.tab-nav { display: flex; gap: .25rem; border-bottom: 2px solid var(--border-color); margin-bottom: 1.25rem; overflow-x: auto; }
.tab-nav button { display: flex; align-items: center; gap: .375rem; padding: .625rem 1rem; border: none; background: none; cursor: pointer; font-size: .8125rem; font-weight: 500; color: var(--gray-500); border-bottom: 2px solid transparent; margin-bottom: -2px; white-space: nowrap; transition: all .15s; }
.tab-nav button:hover { color: var(--gray-700); }
.tab-nav button.active { color: var(--primary-600); border-bottom-color: var(--primary-500); }

/* Filter bar */
.filter-bar { display: flex; gap: .75rem; margin-bottom: 1rem; }
.search-input { flex: 1; max-width: 400px; }
.filter-select { width: 200px; }

/* Employee grid */
.emp-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(380px, 1fr)); gap: 1rem; }
.emp-card { padding: 0; overflow: hidden; }
.emp-card.emp-inactive { opacity: .6; }
.emp-card.emp-banned { border-color: var(--red-500); }
.emp-top { display: flex; align-items: center; gap: .75rem; padding: 1.25rem 1.25rem .75rem; }
.avatar { width: 42px; height: 42px; border-radius: 50%; background: var(--primary-500); color: #fff; display: flex; align-items: center; justify-content: center; font-weight: 600; font-size: .875rem; flex-shrink: 0; }
.avatar-admin { background: var(--red-500); }
.avatar-executive { background: #7c3aed; }
.avatar-manager { background: var(--amber-500, #f59e0b); }
.avatar-supervisor { background: var(--blue-500); }
.emp-identity { flex: 1; min-width: 0; }
.emp-name { font-size: .9375rem; font-weight: 600; color: var(--gray-900); margin: 0; }
.emp-email { font-size: .8125rem; color: var(--gray-500); margin: .125rem 0 0; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.status-badge { margin-left: .25rem; }
.emp-details { padding: 0 1.25rem; }
.detail-row { display: flex; justify-content: space-between; padding: .375rem 0; border-bottom: 1px solid var(--gray-100); font-size: .8125rem; }
.detail-row:last-child { border-bottom: none; }
.detail-label { color: var(--gray-500); flex-shrink: 0; }
.detail-value { color: var(--gray-800); font-weight: 500; text-align: right; }
.emp-notes { padding: .75rem 1.25rem; border-top: 1px solid var(--border-color); }
.emp-notes .detail-label { display: block; margin-bottom: .25rem; font-size: .75rem; }
.emp-notes p { margin: 0; font-size: .8125rem; color: var(--gray-600); line-height: 1.5; }
.emp-actions { display: flex; gap: .5rem; padding: .75rem 1.25rem; border-top: 1px solid var(--border-color); background: var(--gray-50); }

/* Onboard form */
.onboard-container { max-width: 720px; }
.onboard-header { margin-bottom: 1.5rem; }
.onboard-header h2 { margin: 0 0 .25rem; }
.hierarchy-info { display: flex; align-items: center; gap: .5rem; padding: .625rem .875rem; background: var(--blue-50, #eff6ff); border: 1px solid var(--blue-200, #bfdbfe); border-radius: 8px; font-size: .8125rem; color: var(--blue-700, #1d4ed8); margin-top: .75rem; }
.form-section { margin-bottom: 1.5rem; padding-bottom: 1rem; border-bottom: 1px solid var(--gray-100); }
.form-section:last-of-type { border-bottom: none; margin-bottom: 0; }
.section-title { font-size: .8125rem; font-weight: 600; color: var(--gray-500); text-transform: uppercase; letter-spacing: .04em; margin: 0 0 .75rem; }
.form-grid-2 { display: grid; grid-template-columns: repeat(2, 1fr); gap: 1rem; }
.form-actions { display: flex; gap: .75rem; justify-content: flex-end; margin-top: 1.5rem; }

/* Offboard */
.offboard-container { max-width: 720px; }
.offboard-header { margin-bottom: 1.25rem; }
.offboard-header h2 { margin: 0 0 .25rem; }
.offboard-list { display: flex; flex-direction: column; gap: .75rem; }
.offboard-card { padding: 0; overflow: hidden; }
.offboard-top { display: flex; justify-content: space-between; align-items: center; padding: 1rem 1.25rem; }
.offboard-name { margin: 0; font-size: .9375rem; font-weight: 600; }
.offboard-email { margin: .125rem 0 0; font-size: .8125rem; color: var(--gray-500); }
.offboard-details { padding: 0 1.25rem .75rem; }
.offboard-actions { padding: .75rem 1.25rem; border-top: 1px solid var(--border-color); background: var(--gray-50); }

/* Logs */
.logs-container { max-width: 960px; }
.logs-header { margin-bottom: 1.25rem; }
.logs-header h2 { margin: 0 0 .25rem; }
.logs-table-wrap { overflow-x: auto; }
.logs-table { width: 100%; border-collapse: collapse; font-size: .8125rem; }
.logs-table th { text-align: left; padding: .625rem .75rem; background: var(--gray-50); color: var(--gray-600); font-weight: 600; font-size: .75rem; text-transform: uppercase; letter-spacing: .04em; border-bottom: 2px solid var(--border-color); }
.logs-table td { padding: .625rem .75rem; border-bottom: 1px solid var(--gray-100); color: var(--gray-800); }
.log-offboard { background: var(--red-50, #fef2f2); }

/* Badge colors */
.badge-purple { background: #f3e8ff; color: #7c3aed; }
.badge-green { background: #dcfce7; color: #16a34a; }
.badge-warning, .btn-warning { background: #fef3c7; color: #d97706; border-color: #fcd34d; }
.btn-warning:hover { background: #fde68a; }

/* Modal sizes */
.modal-lg { max-width: 680px; }
.modal-sm { max-width: 460px; }
.text-muted { color: var(--gray-500); font-size: .875rem; margin: 0; }

@media (max-width: 768px) {
  .employees-page { padding: 1rem; }
  .emp-grid { grid-template-columns: 1fr; }
  .form-grid-2 { grid-template-columns: 1fr; }
  .header-right { flex-direction: column; align-items: stretch; }
  .stats-bar { grid-template-columns: repeat(2, 1fr); }
  .filter-bar { flex-direction: column; }
  .filter-select { width: 100%; }
  .search-input { max-width: 100%; }
}
</style>

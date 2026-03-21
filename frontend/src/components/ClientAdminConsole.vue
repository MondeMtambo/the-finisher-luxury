<template>
  <div class="cac-page">
    <div class="page-header">
      <div>
        <h1>Team Management</h1>
        <p class="page-subtitle">Manage your employees and team settings</p>
      </div>
    </div>

    <div class="overview-row">
      <div class="card ov-card">
        <div class="ov-icon blue"><svg width="20" height="20" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="3" width="14" height="14" rx="2"/><path d="M7 7h6M7 10h4"/></svg></div>
        <div>
          <h3 style="font-size:.8125rem;font-weight:500;color:var(--gray-500);margin:0">Your Plan</h3>
          <p style="font-size:1rem;font-weight:700;color:var(--gray-900);margin:.125rem 0 0">{{ tierName }}</p>
          <p style="font-size:.75rem;color:var(--gray-500);margin:.125rem 0 0">Professional CRM with unlimited features</p>
        </div>
      </div>
      <div class="card ov-card" :class="{ 'ov-full': remainingSlots === 0 }">
        <div class="ov-icon green"><svg width="20" height="20" fill="none" stroke="currentColor" stroke-width="2"><circle cx="7" cy="6" r="3"/><circle cx="14" cy="6" r="3"/><path d="M1 17c0-2.2 2.7-4 6-4s6 1.8 6 4M8 17c0-2.2 2.7-4 6-4s6 1.8 6 4"/></svg></div>
        <div style="flex:1">
          <h3 style="font-size:.8125rem;font-weight:500;color:var(--gray-500);margin:0">Team Capacity</h3>
          <p style="font-size:1rem;font-weight:700;color:var(--gray-900);margin:.125rem 0 .375rem">{{ currentUsers }} / {{ maxUsers }} Users</p>
          <div class="cap-bar"><div class="cap-fill" :style="{ width: usagePercentage + '%' }"></div></div>
          <p style="font-size:.75rem;color:var(--gray-500);margin:.25rem 0 0">{{ remainingSlots }} slot{{ remainingSlots !== 1 ? 's' : '' }} available</p>
        </div>
      </div>
      <div class="card ov-card">
        <div class="ov-icon amber"><svg width="20" height="20" fill="none" stroke="currentColor" stroke-width="2"><polyline points="4 14 8 8 12 12 16 4"/></svg></div>
        <div>
          <h3 style="font-size:.8125rem;font-weight:500;color:var(--gray-500);margin:0">Team Stats</h3>
          <div style="display:flex;gap:1.5rem;margin-top:.375rem">
            <div><span style="font-size:1.125rem;font-weight:700;color:var(--gray-900)">{{ adminCount }}</span><br><span style="font-size:.6875rem;color:var(--gray-500)">Admin{{ adminCount !== 1 ? 's' : '' }}</span></div>
            <div><span style="font-size:1.125rem;font-weight:700;color:var(--gray-900)">{{ employeeCount }}</span><br><span style="font-size:.6875rem;color:var(--gray-500)">Employee{{ employeeCount !== 1 ? 's' : '' }}</span></div>
          </div>
        </div>
      </div>
    </div>

    <div style="display:flex;gap:.75rem;margin-bottom:1.5rem;flex-wrap:wrap">
      <button @click="openCreateModal" class="btn btn-primary" :disabled="remainingSlots === 0">
        <svg width="16" height="16" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><line x1="8" y1="3" x2="8" y2="13"/><line x1="3" y1="8" x2="13" y2="8"/></svg>
        Add Employee
      </button>
      <button @click="refreshData" class="btn btn-secondary">Refresh Data</button>
    </div>

    <div class="card" style="padding:0;overflow:hidden">
      <div style="padding:.75rem 1.25rem;border-bottom:1px solid var(--border-color);display:flex;align-items:center;justify-content:space-between">
        <h2 style="font-size:.9375rem;font-weight:600;color:var(--gray-900);margin:0">Your Team Members</h2>
        <span class="badge badge-gray">{{ employees.length }} member{{ employees.length !== 1 ? 's' : '' }}</span>
      </div>

      <div v-if="loading" style="text-align:center;padding:2rem"><span class="spinner"></span></div>

      <div v-else-if="employees.length === 0" class="empty-state" style="padding:2rem">
        <svg width="40" height="40" fill="none" stroke="var(--gray-400)" stroke-width="1.5"><circle cx="20" cy="12" r="7"/><path d="M6 36c0-7.7 6.3-14 14-14s14 6.3 14 14"/></svg>
        <h3>No team members yet</h3>
        <p>Start by adding your first employee</p>
        <button v-if="remainingSlots > 0" @click="openCreateModal" class="btn btn-primary">Add First Employee</button>
      </div>

      <div v-else class="table-wrap">
        <table class="data-table">
          <thead><tr><th>Employee</th><th>Role</th><th>Contact</th><th>Department</th><th>Status</th><th>Actions</th></tr></thead>
          <tbody>
            <tr v-for="employee in employees" :key="employee.id" :class="{ 'row-inactive': !employee.is_active }">
              <td>
                <div style="display:flex;align-items:center;gap:.5rem">
                  <div style="width:32px;height:32px;border-radius:50%;background:var(--primary-500);color:#fff;display:flex;align-items:center;justify-content:center;font-weight:600;font-size:.75rem;flex-shrink:0">{{ getInitials(employee) }}</div>
                  <div><div style="font-weight:600;font-size:.8125rem">{{ employee.full_name || employee.username }}</div><div style="font-size:.75rem;color:var(--gray-500)">@{{ employee.username }}</div></div>
                </div>
              </td>
              <td><span class="badge" :class="getRoleClass(employee.role)">{{ getRoleLabel(employee.role) }}</span></td>
              <td><div style="font-size:.8125rem">{{ employee.email }}</div><div v-if="employee.phone" style="font-size:.75rem;color:var(--gray-500)">{{ employee.phone }}</div></td>
              <td style="font-size:.8125rem">{{ employee.department || '\u2014' }}</td>
              <td><span class="badge" :class="employee.is_active ? 'badge-green' : 'badge-gray'">{{ employee.is_active ? 'Active' : 'Inactive' }}</span></td>
              <td>
                <div style="display:flex;gap:.25rem">
                  <button v-if="currentUserId !== employee.user" @click="openEditModal(employee)" class="btn btn-sm btn-secondary">Edit</button>
                  <button v-if="currentUserId !== employee.user" @click="confirmDelete(employee)" class="btn btn-sm btn-danger">Delete</button>
                  <span v-if="currentUserId === employee.user" class="badge badge-blue" style="font-size:.5625rem">You</span>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <div v-if="remainingSlots === 0" class="info-bar" style="background:#fffbeb;color:var(--amber-500);margin-top:1rem">
      <strong>Team Capacity Reached</strong> &mdash; You've reached the maximum of {{ maxUsers }} users. Contact support for upgrade options.
    </div>

    <div v-if="showModal" class="modal-overlay" @click="closeModal">
      <div class="modal-panel modal-lg" @click.stop>
        <div class="modal-header">
          <h3>{{ isEditMode ? 'Edit Employee' : 'Add New Employee' }}</h3>
          <button class="modal-close" @click="closeModal">&times;</button>
        </div>
        <div class="modal-body">
          <form @submit.prevent="saveEmployee">
            <div class="form-section"><h4 class="section-title">Basic Information</h4>
              <div class="form-grid-2">
                <div class="form-group"><label class="form-label">First Name *</label><input v-model="form.first_name" type="text" class="form-input" required></div>
                <div class="form-group"><label class="form-label">Last Name *</label><input v-model="form.last_name" type="text" class="form-input" required></div>
              </div>
              <div class="form-grid-2">
                <div class="form-group"><label class="form-label">Username *</label><input v-model="form.username" type="text" class="form-input" required :disabled="isEditMode"></div>
                <div class="form-group"><label class="form-label">Email *</label><input v-model="form.email" type="email" class="form-input" required :disabled="isEditMode"></div>
              </div>
              <div class="form-grid-2">
                <div class="form-group"><label class="form-label">Role *</label><select v-model="form.role" class="form-input" required><option value="user">Standard User</option><option value="supervisor">Supervisor</option><option value="manager">Manager</option><option value="admin">Administrator</option></select></div>
                <div class="form-group"><label class="form-label">Phone</label><input v-model="form.phone" type="tel" class="form-input"></div>
              </div>
            </div>
            <div class="form-section"><h4 class="section-title">Position Details</h4>
              <div class="form-grid-2">
                <div class="form-group"><label class="form-label">Job Title</label><input v-model="form.job_title" type="text" class="form-input" placeholder="e.g., Sales Manager"></div>
                <div class="form-group"><label class="form-label">Department</label><input v-model="form.department" type="text" class="form-input" placeholder="e.g., Sales"></div>
              </div>
              <div class="form-grid-2">
                <div class="form-group"><label class="form-label">Employee ID</label><input v-model="form.employee_id" type="text" class="form-input" placeholder="e.g., EMP001"></div>
                <div class="form-group"><label class="form-label">Start Date</label><input v-model="form.start_date" type="date" class="form-input"></div>
              </div>
            </div>
            <div class="form-section"><h4 class="section-title">Personal Details</h4>
              <div class="form-group"><label class="form-label">Date of Birth</label><input v-model="form.date_of_birth" type="date" class="form-input"></div>
              <div class="form-group"><label class="form-label">Address</label><textarea v-model="form.address" rows="2" class="form-input" placeholder="Physical address"></textarea></div>
            </div>
            <div class="form-section"><h4 class="section-title">Emergency Contact</h4>
              <div class="form-grid-2">
                <div class="form-group"><label class="form-label">Contact Name</label><input v-model="form.emergency_contact_name" type="text" class="form-input" placeholder="Full name"></div>
                <div class="form-group"><label class="form-label">Contact Phone</label><input v-model="form.emergency_contact_phone" type="tel" class="form-input" placeholder="Phone number"></div>
              </div>
            </div>
            <div class="form-section"><h4 class="section-title">Notes</h4>
              <div class="form-group"><textarea v-model="form.notes" rows="3" class="form-input" placeholder="Additional information"></textarea></div>
            </div>
            <div class="modal-footer" style="padding:0;border:none;margin-top:1.5rem">
              <button type="button" @click="closeModal" class="btn btn-secondary">Cancel</button>
              <button type="submit" class="btn btn-primary" :disabled="saving">{{ saving ? 'Saving...' : (isEditMode ? 'Update Employee' : 'Create Employee') }}</button>
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
          <p style="color:var(--red-500);font-size:.8125rem">This action cannot be undone.</p>
        </div>
        <div class="modal-footer">
          <button @click="showDeleteConfirm = false" class="btn btn-secondary">Cancel</button>
          <button @click="deleteEmployee" class="btn btn-danger">Delete Employee</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { employeesAPI, authAPI } from '../api'
import authService from '../services/auth'
import toast from '../utils/toast'
import modal from '../utils/modal'

export default {
  name: 'ClientAdminConsole',
  data() {
    return {
      employees: [],
      loading: false,
      saving: false,
      showModal: false,
      showDeleteConfirm: false,
      isEditMode: false,
      currentUserId: null,
      employeeToDelete: null,
      remainingSlots: 0,
      maxUsers: 2,
      currentUsers: 0,
      tierName: 'FINISHER LUXURY',
      form: this.getEmptyForm()
    }
  },
  computed: {
    usagePercentage() {
      return this.maxUsers > 0 ? (this.currentUsers / this.maxUsers) * 100 : 0
    },
    adminCount() {
      return this.employees.filter(e => {
        const role = e.role
        if (typeof role === 'string') return role === 'admin'
        if (typeof role === 'object' && role.value) return role.value === 'admin'
        return false
      }).length
    },
    employeeCount() {
      return this.employees.length - this.adminCount
    }
  },
  mounted() {
    const user = authService.getUser() || {}
    this.currentUserId = user.id || null
    this.tierName = user.tier || 'FINISHER LUXURY'
    
    this.loadEmployees()
    this.loadAvailableSlots()
    
    
    authAPI.getProfile()
      .then(resp => {
        if (resp && resp.data) {
          authService.setUser(resp.data)
          this.tierName = resp.data.tier || 'FINISHER LUXURY'
        }
      })
      .catch(() => {})
  },
  methods: {
    getEmptyForm() {
      return {
        username: '',
        email: '',
        first_name: '',
        last_name: '',
        role: 'user',
        phone: '',
        job_title: '',
        department: '',
        employee_id: '',
        date_of_birth: null,
        address: '',
        emergency_contact_name: '',
        emergency_contact_phone: '',
        start_date: null,
        notes: ''
      }
    },
    
    async loadEmployees() {
      this.loading = true
      try {
        const response = await employeesAPI.getAll()
        this.employees = response.data
      } catch (error) {
        console.error('Error loading employees:', error)
        toast.error('Load Failed', 'Failed to load employees')
      } finally {
        this.loading = false
      }
    },

    async loadAvailableSlots() {
      try {
        const response = await employeesAPI.getAvailableSlots()
        this.remainingSlots = response.data.remaining_slots
        this.currentUsers = response.data.current_users
        this.maxUsers = response.data.max_users
      } catch (error) {
        console.error('Error loading available slots:', error)
      }
    },

    refreshData() {
      this.loadEmployees()
      this.loadAvailableSlots()
    },

    openCreateModal() {
      if (this.remainingSlots === 0) {
        modal.payment('User Limit Reached', 'LUXURY edition allows a maximum of 10 users. Please contact support to upgrade.')
        return
      }
      this.isEditMode = false
      this.form = this.getEmptyForm()
      this.showModal = true
    },

    openEditModal(employee) {
      this.isEditMode = true
      this.form = {
        id: employee.id,
        username: employee.username,
        email: employee.email,
        first_name: employee.first_name,
        last_name: employee.last_name,
        role: employee.role,
        phone: employee.phone || '',
        job_title: employee.job_title || '',
        department: employee.department || '',
        employee_id: employee.employee_id || '',
        date_of_birth: employee.date_of_birth || null,
        address: employee.address || '',
        emergency_contact_name: employee.emergency_contact_name || '',
        emergency_contact_phone: employee.emergency_contact_phone || '',
        start_date: employee.start_date || null,
        notes: employee.notes || ''
      }
      this.showModal = true
    },

    closeModal() {
      this.showModal = false
      this.form = this.getEmptyForm()
    },

    async saveEmployee() {
      this.saving = true
      try {
        if (this.isEditMode) {
          await employeesAPI.update(this.form.id, this.form)
          toast.success('Employee Updated', 'Employee details have been saved successfully.')
        } else {
          await employeesAPI.create(this.form)
          toast.success('Employee Created', 'New employee has been added successfully.')
        }
        this.closeModal()
        this.refreshData()
      } catch (error) {
        console.error('Error saving employee:', error)
        const errorMsg = error.response?.data?.error || error.response?.data?.message || 'Failed to save employee'
        toast.error('Save Failed', errorMsg)
      } finally {
        this.saving = false
      }
    },

    confirmDelete(employee) {
      this.employeeToDelete = employee
      this.showDeleteConfirm = true
    },

    async deleteEmployee() {
      try {
        await employeesAPI.delete(this.employeeToDelete.id)
        toast.success('Employee Deleted', 'Employee has been removed successfully.')
        this.showDeleteConfirm = false
        this.employeeToDelete = null
        this.refreshData()
      } catch (error) {
        console.error('Error deleting employee:', error)
        toast.error('Delete Failed', error.response?.data?.error || 'Failed to delete employee')
      }
    },

    getInitials(employee) {
      if (employee.first_name && employee.last_name) {
        return `${employee.first_name[0]}${employee.last_name[0]}`.toUpperCase()
      }
      return employee.username.substring(0, 2).toUpperCase()
    },

    getRoleLabel(role) {
      const labels = {
        admin: 'Administrator',
        manager: 'Manager',
        supervisor: 'Supervisor',
        user: 'Standard User'
      }
      return labels[role] || role
    },

    getRoleClass(role) {
      return `role-${role}`
    }
  }
}
</script>
<style scoped>
.cac-page { padding: 1.5rem 2rem; }

.overview-row { display: grid; grid-template-columns: repeat(3, 1fr); gap: 1rem; margin-bottom: 1.5rem; }
.ov-card { padding: 1.25rem; display: flex; align-items: flex-start; gap: .75rem; }
.ov-card.ov-full { border-color: var(--amber-500); }
.ov-icon { width: 40px; height: 40px; border-radius: var(--radius-md); display: flex; align-items: center; justify-content: center; flex-shrink: 0; }
.ov-icon.blue  { background: #eff6ff; color: var(--primary-500); }
.ov-icon.green { background: #ecfdf5; color: var(--green-500); }
.ov-icon.amber { background: #fffbeb; color: var(--amber-500); }
.cap-bar { height: 6px; background: var(--gray-200); border-radius: 3px; overflow: hidden; }
.cap-fill { height: 100%; background: var(--primary-500); border-radius: 3px; transition: width .3s; }
.table-wrap { overflow-x: auto; }
.row-inactive { opacity: .6; }
.info-bar { background: #eff6ff; color: var(--primary-500); padding: .75rem 1rem; border-radius: var(--radius-md); font-size: .8125rem; line-height: 1.5; }

.form-section { margin-bottom: 1.5rem; padding-bottom: 1rem; border-bottom: 1px solid var(--gray-100); }
.form-section:last-of-type { border-bottom: none; margin-bottom: 0; }
.section-title { font-size: .8125rem; font-weight: 600; color: var(--gray-500); text-transform: uppercase; letter-spacing: .04em; margin: 0 0 .75rem; }
.form-grid-2 { display: grid; grid-template-columns: repeat(2, 1fr); gap: 1rem; }
.modal-lg { max-width: 680px; }
.modal-sm { max-width: 420px; }

@media (max-width: 768px) {
  .overview-row { grid-template-columns: 1fr; }
  .form-grid-2 { grid-template-columns: 1fr; }
}
</style>

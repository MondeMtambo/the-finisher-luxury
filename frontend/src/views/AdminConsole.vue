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
          <button class="btn btn-gold" @click="openOnboardModal">
            🏢 Onboard New Company
          </button>
          <button class="btn btn-danger" @click="showQuickDelete = true">
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

      <!-- Corporate Access Requests (Executive Authorization Deck) -->
      <div class="section-container">
        <div class="flex-between mb-3" style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 1rem;">
          <div>
            <h2 class="section-title" style="margin-bottom: 0.25rem;">Corporate Access Requests &amp; Executive Approvals</h2>
            <p class="section-subtitle" style="color: #9ca3af; font-size: 0.85rem; margin: 0;">
              Review applicant dossiers and provision enterprise tenant workspaces with 7-Day VIP Executive privileges.
            </p>
          </div>
          <div class="header-badges">
            <span class="badge font-mono" style="font-size: 0.85rem; padding: 0.45rem 1rem; border-radius: 20px; background: rgba(212, 175, 55, 0.15); color: #d4af37; border: 1px solid rgba(212, 175, 55, 0.4);">
              👑 {{ pendingAccessRequestsCount }} PENDING AUTHORIZATION
            </span>
          </div>
        </div>

        <div class="table-container">
          <div v-if="loadingAccessRequests" class="audit-loading" style="padding: 2rem; text-align: center;">
            <div class="spinner"></div>
            <span>Fetching incoming corporate applications from Supabase...</span>
          </div>
          <table v-else-if="corporateAccessRequests.length > 0" class="luxury-table">
            <thead>
              <tr>
                <th>Applicant / Executive</th>
                <th>Company &amp; Sector</th>
                <th>Work Email &amp; Phone</th>
                <th>Physical Headquarters</th>
                <th>CIPC &amp; Tax No.</th>
                <th>Status</th>
                <th>Submitted</th>
                <th>Executive Decision</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="req in corporateAccessRequests" :key="req.id">
                <td>
                  <div style="font-weight: 700; color: #fff;">{{ req.first_name }} {{ req.last_name }}</div>
                  <div style="font-size: 0.78rem; color: #d4af37; margin-top: 0.2rem;">
                    {{ req.job_title }}
                    <span v-if="req.is_ceo" style="margin-left: 0.35rem; background: rgba(212,175,55,0.2); padding: 0.15rem 0.4rem; border-radius: 4px; font-size: 0.72rem;">👑 CEO</span>
                    <span v-else style="margin-left: 0.35rem; background: rgba(255,255,255,0.1); padding: 0.15rem 0.4rem; border-radius: 4px; font-size: 0.72rem;" :title="`Sponsor / Linked CEO: ${req.target_ceo_name || req.executive_sponsor_name || 'N/A'}`">👔 Non-CEO Member</span>
                  </div>
                  <div v-if="!req.is_ceo && req.target_ceo_name" style="font-size: 0.72rem; color: #60a5fa; margin-top: 0.25rem; background: rgba(96,165,250,0.12); padding: 0.15rem 0.45rem; border-radius: 4px; display: inline-block;">
                    🔗 Linked CEO: <strong>{{ req.target_ceo_name }}</strong>
                  </div>
                </td>
                <td>
                  <div style="font-weight: 700; color: #f3f4f6;">{{ req.company_name }}</div>
                  <div style="font-size: 0.78rem; color: #9ca3af;">{{ req.trading_name ? `T/A ${req.trading_name}` : req.industry }}</div>
                </td>
                <td>
                  <div style="font-family: monospace; font-size: 0.82rem; color: #e5e7eb;">{{ req.email }}</div>
                  <div style="font-size: 0.78rem; color: #9ca3af;">{{ req.phone }}</div>
                  <div v-if="req.auto_generated_password" style="font-size: 0.72rem; color: #d4af37; background: rgba(212,175,55,0.12); padding: 0.15rem 0.45rem; border-radius: 4px; margin-top: 0.3rem; font-family: monospace; display: inline-block; border: 1px solid rgba(212,175,55,0.25);" title="Auto-Generated Secure Password">
                    🔑 Auto-Pass: {{ req.auto_generated_password }}
                  </div>
                </td>
                <td>
                  <div style="font-size: 0.82rem; max-width: 200px; line-height: 1.3;" :title="req.physical_address">
                    {{ req.physical_address }}, {{ req.city }}, {{ req.province }} {{ req.postal_code }}
                  </div>
                </td>
                <td>
                  <div style="font-family: monospace; font-size: 0.82rem; color: #d4af37;">
                    {{ req.cipc_number || 'N/A' }}
                  </div>
                  <div style="font-size: 0.75rem; color: #9ca3af;" v-if="req.tax_number">VAT: {{ req.tax_number }}</div>
                </td>
                <td>
                  <span v-if="req.status === 'pending'" style="background: rgba(245, 158, 11, 0.2); color: #f59e0b; border: 1px solid rgba(245, 158, 11, 0.4); padding: 0.25rem 0.6rem; border-radius: 6px; font-size: 0.78rem; font-weight: 700;">
                    Pending Review
                  </span>
                  <span v-else-if="req.status === 'approved'" style="background: rgba(16, 185, 129, 0.2); color: #10b981; border: 1px solid rgba(16, 185, 129, 0.4); padding: 0.25rem 0.6rem; border-radius: 6px; font-size: 0.78rem; font-weight: 700;">
                    ✓ Provisioned
                  </span>
                  <span v-else style="background: rgba(239, 68, 68, 0.2); color: #ef4444; border: 1px solid rgba(239, 68, 68, 0.4); padding: 0.25rem 0.6rem; border-radius: 6px; font-size: 0.78rem; font-weight: 700;">
                    Rejected
                  </span>
                </td>
                <td style="font-size: 0.78rem; color: #9ca3af; white-space: nowrap;">
                  {{ formatAuditTimestamp(req.created_at) }}
                </td>
                <td>
                  <div v-if="req.status === 'pending'" style="display: flex; gap: 0.5rem; flex-wrap: wrap;">
                    <button 
                      class="btn btn-sm btn-gold" 
                      style="font-size: 0.78rem; padding: 0.4rem 0.75rem; background: linear-gradient(135deg, #d4af37, #b48608); color: #000; font-weight: 700; border: none; border-radius: 6px; cursor: pointer;" 
                      :disabled="accessRequestActionLoading === req.id"
                      @click="processAccessRequest(req.id, 'approve', req.company_name, req.email)"
                    >
                      {{ accessRequestActionLoading === req.id ? 'Provisioning...' : '⚡ Approve & Provision' }}
                    </button>
                    <button 
                      class="btn btn-sm btn-secondary" 
                      style="font-size: 0.78rem; padding: 0.4rem 0.6rem; color: #ef4444; border: 1px solid rgba(239, 68, 68, 0.4); background: rgba(239, 68, 68, 0.1); border-radius: 6px; cursor: pointer;" 
                      :disabled="accessRequestActionLoading === req.id"
                      @click="processAccessRequest(req.id, 'reject', req.company_name, req.email)"
                    >
                      ✕ Reject
                    </button>
                  </div>
                  <div v-else-if="req.status === 'approved'" style="font-size: 0.78rem; color: #10b981; font-weight: 600;">
                    Workspace Active ({{ req.created_organization_name || 'Provisioned' }})
                  </div>
                  <div v-else style="font-size: 0.78rem; color: #ef4444;" :title="req.rejection_reason">
                    {{ req.rejection_reason || 'Rejected' }}
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
          <div v-else class="audit-empty" style="padding: 2.5rem; text-align: center; color: #9ca3af;">
            <p>👑 No corporate access requests currently awaiting executive review.</p>
          </div>
        </div>
      </div>

      <!-- User Management (Fleet Command) -->
      <div class="section-container">
        <h2 class="section-title">Fleet Command & User Access</h2>
        <div class="kpi-grid six-cols">
          <div class="kpi-card mini"><div class="kpi-val-mini">{{ userSummary.total_users }}</div><div class="kpi-lbl-mini">Total Users</div></div>
          <div class="kpi-card mini"><div class="kpi-val-mini text-green">{{ userSummary.active_users }}</div><div class="kpi-lbl-mini">Active</div></div>
          <div class="kpi-card mini">
            <div class="kpi-val-mini text-blue">{{ userSummary.trial_users }} <span style="font-size: 0.9rem; color: #a0aec0;">/ 15</span></div>
            <div class="kpi-lbl-mini">7-Day Trial (15 Max)</div>
          </div>
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
        <div class="section-header-flex">
          <div>
            <div class="badge-popia" style="background: rgba(212, 175, 55, 0.15); color: #d4af37; border-color: rgba(212, 175, 55, 0.35);">ENTERPRISE TENANT DIRECTORY</div>
            <h2 class="section-title mb-0">Tenant Workspaces &amp; Corporate Roster</h2>
            <p class="text-muted text-sm mt-1">Manage corporate tenant organizations, onboard requesting businesses, and assign root administrators.</p>
          </div>
          <button class="btn btn-gold btn-sm" @click="openOnboardModal">
            🏢 + Onboard New Company
          </button>
        </div>
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

      <!-- CIPC Business Verifications & Compliance Portal -->
      <div class="section-container">
        <div class="section-header-flex">
          <div>
            <div class="badge-popia" style="background: rgba(212, 175, 55, 0.15); color: #d4af37; border-color: rgba(212, 175, 55, 0.35);">CIPC SOUTH AFRICA COMPLIANCE</div>
            <h2 class="section-title">Tenant Business Verifications &amp; Document Review</h2>
            <p class="text-muted">Review uploaded official CIPC CoR14.3 certificates, proof of address, and director IDs. Verify on BizPortal and approve workspace access.</p>
          </div>
          <button class="btn btn-secondary btn-sm" @click="fetchVerifications" :disabled="loadingVerifications">
            🔄 {{ loadingVerifications ? 'Refreshing...' : 'Refresh Verifications' }}
          </button>
        </div>

        <div class="table-container">
          <table class="luxury-table" v-if="verifications.length">
            <thead>
              <tr>
                <th>Organization &amp; Trading Name</th>
                <th>CIPC Reg Number</th>
                <th>SARS Tax Ref</th>
                <th>Director</th>
                <th>Uploaded Documents</th>
                <th>Status</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="v in verifications" :key="v.id">
                <td>
                  <div class="user-main">{{ v.company_name }}</div>
                  <div v-if="v.trading_name" class="user-sub">T/A {{ v.trading_name }}</div>
                  <div class="text-muted text-sm">Org: {{ v.organization_name }}</div>
                </td>
                <td>
                  <code class="font-mono text-gold">{{ v.cipc_number }}</code>
                </td>
                <td>{{ v.tax_number || '—' }}</td>
                <td>{{ v.director_name || '—' }}</td>
                <td>
                  <div class="doc-links">
                    <a v-if="v.cipc_certificate_url" :href="apiBase.replace('/api', '') + v.cipc_certificate_url" target="_blank" class="doc-link-btn" title="View CIPC Certificate">
                      📄 CIPC Cert
                    </a>
                    <a v-if="v.proof_of_address_url" :href="apiBase.replace('/api', '') + v.proof_of_address_url" target="_blank" class="doc-link-btn" title="View Proof of Address">
                      🏢 Address
                    </a>
                    <a v-if="v.director_id_doc_url" :href="apiBase.replace('/api', '') + v.director_id_doc_url" target="_blank" class="doc-link-btn" title="View Director ID">
                      🪪 Director ID
                    </a>
                    <span v-if="!v.cipc_certificate_url && !v.proof_of_address_url && !v.director_id_doc_url" class="text-muted text-sm">No files</span>
                  </div>
                </td>
                <td>
                  <span v-if="v.status === 'verified'" class="badge badge-success">✓ Verified</span>
                  <span v-else-if="v.status === 'pending'" class="badge badge-warning">⏳ Pending</span>
                  <span v-else class="badge badge-danger">✕ Rejected</span>
                </td>
                <td>
                  <div class="action-flex">
                    <button 
                      v-if="v.status !== 'verified'" 
                      @click="reviewVerification(v.id, 'approve')" 
                      class="btn btn-sm btn-primary"
                      title="Approve and unlock workspace"
                    >
                      ✓ Approve
                    </button>
                    <button 
                      v-if="v.status !== 'rejected'" 
                      @click="reviewVerification(v.id, 'reject')" 
                      class="btn btn-sm btn-danger"
                      title="Reject with notes"
                    >
                      ✕ Reject
                    </button>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
          <div v-else class="audit-empty">
            <p>No tenant business verifications submitted yet.</p>
          </div>
        </div>
      </div>

      <!-- POPIA Section 19 Enterprise Security Audit Trail -->
      <div class="section-container audit-deck-container">
        <div class="section-header-flex">
          <div>
            <div class="badge-popia">POPIA SECTION 19 SAFEGUARD</div>
            <h2 class="section-title">Institutional Security Audit Trail</h2>
            <p class="text-muted">Cryptographic, immutable logging of all logins, data exports, and administrative mutations.</p>
          </div>
          <div class="audit-actions">
            <button class="btn btn-secondary btn-sm" @click="fetchAuditLogs" :disabled="loadingAudit">
              🔄 {{ loadingAudit ? 'Refreshing...' : 'Refresh Logs' }}
            </button>
            <button class="btn btn-gold btn-sm" @click="exportPopiaCert">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4M7 10l5 5 5-5M12 15V3"/></svg>
              Export POPIA Audit Log (CSV)
            </button>
          </div>
        </div>

        <!-- Audit Filters -->
        <div class="audit-filter-bar">
          <div class="filter-group">
            <label>Event Type:</label>
            <select v-model="auditFilterEvent" @change="fetchAuditLogs" class="form-input form-input-sm">
              <option value="">All Security Events</option>
              <option value="AUTH_LOGIN_SUCCESS">Login Success</option>
              <option value="AUTH_LOGIN_FAILED">Login Failed</option>
              <option value="AUTH_LOGOUT">Logout</option>
              <option value="MFA_VERIFIED">MFA Verified</option>
              <option value="DATA_EXPORT">POPIA Data Export</option>
              <option value="PRIVILEGE_CHANGE">Privilege / Plan Change</option>
              <option value="SECURITY_POLICY_VIOLATION">Policy Violation</option>
            </select>
          </div>
          <div class="filter-group">
            <label>Severity:</label>
            <select v-model="auditFilterSeverity" @change="fetchAuditLogs" class="form-input form-input-sm">
              <option value="">All Severities</option>
              <option value="INFO">Informational</option>
              <option value="WARNING">Warning</option>
              <option value="CRITICAL">Critical Alert</option>
            </select>
          </div>
          <div class="filter-group">
            <label>Company / Tenant:</label>
            <select v-model="auditFilterCompany" @change="fetchAuditLogs" class="form-input form-input-sm">
              <option value="">All Companies (Full Immunity)</option>
              <option v-for="c in companiesList" :key="c" :value="c">{{ c }}</option>
            </select>
          </div>
          <div class="filter-group flex-1">
            <label>Search:</label>
            <input type="text" v-model="auditSearch" @input="debounceAuditSearch" placeholder="Search IP, actor, or description..." class="form-input form-input-sm" />
          </div>
        </div>

        <!-- Audit Table -->
        <div class="table-container">
          <div v-if="loadingAudit" class="audit-loading">
            <div class="spinner"></div>
            <span>Fetching encrypted audit records from Supabase...</span>
          </div>
          <table v-else-if="auditLogs.length > 0" class="admin-table">
            <thead>
              <tr>
                <th>Timestamp (UTC)</th>
                <th>Company / Tenant</th>
                <th>Severity</th>
                <th>Event Type</th>
                <th>Actor / User</th>
                <th>IP Address</th>
                <th>Description</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="log in auditLogs" :key="log.id">
                <td class="text-sm font-mono whitespace-nowrap">{{ formatAuditTimestamp(log.timestamp) }}</td>
                <td>
                  <span class="badge badge-gray" style="font-weight: 700; color: #D4AF37;">{{ log.organization_name || 'MTAMBO HOLDINGS' }}</span>
                </td>
                <td>
                  <span :class="`badge-audit badge-${(log.severity || 'info').toLowerCase()}`">{{ log.severity }}</span>
                </td>
                <td>
                  <span class="event-badge">{{ log.event_type_display || log.event_type }}</span>
                </td>
                <td>
                  <strong>{{ log.actor }}</strong>
                </td>
                <td class="font-mono text-sm">
                  <span class="ip-pill">{{ log.ip_address || 'Internal' }}</span>
                </td>
                <td class="text-sm audit-desc">
                  {{ log.description }}
                </td>
              </tr>
            </tbody>
          </table>
          <div v-else class="audit-empty">
            <p>🛡️ No audit events matching current filters. All systems secure.</p>
          </div>
        </div>
      </div>
    </template>

    <!-- MODALS -->
    <!-- Quick Delete Modal -->
    <div v-if="showQuickDelete" class="modal-overlay">
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
    <div v-if="showBanModal" class="modal-overlay">
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
    <div v-if="showPaymentModal" class="modal-overlay">
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
                        <option value="trial">Trial Period (7 days)</option>
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
    <div v-if="showWarningDetailsModal" class="modal-overlay">
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

    <!-- Onboard Corporate Tenant Modal -->
    <div v-if="showOnboardModal" class="modal-overlay">
      <div class="modal-panel luxury-modal" style="max-width: 650px;">
        <div class="modal-header">
          <div class="modal-title-wrap">
            <span class="modal-badge-tag" style="color: #d4af37; font-size: 0.7rem; font-weight: 800; letter-spacing: 0.1em;">CORPORATE TENANT PROVISIONING</span>
            <h3 style="margin: 0; color: #fff; font-size: 1.35rem;">🏢 Onboard New Company</h3>
            <p class="text-muted text-sm mt-1 mb-0">Provision an isolated workspace for a business that requested access.</p>
          </div>
          <button class="modal-close" @click="closeOnboardModal">×</button>
        </div>
        <div class="modal-body" style="padding: 1.5rem;">
          <div v-if="onboardSuccessCredentials" class="alert-box success-box mb-4" style="background: rgba(34, 197, 94, 0.15); border: 1px solid rgba(34, 197, 94, 0.4); padding: 1.25rem; border-radius: 8px;">
            <h4 style="margin: 0 0 0.5rem 0; color: #86efac; font-size: 1.1rem;">✓ Workspace Provisioned Successfully!</h4>
            <p class="text-sm" style="color: #d1d5db; margin-bottom: 0.75rem;">Share these credentials with the client administrator to log in:</p>
            <div style="background: rgba(0,0,0,0.4); padding: 0.85rem; border-radius: 6px; font-family: monospace; font-size: 0.85rem; line-height: 1.6; color: #e5e7eb;">
              <div><strong>Company:</strong> {{ onboardSuccessCredentials.company_name }}</div>
              <div><strong>Login URL:</strong> https://www.thefinishercrm.tech</div>
              <div><strong>Login Email:</strong> {{ onboardSuccessCredentials.email }}</div>
              <div><strong>Initial Password:</strong> <span style="color: #facc15; font-weight: 700;">{{ onboardSuccessCredentials.password }}</span></div>
              <div><strong>Subscription Tier:</strong> {{ onboardSuccessCredentials.subscription_tier }}</div>
            </div>
            <button class="btn btn-sm btn-secondary mt-3" @click="copyCredentials">📋 Copy Credentials to Clipboard</button>
          </div>

          <form v-else @submit.prevent="submitOnboardCompany">
            <div v-if="onboardError" class="alert alert-danger mb-3" style="background: rgba(239, 68, 68, 0.15); border: 1px solid rgba(239, 68, 68, 0.4); color: #fca5a5; padding: 0.75rem; border-radius: 6px;">{{ onboardError }}</div>

            <div class="form-row-2col">
              <div class="form-group">
                <label class="form-label">Company Legal Name *</label>
                <input class="form-input" v-model="onboardForm.company_name" placeholder="e.g. Apex Logistics (Pty) Ltd" required />
              </div>
              <div class="form-group">
                <label class="form-label">Trading Name (T/A)</label>
                <input class="form-input" v-model="onboardForm.trading_name" placeholder="e.g. Apex Freight" />
              </div>
            </div>

            <div class="form-row-2col">
              <div class="form-group">
                <label class="form-label">CIPC Registration Number</label>
                <input class="form-input font-mono" v-model="onboardForm.cipc_number" placeholder="2024/123456/07" />
              </div>
              <div class="form-group">
                <label class="form-label">SARS Tax / VAT Reference</label>
                <input class="form-input font-mono" v-model="onboardForm.tax_number" placeholder="4123456789" />
              </div>
            </div>

            <div class="section-divider my-3" style="border-top: 1px solid rgba(255,255,255,0.08); padding-top: 0.75rem; margin: 1rem 0;">
              <span style="color: #d4af37; font-weight: 700; font-size: 0.85rem;">PRIMARY ROOT ADMINISTRATOR (CEO / DIRECTOR)</span>
            </div>

            <div class="form-row-2col">
              <div class="form-group">
                <label class="form-label">Director / Admin Full Name *</label>
                <input class="form-input" v-model="onboardForm.admin_name" placeholder="e.g. David Smith" required />
              </div>
              <div class="form-group">
                <label class="form-label">Corporate Email (Login Username) *</label>
                <input class="form-input" type="email" v-model="onboardForm.admin_email" placeholder="e.g. david@apexlogistics.co.za" required />
              </div>
            </div>

            <div class="form-row-2col">
              <div class="form-group">
                <label class="form-label">Direct Contact Landline/Mobile</label>
                <input class="form-input" v-model="onboardForm.admin_phone" placeholder="+27 82 123 4567" />
              </div>
              <div class="form-group">
                <label class="form-label">Subscription Tier / License</label>
                <select class="form-input" v-model="onboardForm.subscription_tier">
                  <option value="trial">7-Day VIP Trial (15 Max Cohort)</option>
                  <option value="luxury">The Finisher Luxury Private OS</option>
                  <option value="enterprise">Enterprise Custom Retainer</option>
                </select>
              </div>
            </div>

            <div class="form-group">
              <label class="form-label">Initial Password</label>
              <div style="display: flex; gap: 0.5rem;">
                <input class="form-input font-mono" v-model="onboardForm.password" placeholder="Leave blank to auto-generate" />
                <button type="button" class="btn btn-secondary btn-sm" @click="generateOnboardPassword">🎲 Generate</button>
              </div>
            </div>

            <div class="form-group mt-2">
              <label class="form-check-row" style="display: flex; align-items: center; gap: 0.5rem; cursor: pointer;">
                <input type="checkbox" v-model="onboardForm.is_verified" style="accent-color: #d4af37;" />
                <span style="font-size: 0.85rem; color: #e5e7eb;">Pre-verify CIPC Entity on BizPortal (Activate &amp; Unlock Workspace Immediately)</span>
              </label>
            </div>

            <div class="modal-footer mt-4" style="display: flex; justify-content: flex-end; gap: 0.75rem; border-top: 1px solid rgba(255,255,255,0.08); padding-top: 1rem;">
              <button type="button" class="btn btn-secondary" @click="closeOnboardModal" :disabled="onboardingSubmitting">Cancel</button>
              <button type="submit" class="btn btn-gold" :disabled="onboardingSubmitting">
                {{ onboardingSubmitting ? 'Provisioning...' : '🚀 Provision Corporate Workspace' }}
              </button>
            </div>
          </form>
        </div>
        <div v-if="onboardSuccessCredentials" class="modal-footer" style="display: flex; justify-content: flex-end; padding: 1rem 1.5rem; border-top: 1px solid rgba(255,255,255,0.08);">
          <button class="btn btn-primary" @click="closeOnboardModal">Done</button>
        </div>
      </div>
    </div>

    <!-- Executive Approval & Dispatch Modal -->
    <div v-if="showApprovalDispatchModal" class="modal-overlay">
      <div class="modal-panel luxury-modal" style="max-width: 650px;">
        <div class="modal-header">
          <div class="modal-title-wrap">
            <span class="modal-badge-tag" style="color: #10b981; font-size: 0.7rem; font-weight: 800; letter-spacing: 0.1em;">✓ WORKSPACE PROVISIONED</span>
            <h3 style="margin: 0; color: #fff; font-size: 1.35rem;">⚡ Executive Onboarding Dispatch</h3>
            <p class="text-muted text-sm mt-1 mb-0">The corporate workspace has been provisioned. Send or review credentials below.</p>
          </div>
          <button class="modal-close" @click="closeApprovalDispatchModal">×</button>
        </div>

        <div class="modal-body" style="padding: 1.5rem;" v-if="approvalDispatchData">
          <div class="alert-box success-box mb-4" style="background: rgba(16, 185, 129, 0.12); border: 1px solid rgba(16, 185, 129, 0.4); padding: 1.25rem; border-radius: 8px;">
            <div style="font-weight: 700; color: #86efac; font-size: 1.05rem; margin-bottom: 0.4rem;">
              ✓ Workspace Active for {{ approvalDispatchData.company_name }}
            </div>
            <div style="font-size: 0.85rem; color: #d1d5db;">
              Recipient: <strong>{{ approvalDispatchData.full_name }}</strong> ({{ approvalDispatchData.email }})
            </div>
          </div>

          <div style="background: rgba(0,0,0,0.5); border: 1px solid rgba(212,175,55,0.3); padding: 1.1rem; border-radius: 8px; font-family: monospace; font-size: 0.85rem; line-height: 1.7; color: #e5e7eb; margin-bottom: 1.25rem;">
            <div><strong style="color: #d4af37;">Portal URL:</strong> https://www.thefinishercrm.tech/#/login</div>
            <div><strong style="color: #d4af37;">Login Email:</strong> {{ approvalDispatchData.email }}</div>
            <div style="display: flex; align-items: center; justify-content: space-between; margin-top: 0.25rem;">
              <div>
                <strong style="color: #d4af37;">Auto-Generated Password:</strong> 
                <span style="color: #facc15; font-weight: 700; font-size: 1.05rem; background: rgba(250,204,21,0.15); padding: 0.15rem 0.5rem; border-radius: 4px; margin-left: 0.35rem;">
                  {{ approvalDispatchData.password }}
                </span>
              </div>
              <button type="button" class="btn btn-sm btn-secondary" @click="copyDispatchPassword" style="font-size: 0.72rem; padding: 0.2rem 0.5rem;">
                📋 Copy Pass
              </button>
            </div>
          </div>

          <div class="security-reset-badge" style="background: rgba(59, 130, 246, 0.12); border: 1px solid rgba(59, 130, 246, 0.3); border-radius: 6px; padding: 0.75rem 1rem; margin-bottom: 1.25rem; font-size: 0.82rem; color: #93c5fd; display: flex; align-items: center; gap: 0.5rem;">
            <span style="font-size: 1.1rem;">🔒</span>
            <div>
              <strong>Mandatory First Login Password Change Active:</strong>
              <div style="color: #bfdbfe; font-size: 0.78rem; margin-top: 0.1rem;">
                When the user enters this auto-generated temporary password, the system intercepts them immediately and forces them to choose a permanent personal password before accessing the system.
              </div>
            </div>
          </div>

          <!-- Executive Letter Preview Card -->
          <div class="letter-preview-card" style="background: rgba(10,10,10,0.85); border: 1px solid rgba(212,175,55,0.25); border-radius: 8px; padding: 1rem; margin-bottom: 1.25rem;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
              <span style="font-size: 0.75rem; font-weight: 800; letter-spacing: 1px; color: #d4af37; text-transform: uppercase;">
                📜 Executive Dispatch Letter Preview
              </span>
              <span style="font-size: 0.72rem; color: #9ca3af;">Auto-Preloaded into Outlook</span>
            </div>
            <pre style="white-space: pre-wrap; word-break: break-word; font-family: monospace; font-size: 0.76rem; color: #e5e7eb; background: rgba(0,0,0,0.5); padding: 0.75rem; border-radius: 6px; margin: 0; max-height: 180px; overflow-y: auto; border: 1px solid rgba(255,255,255,0.06); line-height: 1.5;">{{ approvalDispatchData.email_body }}</pre>
          </div>

          <div style="display: flex; gap: 0.75rem; flex-wrap: wrap;">
            <button 
              type="button" 
              class="btn btn-gold" 
              style="flex: 1; min-width: 200px; font-weight: 700; display: flex; align-items: center; justify-content: center; gap: 0.4rem; padding: 0.65rem 1rem;"
              @click="openOutlookWeb"
            >
              🌐 Open in Outlook Web (365)
            </button>
            <button 
              type="button" 
              class="btn btn-secondary" 
              style="font-weight: 600; display: flex; align-items: center; justify-content: center; gap: 0.4rem; padding: 0.65rem 1rem;"
              @click="openMailClient"
            >
              ✉️ Desktop Outlook
            </button>
            <button 
              type="button" 
              class="btn btn-secondary" 
              style="display: flex; align-items: center; gap: 0.4rem; padding: 0.65rem 1rem;"
              @click="copyDispatchLetter"
            >
              📋 Copy Letter
            </button>
          </div>
        </div>

        <div class="modal-footer" style="display: flex; justify-content: flex-end; padding: 1rem 1.5rem; border-top: 1px solid rgba(255,255,255,0.08);">
          <button class="btn btn-secondary" @click="closeApprovalDispatchModal">Done</button>
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
      filteredDeleteUsers: [],
      // POPIA Audit Trail
      auditLogs: [],
      loadingAudit: false,
      auditFilterEvent: '',
      auditFilterSeverity: '',
      auditFilterCompany: '',
      auditSearch: '',
      auditDebounceTimer: null,
      // CIPC Tenant Verifications
      verifications: [],
      loadingVerifications: false,
      // Corporate Access Requests (Executive Approvals)
      corporateAccessRequests: [],
      loadingAccessRequests: false,
      pendingAccessRequestsCount: 0,
      accessRequestActionLoading: null,
      showApprovalDispatchModal: false,
      approvalDispatchData: null,
      // Onboard Corporate Tenant Modal
      showOnboardModal: false,
      onboardingSubmitting: false,
      onboardError: '',
      onboardSuccessCredentials: null,
      onboardForm: {
        company_name: '',
        trading_name: '',
        cipc_number: '',
        tax_number: '',
        admin_name: '',
        admin_email: '',
        admin_phone: '',
        subscription_tier: 'trial',
        password: '',
        is_verified: false
      }
    }
  },
  computed: {
    apiBase() {
      const isLocal = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1';
      return isLocal ? 'http://localhost:8000/api' : 'https://the-finisher-luxury-api.onrender.com/api';
    },
    token() {
      return localStorage.getItem('thefinisher_access_token');
    },
    companiesList() {
      const list = new Set();
      if (this.overview && this.overview.clients) {
        this.overview.clients.forEach(cl => {
          if (cl.companies) cl.companies.forEach(co => { if (co.name) list.add(co.name); });
        });
      }
      if (this.auditLogs) {
        this.auditLogs.forEach(l => { if (l.organization_name) list.add(l.organization_name); });
      }
      return Array.from(list).filter(Boolean).sort();
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
        await this.fetchAuditLogs();
        await this.fetchVerifications();
        await this.fetchAccessRequests();
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
    // CIPC Business Verification Methods
    async fetchVerifications() {
      this.loadingVerifications = true;
      try {
        const res = await this.fetchApi('/admin/tenant-verifications/');
        this.verifications = Array.isArray(res) ? res : [];
      } catch (e) {
        console.warn('Failed to load verifications:', e);
      } finally {
        this.loadingVerifications = false;
      }
    },
    async reviewVerification(id, action) {
      let reason = '';
      if (action === 'reject') {
        reason = prompt('Enter rejection reason / instructions for client:', 'Documentation could not be verified against the official CIPC register.');
        if (reason === null) return;
      }
      const notes = prompt('Internal compliance check notes (optional):', action === 'approve' ? 'Verified on CIPC BizPortal' : 'Failed CIPC validation');
      if (notes === null && action === 'approve') return;

      try {
        await this.fetchApi(`/admin/tenant-verifications/${id}/review/`, {
          method: 'POST',
          body: JSON.stringify({
            action,
            internal_notes: notes || '',
            rejection_reason: reason || ''
          })
        });
        alert(action === 'approve' ? '✓ Tenant verified and workspace unlocked successfully!' : '✕ Tenant verification rejected.');
        await this.fetchVerifications();
        await this.fetchAuditLogs();
      } catch (e) {
        alert('Failed to process verification: ' + e.message);
      }
    },
    // Corporate Access Request Methods
    async fetchAccessRequests() {
      this.loadingAccessRequests = true;
      try {
        const res = await this.fetchApi('/admin/access-requests/');
        this.corporateAccessRequests = res.requests || [];
        this.pendingAccessRequestsCount = res.pending_count || 0;
      } catch (e) {
        console.warn('Failed to load corporate access requests:', e);
      } finally {
        this.loadingAccessRequests = false;
      }
    },
    async processAccessRequest(id, action, companyName, email) {
      if (action === 'approve') {
        if (!confirm(`Authorize & provision dedicated corporate workspace for ${companyName} (${email})?\n\nThis will automatically:\n1. Provision Organization tenant\n2. Create Admin User account\n3. Activate 7-Day VIP Executive privileges\n4. Dispatch live credentials to ${email}`)) {
          return;
        }
      } else if (action === 'reject') {
        const reason = prompt(`Enter rejection feedback for ${companyName}:`, 'Application criteria not met');
        if (reason === null) return;
        return this.executeAccessRequestAction(id, action, '', reason);
      }
      await this.executeAccessRequestAction(id, action);
    },
    async executeAccessRequestAction(id, action, notes = '', rejectionReason = '') {
      this.accessRequestActionLoading = id;
      try {
        const res = await this.fetchApi(`/admin/access-requests/${id}/action/`, {
          method: 'POST',
          body: JSON.stringify({ action, notes, rejection_reason: rejectionReason })
        });
        if (action === 'approve') {
          this.approvalDispatchData = {
            company_name: res.organization?.name || 'Enterprise Workspace',
            email: res.user?.email || '',
            full_name: res.user?.full_name || '',
            password: res.auto_generated_password || '',
            email_subject: res.email_subject || '',
            email_body: res.email_body || '',
            mailto_link: res.mailto_link || `mailto:${res.user?.email || ''}`
          };
          this.showApprovalDispatchModal = true;
        } else {
          alert(res.message || `Request ${action}ed successfully.`);
        }
        await this.fetchAccessRequests();
        await this.loadAllData();
      } catch (err) {
        alert('Operation failed: ' + err.message);
      } finally {
        this.accessRequestActionLoading = null;
      }
    },
    // POPIA Audit Trail Methods
    async fetchAuditLogs() {
      this.loadingAudit = true;
      try {
        let endpoint = '/audit-trail/?';
        if (this.auditFilterEvent) endpoint += `event_type=${encodeURIComponent(this.auditFilterEvent)}&`;
        if (this.auditFilterSeverity) endpoint += `severity=${encodeURIComponent(this.auditFilterSeverity)}&`;
        if (this.auditFilterCompany) endpoint += `company_name=${encodeURIComponent(this.auditFilterCompany)}&`;
        if (this.auditSearch) endpoint += `search=${encodeURIComponent(this.auditSearch)}&`;
        const res = await this.fetchApi(endpoint);
        this.auditLogs = Array.isArray(res) ? res : (res.results || []);
      } catch (e) {
        console.warn('Failed to load audit logs:', e);
      } finally {
        this.loadingAudit = false;
      }
    },
    debounceAuditSearch() {
      clearTimeout(this.auditDebounceTimer);
      this.auditDebounceTimer = setTimeout(() => {
        this.fetchAuditLogs();
      }, 350);
    },
    formatAuditTimestamp(ts) {
      if (!ts) return '—';
      try {
        const d = new Date(ts);
        return d.toISOString().replace('T', ' ').substring(0, 19);
      } catch (_) {
        return ts;
      }
    },
    exportPopiaCert() {
      const url = `${this.apiBase}/audit-trail/export-compliance-log/`;
      const token = this.token;
      fetch(url, {
        headers: { 'Authorization': `Bearer ${token}` }
      })
      .then(res => {
        if (!res.ok) throw new Error('Export failed');
        return res.blob();
      })
      .then(blob => {
        const downloadUrl = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = downloadUrl;
        a.download = `POPIA_Audit_Trail_${new Date().toISOString().substring(0,10)}.csv`;
        document.body.appendChild(a);
        a.click();
        a.remove();
        window.URL.revokeObjectURL(downloadUrl);
        setTimeout(() => this.fetchAuditLogs(), 500);
      })
      .catch(err => {
        alert('Could not export POPIA Audit log: ' + err.message);
      });
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

    // Corporate Tenant Onboarding
    openOnboardModal() {
      this.onboardForm = {
        company_name: '',
        trading_name: '',
        cipc_number: '',
        tax_number: '',
        admin_name: '',
        admin_email: '',
        admin_phone: '',
        subscription_tier: 'trial',
        password: '',
        is_verified: false
      };
      this.generateOnboardPassword();
      this.onboardError = '';
      this.onboardSuccessCredentials = null;
      this.showOnboardModal = true;
    },
    closeOnboardModal() {
      this.showOnboardModal = false;
      this.onboardError = '';
      this.onboardSuccessCredentials = null;
    },
    generateOnboardPassword() {
      const chars = 'ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnpqrstuvwxyz23456789!@#$';
      let pwd = '';
      for (let i = 0; i < 12; i++) {
        pwd += chars.charAt(Math.floor(Math.random() * chars.length));
      }
      this.onboardForm.password = pwd;
    },
    async submitOnboardCompany() {
      this.onboardError = '';
      this.onboardingSubmitting = true;
      try {
        const res = await this.fetchApi('/admin/clients-employees/', {
          method: 'POST',
          body: JSON.stringify({
            action: 'onboard_company',
            ...this.onboardForm
          })
        });
        this.onboardSuccessCredentials = res.credentials;
        await this.loadAllData();
      } catch (err) {
        this.onboardError = err.message || 'Failed to onboard company.';
      } finally {
        this.onboardingSubmitting = false;
      }
    },
    copyCredentials() {
      if (!this.onboardSuccessCredentials) return;
      const text = `The Finisher CRM Corporate Workspace Credentials\nCompany: ${this.onboardSuccessCredentials.company_name}\nLogin URL: https://www.thefinishercrm.tech\nEmail: ${this.onboardSuccessCredentials.email}\nPassword: ${this.onboardSuccessCredentials.password}\nTier: ${this.onboardSuccessCredentials.subscription_tier}`;
      navigator.clipboard.writeText(text).then(() => {
        alert('Corporate credentials copied to clipboard!');
      });
    },

    openMailClient() {
      if (this.approvalDispatchData?.mailto_link) {
        window.location.href = this.approvalDispatchData.mailto_link;
      }
    },
    copyDispatchLetter() {
      if (!this.approvalDispatchData?.email_body) return;
      navigator.clipboard.writeText(this.approvalDispatchData.email_body).then(() => {
        alert('Executive welcome dispatch copied to clipboard!');
      });
    },
    copyDispatchPassword() {
      if (!this.approvalDispatchData?.password) return;
      navigator.clipboard.writeText(this.approvalDispatchData.password).then(() => {
        alert('Auto-generated temporary password copied to clipboard!');
      });
    },
    closeApprovalDispatchModal() {
      this.showApprovalDispatchModal = false;
      this.approvalDispatchData = null;
    },

    closeQuickDelete() {
      this.showQuickDelete = false;
      this.quickDeleteUser = null;
      this.quickDeleteSearch = '';
      this.filteredDeleteUsers = [];
      this.quickDeleteReason = '';
      this.quickDeleteCustomReason = '';
    },
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
    },
    openOutlookWeb() {
      if (!this.approvalDispatchData) return;
      const to = encodeURIComponent(this.approvalDispatchData.email || '');
      const subject = encodeURIComponent(this.approvalDispatchData.email_subject || 'Corporate Access Provisioned - THE FINISHER LUXURY');
      const body = encodeURIComponent(this.approvalDispatchData.email_body || '');
      const outlookWebUrl = `https://outlook.office.com/mail/deeplink/compose?to=${to}&subject=${subject}&body=${body}`;
      window.open(outlookWebUrl, '_blank');
      this.copyDispatchLetter(true);
    },
    openMailClient() {
      if (!this.approvalDispatchData) return;
      if (this.approvalDispatchData.mailto_link) {
        window.location.href = this.approvalDispatchData.mailto_link;
      }
      this.copyDispatchLetter(true);
    },
    closeApprovalDispatchModal() {
      this.showApprovalDispatchModal = false;
      this.approvalDispatchData = null;
    },
    copyDispatchPassword() {
      if (!this.approvalDispatchData?.password) return;
      navigator.clipboard.writeText(this.approvalDispatchData.password);
      this.dispatchEvent('show-toast', { message: 'Password copied to clipboard', type: 'success' });
    },
    copyDispatchLetter(silent = false) {
      if (!this.approvalDispatchData?.email_body) return;
      navigator.clipboard.writeText(this.approvalDispatchData.email_body);
      if (!silent) {
        this.dispatchEvent('show-toast', { message: 'Full letter copied to clipboard', type: 'success' });
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

/* POPIA Audit Trail Deck */
.badge-popia {
  display: inline-block;
  font-size: 0.65rem;
  font-weight: 800;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  background: rgba(212, 175, 55, 0.15);
  color: #D4AF37;
  border: 1px solid rgba(212, 175, 55, 0.3);
  padding: 2px 8px;
  border-radius: 4px;
  margin-bottom: 0.5rem;
}
.section-header-flex {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  flex-wrap: wrap;
  gap: 1rem;
  margin-bottom: 1.25rem;
}
.audit-actions {
  display: flex;
  gap: 0.5rem;
  align-items: center;
}
.btn-gold {
  background: linear-gradient(135deg, #D4AF37 0%, #AA771C 100%);
  color: #000;
  font-weight: 700;
  border: none;
  display: inline-flex;
  align-items: center;
  gap: 0.35rem;
  cursor: pointer;
  border-radius: 6px;
  padding: 0.5rem 1rem;
  transition: all 0.2s ease;
}
.btn-gold:hover {
  filter: brightness(1.15);
  box-shadow: 0 0 12px rgba(212, 175, 55, 0.4);
}
.audit-filter-bar {
  display: flex;
  gap: 1rem;
  background: rgba(255, 255, 255, 0.02);
  border: 1px solid rgba(255, 255, 255, 0.08);
  padding: 0.75rem 1rem;
  border-radius: 8px;
  margin-bottom: 1rem;
  flex-wrap: wrap;
  align-items: center;
}
.filter-group {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.8125rem;
  color: #9ca3af;
}
.filter-group.flex-1 { flex: 1; min-width: 220px; }
.form-input-sm {
  padding: 0.35rem 0.65rem;
  font-size: 0.8125rem;
  height: auto;
  border-radius: 4px;
}
.badge-audit {
  display: inline-block;
  padding: 2px 8px;
  border-radius: 4px;
  font-size: 0.6875rem;
  font-weight: 700;
  letter-spacing: 0.04em;
  text-transform: uppercase;
}
.badge-info {
  background: rgba(59, 130, 246, 0.15);
  color: #60a5fa;
  border: 1px solid rgba(59, 130, 246, 0.3);
}
.badge-warning {
  background: rgba(245, 158, 11, 0.15);
  color: #fbbf24;
  border: 1px solid rgba(245, 158, 11, 0.3);
}
.badge-critical {
  background: rgba(239, 68, 68, 0.2);
  color: #f87171;
  border: 1px solid rgba(239, 68, 68, 0.4);
}
.event-badge {
  font-size: 0.75rem;
  color: #e5e7eb;
  font-weight: 600;
}
.ip-pill {
  background: rgba(255, 255, 255, 0.05);
  padding: 2px 6px;
  border-radius: 4px;
  font-size: 0.75rem;
  color: #d1d5db;
  border: 1px solid rgba(255, 255, 255, 0.1);
}
.audit-desc {
  color: #d1d5db;
  max-width: 420px;
  line-height: 1.4;
}
.audit-loading, .audit-empty {
  padding: 2.5rem;
  text-align: center;
  color: #9ca3af;
  font-size: 0.875rem;
}
.doc-links {
  display: flex;
  gap: 0.35rem;
  flex-wrap: wrap;
}
.doc-link-btn {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  background: rgba(255, 255, 255, 0.06);
  border: 1px solid rgba(255, 255, 255, 0.12);
  color: #60a5fa;
  padding: 2px 7px;
  border-radius: 4px;
  font-size: 0.75rem;
  text-decoration: none;
  transition: all 0.2s;
}
.doc-link-btn:hover {
  background: rgba(59, 130, 246, 0.2);
  border-color: #60a5fa;
  color: #ffffff;
}
</style>
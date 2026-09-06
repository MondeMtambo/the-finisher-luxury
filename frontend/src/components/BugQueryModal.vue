<template>
  <div v-if="isOpen" class="query-modal-overlay" @click.self="closeModal">
    <div class="query-modal-card">
      <!-- Luxury Gold Top Accent Line -->
      <div class="modal-gold-bar"></div>

      <div class="modal-header">
        <div class="header-badge">
          <span class="badge-icon">🛡️</span>
          <span class="badge-text">EXECUTIVE DESK DIRECT DISPATCH</span>
        </div>
        <button class="close-btn" @click="closeModal" aria-label="Close modal">&times;</button>
      </div>

      <div class="modal-title-wrap">
        <h2>Submit a Query / Report an Issue</h2>
        <p>Direct communication pipeline to Mtambo Holdings Executive Desk &amp; Engineering Team (<code>mtamboholdings@outlook.com</code>).</p>
      </div>

      <form @submit.prevent="handleSubmit" class="query-form">
        <div class="form-row-2">
          <div class="form-group">
            <label>Your Name *</label>
            <input 
              v-model="form.name" 
              type="text" 
              required 
              placeholder="e.g. Monde Mtambo" 
              class="luxury-input"
            />
          </div>
          <div class="form-group">
            <label>Your Email *</label>
            <input 
              v-model="form.email" 
              type="email" 
              required 
              placeholder="e.g. client@company.co.za" 
              class="luxury-input"
            />
          </div>
        </div>

        <div class="form-row-2">
          <div class="form-group">
            <label>Query Type</label>
            <select v-model="form.query_type" class="luxury-input">
              <option value="Bug Report">🐛 System Bug / Glitch</option>
              <option value="Feature Request">💡 Feature / Enhancement Request</option>
              <option value="Billing / License">💳 Commercial, Billing &amp; Licensing</option>
              <option value="Security / POPIA">🔒 Security / POPIA Compliance</option>
              <option value="General Support">💬 General Support Inquiry</option>
            </select>
          </div>
          <div class="form-group">
            <label>Urgency Level</label>
            <select v-model="form.urgency" class="luxury-input">
              <option value="Low">Low — Informational</option>
              <option value="Normal">Normal — Standard SLA</option>
              <option value="High">High — Critical Impact</option>
              <option value="Urgent Executive">🚨 Urgent Executive Attention</option>
            </select>
          </div>
        </div>

        <div class="form-group">
          <label>Subject *</label>
          <input 
            v-model="form.subject" 
            type="text" 
            required 
            placeholder="Brief summary of your query or issue" 
            class="luxury-input"
          />
        </div>

        <div class="form-group">
          <label>Description &amp; Context *</label>
          <textarea 
            v-model="form.description" 
            required 
            rows="4" 
            placeholder="Please detail your query, steps to reproduce the issue, or requested assistance..." 
            class="luxury-input"
          ></textarea>
        </div>

        <div class="compliance-hint">
          <span class="lock-icon">🔒</span>
          <span>Dispatched with 256-bit TLS encryption. Copy sent to Executive Audit Desk. Registered Office: <strong>7682 Isikova Crescent, Gauteng, Boksburg, 1459</strong>.</span>
        </div>

        <div class="modal-actions">
          <button type="button" class="btn-cancel" @click="closeModal" :disabled="submitting">Cancel</button>
          <button type="submit" class="btn-submit" :disabled="submitting">
            <span v-if="submitting" class="spinner-small"></span>
            <span v-else>💎 Dispatch to Executive Desk</span>
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
import { bugQueryAPI } from '../api'
import authService from '../services/auth'
import toast from '../utils/toast'

export default {
  name: 'BugQueryModal',
  props: {
    modelValue: {
      type: Boolean,
      default: false
    }
  },
  emits: ['update:modelValue'],
  data() {
    return {
      submitting: false,
      form: {
        name: '',
        email: '',
        query_type: 'Bug Report',
        urgency: 'Normal',
        subject: '',
        description: ''
      }
    }
  },
  computed: {
    isOpen() {
      return this.modelValue
    }
  },
  watch: {
    modelValue(val) {
      if (val) {
        this.prefillUser()
      }
    }
  },
  methods: {
    prefillUser() {
      const user = authService.getUser()
      if (user) {
        this.form.name = user.full_name || `${user.first_name || ''} ${user.last_name || ''}`.trim() || user.username || ''
        this.form.email = user.email || ''
      }
    },
    closeModal() {
      this.$emit('update:modelValue', false)
    },
    async handleSubmit() {
      this.submitting = true
      try {
        await bugQueryAPI.submit({
          name: this.form.name,
          email: this.form.email,
          query_type: this.form.query_type,
          urgency: this.form.urgency,
          subject: this.form.subject,
          description: this.form.description
        })

        toast.success(
          'Query Dispatched',
          'Your communication has been forwarded directly to Executive Support (mtamboholdings@outlook.com).'
        )

        this.form.subject = ''
        this.form.description = ''
        this.closeModal()
      } catch (error) {
        console.error('Failed to dispatch query:', error)
        toast.error(
          'Dispatch Failed',
          error.response?.data?.error || 'Unable to submit your query. Please try again or email mtamboholdings@outlook.com directly.'
        )
      } finally {
        this.submitting = false
      }
    }
  }
}
</script>

<style scoped>
.query-modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(10, 15, 29, 0.82);
  backdrop-filter: blur(8px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 99999;
  padding: 1.5rem;
  animation: fadeIn 0.2s ease-out;
}

.query-modal-card {
  position: relative;
  width: 100%;
  max-width: 580px;
  background: linear-gradient(180deg, #111827 0%, #0b0f19 100%);
  border: 1px solid rgba(212, 175, 55, 0.35);
  border-radius: 16px;
  box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.7), 0 0 30px rgba(212, 175, 55, 0.15);
  overflow: hidden;
  color: #f3f4f6;
  padding: 1.75rem 2rem;
  animation: scaleUp 0.25s cubic-bezier(0.16, 1, 0.3, 1);
}

.modal-gold-bar {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 4px;
  background: linear-gradient(90deg, #d4af37, #f59e0b, #d4af37);
}

.modal-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 0.75rem;
}

.header-badge {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  background: rgba(212, 175, 55, 0.12);
  border: 1px solid rgba(212, 175, 55, 0.3);
  padding: 4px 10px;
  border-radius: 9999px;
  font-size: 0.7rem;
  font-weight: 800;
  letter-spacing: 0.06em;
  color: #fbbf24;
}

.close-btn {
  background: none;
  border: none;
  color: #9ca3af;
  font-size: 1.6rem;
  cursor: pointer;
  line-height: 1;
  transition: color 0.15s;
}
.close-btn:hover {
  color: #fff;
}

.modal-title-wrap h2 {
  font-size: 1.35rem;
  font-weight: 700;
  color: #ffffff;
  margin: 0 0 0.35rem;
}

.modal-title-wrap p {
  font-size: 0.825rem;
  color: #94a3b8;
  margin: 0 0 1.25rem;
  line-height: 1.45;
}

.modal-title-wrap code {
  color: #d4af37;
  font-weight: 600;
}

.query-form {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.form-row-2 {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 0.85rem;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.35rem;
}

.form-group label {
  font-size: 0.78rem;
  font-weight: 600;
  color: #cbd5e1;
  text-transform: uppercase;
  letter-spacing: 0.04em;
}

.luxury-input {
  background: rgba(17, 24, 39, 0.8);
  border: 1px solid rgba(255, 255, 255, 0.12);
  border-radius: 8px;
  padding: 0.65rem 0.85rem;
  font-size: 0.875rem;
  color: #f8fafc;
  outline: none;
  transition: all 0.2s;
}

.luxury-input:focus {
  border-color: #d4af37;
  box-shadow: 0 0 0 3px rgba(212, 175, 55, 0.2);
}

textarea.luxury-input {
  resize: vertical;
}

.compliance-hint {
  display: flex;
  align-items: flex-start;
  gap: 0.5rem;
  background: rgba(212, 175, 55, 0.06);
  border: 1px solid rgba(212, 175, 55, 0.18);
  border-radius: 8px;
  padding: 0.6rem 0.85rem;
  font-size: 0.74rem;
  color: #cbd5e1;
  line-height: 1.4;
}

.compliance-hint strong {
  color: #facc15;
}

.modal-actions {
  display: flex;
  align-items: center;
  justify-content: flex-end;
  gap: 0.75rem;
  margin-top: 0.5rem;
}

.btn-cancel {
  background: transparent;
  border: 1px solid rgba(255, 255, 255, 0.15);
  color: #cbd5e1;
  padding: 0.65rem 1.25rem;
  border-radius: 8px;
  font-size: 0.85rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.15s;
}
.btn-cancel:hover:not(:disabled) {
  background: rgba(255, 255, 255, 0.05);
  color: #fff;
}

.btn-submit {
  background: linear-gradient(135deg, #d4af37 0%, #b45309 100%);
  border: none;
  color: #0b0f19;
  padding: 0.65rem 1.4rem;
  border-radius: 8px;
  font-size: 0.85rem;
  font-weight: 800;
  letter-spacing: 0.03em;
  cursor: pointer;
  box-shadow: 0 4px 15px rgba(212, 175, 55, 0.35);
  transition: all 0.2s;
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
}

.btn-submit:hover:not(:disabled) {
  transform: translateY(-1px);
  box-shadow: 0 6px 20px rgba(212, 175, 55, 0.5);
}

.btn-submit:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.spinner-small {
  width: 16px;
  height: 16px;
  border: 2px solid rgba(0, 0, 0, 0.3);
  border-top-color: #000;
  border-radius: 50%;
  animation: spin 0.6s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

@keyframes scaleUp {
  from { opacity: 0; transform: scale(0.95); }
  to { opacity: 1; transform: scale(1); }
}

@media (max-width: 600px) {
  .form-row-2 {
    grid-template-columns: 1fr;
  }
}
</style>

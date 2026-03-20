<template>
  <div class="doc-page">
    <div class="doc-container">
      <button class="back-btn" @click="$router.push('/')">← Back to Home</button>
      
      <h1>API Documentation</h1>
      <p class="subtitle">RESTful API for THE FINISHER LUXURY CRM</p>

      <div class="api-notice">
        <strong>🔒 API Access:</strong> Available on LUXURY and PREMIUM tiers only
      </div>

      <section>
        <h2>Getting Started</h2>
        <p>The FINISHER LUXURY API allows you to integrate CRM functionality into your applications. All requests require authentication via JWT tokens.</p>
        
        <h3>Base URL</h3>
        <div class="code-block">
          https://api.thefinisher.co.za/api/
        </div>

        <h3>Authentication</h3>
        <p>Include your JWT token in the Authorization header:</p>
        <div class="code-block">
          Authorization: Bearer YOUR_JWT_TOKEN
        </div>
      </section>

      <section>
        <h2>Endpoints</h2>

        <div class="endpoint">
          <div class="endpoint-header">
            <span class="method get">GET</span>
            <span class="path">/contacts/</span>
          </div>
          <p class="endpoint-desc">Retrieve all contacts for your company</p>
          <div class="code-block">
curl -X GET "https://api.thefinisher.co.za/api/contacts/" \
  -H "Authorization: Bearer YOUR_TOKEN"
          </div>
        </div>

        <div class="endpoint">
          <div class="endpoint-header">
            <span class="method post">POST</span>
            <span class="path">/contacts/</span>
          </div>
          <p class="endpoint-desc">Create a new contact</p>
          <div class="code-block">
curl -X POST "https://api.thefinisher.co.za/api/contacts/" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "John",
    "last_name": "Doe",
    "email": "john@example.com",
    "phone": "+27123456789"
  }'
          </div>
        </div>

        <div class="endpoint">
          <div class="endpoint-header">
            <span class="method get">GET</span>
            <span class="path">/companies/</span>
          </div>
          <p class="endpoint-desc">List all companies</p>
        </div>

        <div class="endpoint">
          <div class="endpoint-header">
            <span class="method get">GET</span>
            <span class="path">/deals/</span>
          </div>
          <p class="endpoint-desc">Retrieve deals with filtering options</p>
          <p class="params"><strong>Query Parameters:</strong></p>
          <ul>
            <li><code>stage</code> - Filter by deal stage (lead, qualified, proposal, negotiation, won, lost)</li>
            <li><code>contact</code> - Filter by contact ID</li>
            <li><code>company</code> - Filter by company ID</li>
          </ul>
        </div>

        <div class="endpoint">
          <div class="endpoint-header">
            <span class="method post">POST</span>
            <span class="path">/deals/</span>
          </div>
          <p class="endpoint-desc">Create a new deal</p>
          <div class="code-block">
{
  "title": "Q4 Enterprise Deal",
  "value": 50000,
  "stage": "qualified",
  "contact": 123,
  "company": 45,
  "expected_close_date": "2025-12-31"
}
          </div>
        </div>

        <div class="endpoint">
          <div class="endpoint-header">
            <span class="method get">GET</span>
            <span class="path">/tickets/</span>
          </div>
          <p class="endpoint-desc">List support tickets</p>
        </div>

        <div class="endpoint">
          <div class="endpoint-header">
            <span class="method post">POST</span>
            <span class="path">/tickets/</span>
          </div>
          <p class="endpoint-desc">Create a new ticket</p>
          <div class="code-block">
{
  "title": "Login Issue",
  "description": "User cannot access account",
  "priority": "high",
  "category": "technical",
  "assigned_to": 5
}
          </div>
        </div>
      </section>

      <section>
        <h2>Response Codes</h2>
        <table class="response-table">
          <thead>
            <tr>
              <th>Code</th>
              <th>Meaning</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td><span class="code-badge success">200</span></td>
              <td>Success</td>
            </tr>
            <tr>
              <td><span class="code-badge success">201</span></td>
              <td>Created</td>
            </tr>
            <tr>
              <td><span class="code-badge error">400</span></td>
              <td>Bad Request</td>
            </tr>
            <tr>
              <td><span class="code-badge error">401</span></td>
              <td>Unauthorized</td>
            </tr>
            <tr>
              <td><span class="code-badge error">403</span></td>
              <td>Forbidden</td>
            </tr>
            <tr>
              <td><span class="code-badge error">404</span></td>
              <td>Not Found</td>
            </tr>
            <tr>
              <td><span class="code-badge error">500</span></td>
              <td>Server Error</td>
            </tr>
          </tbody>
        </table>
      </section>

      <section>
        <h2>Rate Limits</h2>
        <ul>
          <li><strong>LUXURY:</strong> 1,000 requests/hour</li>
          <li><strong>PREMIUM:</strong> 10,000 requests/hour</li>
        </ul>
        <p>Rate limit headers are included in every response:</p>
        <div class="code-block">
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 998
X-RateLimit-Reset: 1699876543
        </div>
      </section>

      <section>
        <h2>Webhooks (Coming Soon)</h2>
        <p>Register webhooks to receive real-time updates for:</p>
        <ul>
          <li>New contacts created</li>
          <li>Deal stage changes</li>
          <li>Ticket assignments</li>
          <li>Status updates</li>
        </ul>
      </section>

      <section>
        <h2>Need Help?</h2>
        <p>Contact our developer support team:</p>
        <p><strong>Email:</strong> api@thefinisher.co.za</p>
        <p><strong>Documentation:</strong> <a href="https://docs.thefinisher.co.za" target="_blank">docs.thefinisher.co.za</a></p>
      </section>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ApiDocs'
}
</script>

<style scoped>
.doc-page {
  min-height: 100vh;
  background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
  color: #e2e8f0;
  padding: 2rem;
}

.doc-container {
  max-width: 1000px;
  margin: 0 auto;
  background: rgba(255, 255, 255, 0.05);
  padding: 3rem;
  border-radius: 16px;
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.back-btn {
  background: rgba(56, 189, 248, 0.2);
  border: 1px solid rgba(56, 189, 248, 0.4);
  color: #38bdf8;
  padding: 0.5rem 1rem;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 600;
  margin-bottom: 2rem;
  transition: all 0.2s ease;
}

.back-btn:hover {
  background: rgba(56, 189, 248, 0.3);
  transform: translateX(-4px);
}

h1 {
  font-size: 2.5rem;
  color: #f8fafc;
  margin-bottom: 0.5rem;
  font-weight: 800;
}

.subtitle {
  color: #94a3b8;
  font-size: 1.1rem;
  margin-bottom: 2rem;
}

.api-notice {
  background: rgba(251, 191, 36, 0.15);
  border: 1px solid rgba(251, 191, 36, 0.4);
  border-radius: 8px;
  padding: 1rem;
  margin: 2rem 0;
  color: #fbbf24;
}

section {
  margin: 3rem 0;
}

h2 {
  font-size: 1.8rem;
  color: #38bdf8;
  margin: 2rem 0 1rem 0;
  font-weight: 700;
  border-bottom: 2px solid rgba(56, 189, 248, 0.3);
  padding-bottom: 0.5rem;
}

h3 {
  font-size: 1.3rem;
  color: #93c5fd;
  margin: 1.5rem 0 0.75rem 0;
  font-weight: 600;
}

p {
  line-height: 1.8;
  margin: 1rem 0;
  color: #cbd5e1;
}

.code-block {
  background: #0a0f1a;
  border: 1px solid rgba(56, 189, 248, 0.3);
  border-radius: 8px;
  padding: 1rem;
  margin: 1rem 0;
  font-family: 'Courier New', monospace;
  font-size: 0.9rem;
  color: #93c5fd;
  overflow-x: auto;
  white-space: pre-wrap;
}

.endpoint {
  background: rgba(15, 23, 42, 0.6);
  border: 1px solid rgba(148, 163, 184, 0.2);
  border-radius: 12px;
  padding: 1.5rem;
  margin: 1.5rem 0;
}

.endpoint-header {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 0.75rem;
}

.method {
  padding: 0.25rem 0.75rem;
  border-radius: 6px;
  font-weight: 700;
  font-size: 0.85rem;
  text-transform: uppercase;
}

.method.get {
  background: rgba(34, 197, 94, 0.2);
  color: #22c55e;
  border: 1px solid rgba(34, 197, 94, 0.4);
}

.method.post {
  background: rgba(59, 130, 246, 0.2);
  color: #3b82f6;
  border: 1px solid rgba(59, 130, 246, 0.4);
}

.path {
  font-family: 'Courier New', monospace;
  font-size: 1.1rem;
  color: #f8fafc;
  font-weight: 600;
}

.endpoint-desc {
  color: #cbd5e1;
  margin: 0.5rem 0;
}

.params {
  margin-top: 1rem;
  color: #94a3b8;
  font-size: 0.9rem;
}

ul {
  margin: 0.5rem 0;
  padding-left: 2rem;
}

li {
  margin: 0.5rem 0;
  line-height: 1.6;
  color: #cbd5e1;
}

code {
  background: rgba(56, 189, 248, 0.15);
  padding: 0.2rem 0.4rem;
  border-radius: 4px;
  font-family: 'Courier New', monospace;
  color: #38bdf8;
  font-size: 0.9em;
}

.response-table {
  width: 100%;
  border-collapse: collapse;
  margin: 1.5rem 0;
}

.response-table th {
  background: rgba(56, 189, 248, 0.1);
  padding: 0.75rem;
  text-align: left;
  font-weight: 700;
  color: #38bdf8;
  border: 1px solid rgba(56, 189, 248, 0.3);
}

.response-table td {
  padding: 0.75rem;
  border: 1px solid rgba(148, 163, 184, 0.2);
  color: #cbd5e1;
}

.code-badge {
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  font-weight: 700;
  font-family: 'Courier New', monospace;
  font-size: 0.85rem;
}

.code-badge.success {
  background: rgba(34, 197, 94, 0.2);
  color: #22c55e;
}

.code-badge.error {
  background: rgba(239, 68, 68, 0.2);
  color: #ef4444;
}

a {
  color: #38bdf8;
  text-decoration: none;
  font-weight: 600;
}

a:hover {
  text-decoration: underline;
}

@media (max-width: 768px) {
  .doc-container {
    padding: 1.5rem;
  }

  h1 {
    font-size: 2rem;
  }

  h2 {
    font-size: 1.5rem;
  }

  .endpoint-header {
    flex-direction: column;
    align-items: flex-start;
  }
}
</style>

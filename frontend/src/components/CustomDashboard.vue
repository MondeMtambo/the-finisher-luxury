<template>
  <div class="page-wrap">
    <div class="page-header">
      <div>
        <h1>Custom Dashboard</h1>
        <p class="page-subtitle">Your personalised analytics overview</p>
        <div v-if="canDragDrop" class="luxury-badge">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/></svg>
          <span>LUXURY EXCLUSIVE: Drag headers to reorder widgets</span>
        </div>
      </div>
      <div class="header-actions">
        <button class="btn btn-secondary" @click="resetDefaults" :disabled="resetting">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 12a9 9 0 1 0 9-9 9.75 9.75 0 0 0-6.74 2.74L3 8"/><path d="M3 3v5h5"/></svg>
          Reset Defaults
        </button>
        <button class="btn btn-primary" @click="showAddWidget = true">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/></svg>
          Add Widget
        </button>
      </div>
    </div>

    <div v-if="!loading && activeWidgets.length > 0" class="grid-stack" ref="gridContainer">
      <div 
        v-for="widget in activeWidgets" 
        :key="widget.id"
        class="grid-stack-item"
        :gs-id="widget.id"
        :gs-x="widget.position_x || 0"
        :gs-y="widget.position_y || 0"
        :gs-w="widget.width || 1"
        :gs-h="widget.height || 1"
      >
        <div class="grid-stack-item-content widget-card">
        <div class="widget-header" :class="{ 'draggable-header': canDragDrop }">
          <h3>{{ widget.title }}</h3>
          <div class="widget-controls">
            <button class="btn-icon" @click="toggleVisibility(widget)" title="Hide widget">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94"/><line x1="1" y1="1" x2="23" y2="23"/></svg>
            </button>
            <button class="btn-icon" @click="removeWidget(widget)" title="Remove widget">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>
            </button>
          </div>
        </div>

        <div class="widget-body">

          <div v-if="widget.widget_type === 'stat_card'" class="widget-stat">
            <div class="stat-big">{{ widgetData[widget.widget_type]?.value ?? '—' }}</div>
            <div class="stat-sub">{{ widgetData[widget.widget_type]?.label ?? '' }}</div>
          </div>

          <div v-else-if="widget.widget_type === 'pipeline_chart'" class="widget-pipeline">
            <div v-for="stage in (widgetData.pipeline_chart || [])" :key="stage.stage" class="pipe-bar-row">
              <span class="pipe-label">{{ stage.stage }}</span>
              <div class="pipe-bar-track">
                <div class="pipe-bar-fill" :style="{ width: pipeWidth(stage.count) }"></div>
              </div>
              <span class="pipe-val">{{ stage.count }}</span>
            </div>
            <div v-if="!(widgetData.pipeline_chart || []).length" class="widget-empty">No pipeline data</div>
          </div>

          <div v-else-if="widget.widget_type === 'revenue_chart'" class="widget-revenue">
            <div class="rev-total">R{{ formatNumber(widgetData.revenue_chart?.total ?? 0) }}</div>
            <div class="rev-label">Total Revenue</div>
            <div class="rev-bars">
              <div v-for="(m, idx) in (widgetData.revenue_chart?.months || [])" :key="idx" class="rev-bar-col">
                <div class="rev-bar" :style="{ height: revHeight(m.value) }"></div>
                <span class="rev-month">{{ m.label }}</span>
              </div>
            </div>
          </div>

          <div v-else-if="widget.widget_type === 'activity_feed'" class="widget-feed">
            <div v-for="item in (widgetData.activity_feed || []).slice(0, 6)" :key="item.id" class="feed-item">
              <div class="feed-dot"></div>
              <div class="feed-content">
                <span class="feed-text">{{ item.description }}</span>
                <span class="feed-time">{{ formatTime(item.created_at) }}</span>
              </div>
            </div>
            <div v-if="!(widgetData.activity_feed || []).length" class="widget-empty">No recent activity</div>
          </div>

          <div v-else-if="widget.widget_type === 'deal_funnel'" class="widget-funnel">
            <div v-for="(step, idx) in (widgetData.deal_funnel || [])" :key="idx" class="funnel-step" :style="{ width: funnelWidth(step.count, idx) }">
              <span class="funnel-label">{{ step.stage }}</span>
              <span class="funnel-count">{{ step.count }}</span>
            </div>
            <div v-if="!(widgetData.deal_funnel || []).length" class="widget-empty">No funnel data</div>
          </div>

          <div v-else-if="widget.widget_type === 'top_contacts'" class="widget-contacts">
            <div v-for="c in (widgetData.top_contacts || []).slice(0, 5)" :key="c.id" class="contact-row">
              <div class="contact-avatar">{{ (c.first_name || 'U')[0] }}</div>
              <div class="contact-info">
                <span class="contact-name">{{ c.first_name }} {{ c.last_name }}</span>
                <span class="contact-company">{{ c.company_name || '—' }}</span>
              </div>
              <span class="contact-score badge badge-blue">{{ c.health_score || 0 }}</span>
            </div>
            <div v-if="!(widgetData.top_contacts || []).length" class="widget-empty">No contacts</div>
          </div>

          <div v-else-if="widget.widget_type === 'campaign_stats'" class="widget-campaign-stats">
            <div class="camp-stat-row">
              <div class="camp-stat"><span class="camp-val">{{ widgetData.campaign_stats?.total ?? 0 }}</span><span class="camp-lbl">Campaigns</span></div>
              <div class="camp-stat"><span class="camp-val">{{ widgetData.campaign_stats?.sent ?? 0 }}</span><span class="camp-lbl">Sent</span></div>
              <div class="camp-stat"><span class="camp-val">{{ widgetData.campaign_stats?.open_rate ?? 0 }}%</span><span class="camp-lbl">Open Rate</span></div>
            </div>
          </div>

          <div v-else-if="widget.widget_type === 'team_leaderboard'" class="widget-leaderboard">
            <div v-for="(member, idx) in (widgetData.team_leaderboard || []).slice(0, 5)" :key="idx" class="lb-row">
              <span class="lb-rank">#{{ idx + 1 }}</span>
              <span class="lb-name">{{ member.name }}</span>
              <span class="lb-score">{{ member.score }}</span>
            </div>
            <div v-if="!(widgetData.team_leaderboard || []).length" class="widget-empty">No team data</div>
          </div>

          <div v-else-if="widget.widget_type === 'tasks_due'" class="widget-tasks">
            <div v-for="task in (widgetData.tasks_due || []).slice(0, 5)" :key="task.id" class="task-row">
              <span :class="['task-priority', 'p-' + (task.priority || 'medium')]"></span>
              <span class="task-title">{{ task.title }}</span>
            </div>
            <div v-if="!(widgetData.tasks_due || []).length" class="widget-empty">No tasks due today</div>
          </div>

          <div v-else-if="widget.widget_type === 'recent_deals'" class="widget-recent-deals">
            <div v-for="deal in (widgetData.recent_deals || []).slice(0, 5)" :key="deal.id" class="deal-row">
              <div>
                <span class="deal-name">{{ deal.title }}</span>
                <span class="deal-stage badge badge-blue">{{ deal.stage }}</span>
              </div>
              <span class="deal-val">R{{ formatNumber(deal.value) }}</span>
            </div>
            <div v-if="!(widgetData.recent_deals || []).length" class="widget-empty">No recent deals</div>
          </div>

          <div v-else class="widget-empty">Widget loading...</div>
        </div>
      </div>
      </div>
    </div>

    <div v-else-if="!loading && activeWidgets.length === 0" class="empty-state-wrap">
      <div class="empty-state">
        <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="var(--gray-300)" stroke-width="1.5"><rect x="3" y="3" width="7" height="7"/><rect x="14" y="3" width="7" height="7"/><rect x="3" y="14" width="7" height="7"/><rect x="14" y="14" width="7" height="7"/></svg>
        <h3>No widgets yet</h3>
        <p>Add widgets to build your custom dashboard</p>
        <button class="btn btn-primary" @click="resetDefaults">Load Default Widgets</button>
      </div>
    </div>

    <div v-else class="loading-state"><div class="spinner"></div><p>Loading dashboard...</p></div>

    <div v-if="showAddWidget" class="modal-overlay" @click="showAddWidget = false">
      <div class="modal-panel" @click.stop>
        <div class="modal-header">
          <h3>Add Widget</h3>
          <button class="modal-close" @click="showAddWidget = false">&times;</button>
        </div>
        <div class="modal-body">
          <div class="widget-picker">
            <div v-for="w in availableWidgets" :key="w.type" class="widget-option" @click="addWidget(w)">
              <div class="wo-icon">{{ w.icon }}</div>
              <div>
                <div class="wo-name">{{ w.name }}</div>
                <div class="wo-desc">{{ w.desc }}</div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { dashboardWidgetsAPI } from '../api'
import toast from '../utils/toast'
import authService from '../services/auth'
import 'gridstack/dist/gridstack.min.css'
import { GridStack } from 'gridstack'

export default {
  name: 'CustomDashboard',
  data() {
    return {
      grid: null,
      widgets: [],
      widgetData: {},
      loading: true,
      resetting: false,
      showAddWidget: false,
      availableWidgets: [
        { type: 'stat_card', name: 'Stat Card', desc: 'Key metric overview', icon: '📊', width: 3, height: 1 },
        { type: 'pipeline_chart', name: 'Pipeline Chart', desc: 'Deals by stage', icon: '📈', width: 6, height: 1 },
        { type: 'revenue_chart', name: 'Revenue Chart', desc: 'Revenue over time', icon: '💰', width: 6, height: 1 },
        { type: 'activity_feed', name: 'Activity Feed', desc: 'Recent activities', icon: '📋', width: 3, height: 2 },
        { type: 'deal_funnel', name: 'Deal Funnel', desc: 'Sales funnel visual', icon: '🔽', width: 6, height: 1 },
        { type: 'top_contacts', name: 'Top Contacts', desc: 'Highest-scoring contacts', icon: '⭐', width: 3, height: 1 },
        { type: 'campaign_stats', name: 'Campaign Stats', desc: 'Email campaign overview', icon: '✉️', width: 6, height: 1 },
        { type: 'team_leaderboard', name: 'Team Leaderboard', desc: 'Top performers', icon: '🏆', width: 3, height: 1 },
        { type: 'tasks_due', name: 'Tasks Due', desc: 'Tickets due today', icon: '✅', width: 3, height: 1 },
        { type: 'recent_deals', name: 'Recent Deals', desc: 'Latest deal activity', icon: '📝', width: 6, height: 1 },
      ]
    }
  },
  computed: {
    activeWidgets() {
      return this.widgets.filter(w => w.is_visible)
    },
    canDragDrop() {
      const user = authService.getUser() || {}
      const tier = (user.tier || '').toLowerCase()
      const isAdmin = user.is_superuser || (user.username || '').toLowerCase() === 'adminluxury'
      return isAdmin || ['luxury', 'premium', 'ultimate', 'enterprise'].includes(tier)
    },
    maxPipeCount() {
      return Math.max(...(this.widgetData.pipeline_chart || []).map(s => s.count), 1)
    },
    maxRevValue() {
      return Math.max(...(this.widgetData.revenue_chart?.months || []).map(m => m.value), 1)
    }
  },
  mounted() {
    this.fetchWidgets()
  },
  methods: {
    formatNumber(n) {
      return parseFloat(n || 0).toLocaleString('en-ZA', { minimumFractionDigits: 0, maximumFractionDigits: 0 })
    },
    formatTime(d) {
      if (!d) return ''
      const dt = new Date(d)
      const now = new Date()
      const diff = Math.floor((now - dt) / 60000)
      if (diff < 60) return `${diff}m ago`
      if (diff < 1440) return `${Math.floor(diff / 60)}h ago`
      return dt.toLocaleDateString('en-ZA', { day: 'numeric', month: 'short' })
    },
    initGrid() {
      if (this.grid) {
        this.grid.destroy(false);
      }
      this.grid = GridStack.init({
        cellHeight: 180,
        margin: 16,
        disableResize: !this.canDragDrop,
        disableDrag: !this.canDragDrop,
        handle: '.draggable-header',
        animate: true,
        float: true // Allows widgets to be freely placed without auto-snapping up
      }, this.$refs.gridContainer);

      this.grid.on('change', (event, items) => {
        if (!items) return;
        const positions = items.map(item => ({
          id: item.id,
          x: item.x,
          y: item.y,
          w: item.w,
          h: item.h
        }));
        dashboardWidgetsAPI.reorder(positions).catch(e => console.error('Failed to save layout', e));
      });
    },
    pipeWidth(count) {
      return (count / this.maxPipeCount * 100) + '%'
    },
    revHeight(value) {
      return Math.max((value / this.maxRevValue * 100), 4) + '%'
    },
    funnelWidth(count, idx) {
      const base = 100 - (idx * 12)
      return Math.max(base, 30) + '%'
    },
    async fetchWidgets() {
      this.loading = true
      try {
        const res = await dashboardWidgetsAPI.getAll()
        let fetchedWidgets = res.data.results || res.data || []
        if (fetchedWidgets.length === 0) {
          await this.resetDefaults()
          return
        }
        
        // Auto-migrate from old 4-column sizes to standard 12-column sizes seamlessly
        if (fetchedWidgets.some(w => w.width <= 2)) {
           fetchedWidgets = fetchedWidgets.map(w => {
             w.width = w.width * 3
             w.position_x = (w.position_x || 0) * 3
             return w
           })
        }
        this.widgets = fetchedWidgets

        this.$nextTick(() => {
          this.initGrid()
        })
        this.loadWidgetData()
      } catch (e) {
        toast.error('Failed to load dashboard')
      } finally {
        this.loading = false
      }
    },
    async loadWidgetData() {
      const types = [...new Set(this.activeWidgets.map(w => w.widget_type))]
      for (const type of types) {
        try {
          const res = await dashboardWidgetsAPI.getWidgetData(type)
          this.widgetData[type] = res.data
        } catch {
          this.widgetData[type] = null
        }
      }
      
      this.widgetData = { ...this.widgetData }
    },
    async addWidget(w) {
      try {
        await dashboardWidgetsAPI.create({
          widget_type: w.type,
          title: w.name,
          width: w.width,
          height: w.height,
          position_x: 0,
          position_y: this.widgets.length
        })
        toast.success(`${w.name} widget added`)
        this.showAddWidget = false
        this.fetchWidgets()
      } catch (e) {
        toast.error(e.message || 'Failed to add widget')
      }
    },
    async toggleVisibility(widget) {
      try {
        await dashboardWidgetsAPI.update(widget.id, { ...widget, is_visible: false })
        widget.is_visible = false
        toast.success('Widget hidden')
      } catch (e) {
        toast.error('Failed to hide widget')
      }
    },
    async removeWidget(widget) {
      if (!confirm(`Remove "${widget.title}" widget?`)) return
      try {
        await dashboardWidgetsAPI.delete(widget.id)
        this.widgets = this.widgets.filter(w => w.id !== widget.id)
        toast.success('Widget removed')
      } catch (e) {
        toast.error('Failed to remove widget')
      }
    },
    async resetDefaults() {
      this.resetting = true
      try {
        await dashboardWidgetsAPI.resetDefaults()
        toast.success('Dashboard reset to defaults')
        this.fetchWidgets()
      } catch (e) {
        toast.error(e.message || 'Failed to reset dashboard')
      } finally {
        this.resetting = false
      }
    }
  }
}
</script>

<style scoped>
.page-wrap { padding: 24px; max-width: 1400px; margin: 0 auto; }
.page-header { display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 24px; flex-wrap: wrap; gap: 12px; }
.page-header h1 { font-size: 24px; font-weight: 700; color: #ffffff; margin: 0; }
.page-subtitle { color: #9ca3af; font-size: 14px; margin-top: 4px; }
.header-actions { display: flex; gap: 8px; }

.luxury-badge { display: inline-flex; align-items: center; gap: 6px; margin-top: 10px; padding: 4px 10px; background: rgba(212, 175, 55, 0.1); border: 1px solid rgba(212, 175, 55, 0.2); border-radius: 6px; color: #D4AF37; font-size: 11px; font-weight: 600; letter-spacing: 0.05em; text-transform: uppercase; }

.empty-state-wrap { padding-top: 40px; }
.grid-stack { background: transparent; }
.grid-stack-item-content { border-radius: 12px; overflow: hidden; }
.widget-card { height: 100%; background: rgba(15, 15, 15, 0.8) !important; border: 1px solid rgba(212, 175, 55, 0.2) !important; border-radius: 12px; padding: 0; display: flex; flex-direction: column; overflow: hidden; box-shadow: 0 4px 12px rgba(0,0,0,0.5); }

.widget-header { display: flex; justify-content: space-between; align-items: center; padding: 14px 16px 10px; border-bottom: 1px solid rgba(255, 255, 255, 0.05); background: rgba(0,0,0,0.4); }
.draggable-header { cursor: grab; }
.draggable-header:active { cursor: grabbing; }
.widget-header h3 { font-size: 13px; font-weight: 600; color: #D4AF37; margin: 0; text-transform: uppercase; letter-spacing: 0.04em; }
.widget-controls { display: flex; gap: 4px; }

.widget-body { padding: 16px; flex: 1; overflow-y: auto; }

/* Stat Card */
.widget-stat { text-align: center; padding: 20px 0; }
.stat-big { font-size: 40px; font-weight: 800; color: #ffffff; text-shadow: 0 0 12px rgba(212, 175, 55, 0.3); }
.stat-sub { font-size: 13px; color: #9ca3af; margin-top: 4px; }

/* Pipeline */
.pipe-bar-row { display: flex; align-items: center; gap: 10px; margin-bottom: 8px; }
.pipe-label { width: 90px; font-size: 12px; color: #d1d5db; text-transform: capitalize; }
.pipe-bar-track { flex: 1; height: 20px; background: rgba(255,255,255,0.05); border-radius: 4px; overflow: hidden; }
.pipe-bar-fill { height: 100%; background: linear-gradient(90deg, #D4AF37, #B49015); border-radius: 4px; transition: width 0.5s; }
.pipe-val { width: 30px; text-align: right; font-size: 13px; font-weight: 600; color: #ffffff; }

/* Revenue */
.rev-total { font-size: 28px; font-weight: 700; color: #D4AF37; text-align: center; text-shadow: 0 0 10px rgba(212,175,55,0.3); }
.rev-label { font-size: 12px; color: #9ca3af; text-align: center; margin-bottom: 16px; }
.rev-bars { display: flex; align-items: flex-end; justify-content: center; gap: 8px; height: 80px; }
.rev-bar-col { display: flex; flex-direction: column; align-items: center; flex: 1; }
.rev-bar { width: 100%; max-width: 24px; background: linear-gradient(180deg, #D4AF37, #B49015); border-radius: 4px 4px 0 0; transition: height 0.5s; min-height: 4px; }
.rev-month { font-size: 10px; color: #9ca3af; margin-top: 4px; }

/* Feed */
.feed-item { display: flex; gap: 10px; padding: 6px 0; }
.feed-dot { width: 8px; height: 8px; border-radius: 50%; background: #D4AF37; margin-top: 5px; flex-shrink: 0; box-shadow: 0 0 8px rgba(212,175,55,0.6); }
.feed-content { min-width: 0; }
.feed-text { font-size: 13px; color: #d1d5db; display: block; }
.feed-time { font-size: 11px; color: #6b7280; }

/* Funnel */
.widget-funnel { display: flex; flex-direction: column; align-items: center; gap: 4px; }
.funnel-step { padding: 8px 16px; background: rgba(212, 175, 55, 0.1); border: 1px solid rgba(212, 175, 55, 0.2); border-radius: 6px; display: flex; justify-content: space-between; font-size: 13px; transition: width 0.3s; }
.funnel-label { color: #d1d5db; text-transform: capitalize; }
.funnel-count { font-weight: 700; color: #ffffff; }

/* Top Contacts */
.contact-row { display: flex; align-items: center; gap: 10px; padding: 6px 0; }
.contact-avatar { width: 30px; height: 30px; border-radius: 50%; background: rgba(212, 175, 55, 0.2); border: 1px solid rgba(212,175,55,0.4); color: #D4AF37; display: flex; align-items: center; justify-content: center; font-size: 13px; font-weight: 600; flex-shrink: 0; }
.contact-info { min-width: 0; flex: 1; }
.contact-name { font-size: 13px; font-weight: 500; color: #ffffff; display: block; }
.contact-company { font-size: 11px; color: #9ca3af; }
.contact-score { margin-left: auto; }

/* Campaign Stats */
.camp-stat-row { display: flex; gap: 20px; justify-content: center; }
.camp-stat { text-align: center; }
.camp-val { display: block; font-size: 28px; font-weight: 700; color: #ffffff; }
.camp-lbl { font-size: 11px; color: #9ca3af; text-transform: uppercase; }

/* Leaderboard */
.lb-row { display: flex; align-items: center; gap: 12px; padding: 6px 0; }
.lb-rank { font-size: 14px; font-weight: 700; color: #6b7280; width: 24px; }
.lb-name { flex: 1; font-size: 14px; color: #d1d5db; }
.lb-score { font-weight: 600; color: #D4AF37; }

/* Tasks */
.task-row { display: flex; align-items: center; gap: 10px; padding: 6px 0; }
.task-priority { width: 8px; height: 8px; border-radius: 50%; flex-shrink: 0; }
.p-high { background: #ef4444; box-shadow: 0 0 6px rgba(239, 68, 68, 0.6); }
.p-medium { background: #f59e0b; box-shadow: 0 0 6px rgba(245, 158, 11, 0.6); }
.p-low { background: #22c55e; box-shadow: 0 0 6px rgba(34, 197, 94, 0.6); }
.task-title { font-size: 13px; color: #ffffff; }

/* Recent Deals */
.deal-row { display: flex; justify-content: space-between; align-items: center; padding: 6px 0; }
.deal-name { font-size: 13px; font-weight: 500; color: #ffffff; margin-right: 6px; }
.deal-stage { font-size: 10px; }
.deal-val { font-size: 13px; font-weight: 600; color: #d1d5db; white-space: nowrap; }

.widget-empty { text-align: center; padding: 20px; color: #6b7280; font-size: 13px; }

/* Widget Picker */
.widget-picker { display: grid; grid-template-columns: repeat(auto-fill, minmax(240px, 1fr)); gap: 12px; }
.widget-option { display: flex; gap: 12px; padding: 14px; border: 1px solid rgba(255,255,255,0.1); border-radius: 10px; cursor: pointer; transition: all 0.15s; background: rgba(255,255,255,0.02); }
.widget-option:hover { border-color: #D4AF37; background: rgba(212, 175, 55, 0.05); }
.wo-icon { font-size: 24px; }
.wo-name { font-size: 14px; font-weight: 600; color: #ffffff; }
.wo-desc { font-size: 12px; color: #9ca3af; }

.btn-icon { background: none; border: none; cursor: pointer; padding: 4px; color: var(--gray-400); border-radius: 4px; }
.btn-icon:hover { background: var(--gray-100); color: var(--gray-600); }

.badge { display: inline-block; padding: 2px 8px; border-radius: 20px; font-size: 11px; font-weight: 600; }
.badge-blue { background: rgba(212, 175, 55, 0.1); color: #D4AF37; border: 1px solid rgba(212, 175, 55, 0.2); }

.empty-state { text-align: center; padding: 60px 20px; color: #9ca3af; grid-column: 1 / -1; }
.empty-state h3 { color: #D4AF37; margin: 12px 0 4px; }
.empty-state p { margin-bottom: 16px; }

.btn-secondary { background: rgba(255,255,255,0.05); color: #d1d5db; border: 1px solid rgba(255,255,255,0.1); }
.btn-secondary:hover { background: rgba(255,255,255,0.1); color: #fff; }

.modal-panel { background: linear-gradient(135deg, rgba(15,15,15,0.95), rgba(5,5,5,0.95)); border: 1px solid rgba(212, 175, 55, 0.3); border-radius: 16px; width: 95%; max-width: 640px; max-height: 90vh; overflow-y: auto; }
.modal-header { display: flex; justify-content: space-between; align-items: center; padding: 20px 24px; border-bottom: 1px solid rgba(212, 175, 55, 0.2); }
.modal-header h3 { font-size: 18px; font-weight: 600; margin: 0; color: #fff; }
.modal-close { background: none; border: none; font-size: 24px; cursor: pointer; color: #9ca3af; transition: color 0.2s; }
.modal-close:hover { color: #D4AF37; }
.modal-body { padding: 24px; }

.loading-state { display: flex; flex-direction: column; align-items: center; padding: 60px; color: var(--gray-500); }
.spinner { width: 32px; height: 32px; border: 3px solid rgba(212, 175, 55, 0.2); border-top-color: #D4AF37; border-radius: 50%; animation: spin 0.8s linear infinite; }
@keyframes spin { to { transform: rotate(360deg); } }

</style>

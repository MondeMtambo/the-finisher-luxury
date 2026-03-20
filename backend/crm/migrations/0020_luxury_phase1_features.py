# Generated migration for LUXURY Phase 1 features
# Product Catalog, Line Items, Email Campaigns, Workflows, Custom Dashboards

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('crm', '0019_admp_hierarchy_onboarding_offboarding'),
    ]

    operations = [
        # ──────────────────────────────────────────────────────────
        # Product Catalog
        # ──────────────────────────────────────────────────────────
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('description', models.TextField(blank=True)),
                ('sku', models.CharField(blank=True, help_text='Stock Keeping Unit / Product Code', max_length=100)),
                ('price', models.DecimalField(decimal_places=2, help_text='Unit price in ZAR', max_digits=12)),
                ('cost', models.DecimalField(blank=True, decimal_places=2, help_text='Cost price for margin calculation', max_digits=12, null=True)),
                ('tax_rate', models.DecimalField(decimal_places=2, default=15.00, help_text='VAT rate (default 15% for SA)', max_digits=5)),
                ('is_active', models.BooleanField(default=True)),
                ('category', models.CharField(blank=True, help_text='Product category (e.g. Software, Service, Hardware)', max_length=100)),
                ('unit', models.CharField(default='each', help_text='Unit of measure (each, hour, month, licence)', max_length=50)),
                ('company_name', models.CharField(help_text='Company that owns this product', max_length=200)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='products_created', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['category', 'name'],
                'unique_together': {('company_name', 'sku')},
            },
        ),

        # ──────────────────────────────────────────────────────────
        # Line Items (linked to Deal + Product)
        # ──────────────────────────────────────────────────────────
        migrations.CreateModel(
            name='LineItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(blank=True, help_text='Override product description for this line', max_length=300)),
                ('quantity', models.DecimalField(decimal_places=2, default=1, max_digits=10)),
                ('unit_price', models.DecimalField(decimal_places=2, help_text='Price per unit (copied from product, can be overridden)', max_digits=12)),
                ('discount_percent', models.DecimalField(decimal_places=2, default=0, max_digits=5)),
                ('tax_rate', models.DecimalField(decimal_places=2, default=15.00, max_digits=5)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('deal', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='line_items', to='crm.deal')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='line_items', to='crm.product')),
            ],
            options={
                'ordering': ['created_at'],
            },
        ),

        # ──────────────────────────────────────────────────────────
        # Email Templates
        # ──────────────────────────────────────────────────────────
        migrations.CreateModel(
            name='EmailTemplate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('template_type', models.CharField(choices=[('welcome', 'Welcome'), ('follow_up', 'Follow-Up'), ('proposal', 'Proposal'), ('thank_you', 'Thank You'), ('newsletter', 'Newsletter'), ('custom', 'Custom')], default='custom', max_length=20)),
                ('subject', models.CharField(max_length=300)),
                ('body_html', models.TextField(help_text='HTML body. Use {{first_name}}, {{last_name}}, {{company}}, {{email}} as merge fields.')),
                ('company_name', models.CharField(max_length=200)),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='email_templates', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-updated_at'],
            },
        ),

        # ──────────────────────────────────────────────────────────
        # Email Campaigns
        # ──────────────────────────────────────────────────────────
        migrations.CreateModel(
            name='EmailCampaign',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('subject', models.CharField(max_length=300)),
                ('body_html', models.TextField()),
                ('status', models.CharField(choices=[('draft', 'Draft'), ('scheduled', 'Scheduled'), ('sending', 'Sending'), ('sent', 'Sent'), ('paused', 'Paused'), ('failed', 'Failed')], default='draft', max_length=20)),
                ('recipient_filter', models.JSONField(blank=True, default=dict, help_text='Filter criteria: {company_id, tags, all}')),
                ('recipient_ids', models.JSONField(blank=True, default=list, help_text='Explicit list of contact IDs')),
                ('total_recipients', models.IntegerField(default=0)),
                ('sent_count', models.IntegerField(default=0)),
                ('open_count', models.IntegerField(default=0)),
                ('click_count', models.IntegerField(default=0)),
                ('bounce_count', models.IntegerField(default=0)),
                ('scheduled_at', models.DateTimeField(blank=True, null=True)),
                ('sent_at', models.DateTimeField(blank=True, null=True)),
                ('company_name', models.CharField(max_length=200)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('template', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='crm.emailtemplate')),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='email_campaigns', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),

        # ──────────────────────────────────────────────────────────
        # Campaign Recipients (per-contact tracking)
        # ──────────────────────────────────────────────────────────
        migrations.CreateModel(
            name='CampaignRecipient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('sent', 'Sent'), ('opened', 'Opened'), ('clicked', 'Clicked'), ('bounced', 'Bounced'), ('failed', 'Failed')], default='pending', max_length=20)),
                ('sent_at', models.DateTimeField(blank=True, null=True)),
                ('opened_at', models.DateTimeField(blank=True, null=True)),
                ('clicked_at', models.DateTimeField(blank=True, null=True)),
                ('campaign', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recipients', to='crm.emailcampaign')),
                ('contact', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='crm.contact')),
            ],
            options={
                'ordering': ['-sent_at'],
                'unique_together': {('campaign', 'contact')},
            },
        ),

        # ──────────────────────────────────────────────────────────
        # Workflow Automation
        # ──────────────────────────────────────────────────────────
        migrations.CreateModel(
            name='Workflow',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('description', models.TextField(blank=True)),
                ('trigger_type', models.CharField(choices=[('deal_stage_change', 'Deal Stage Changes'), ('deal_created', 'New Deal Created'), ('deal_value_above', 'Deal Value Exceeds Threshold'), ('contact_created', 'New Contact Added'), ('contact_no_activity', 'Contact Inactive For X Days'), ('ticket_created', 'New Ticket Created'), ('ticket_overdue', 'Ticket Past Due Date')], max_length=30)),
                ('trigger_config', models.JSONField(blank=True, default=dict, help_text="Trigger parameters, e.g. {stage_from: 'lead', stage_to: 'qualified'} or {days: 14}")),
                ('is_active', models.BooleanField(default=True)),
                ('company_name', models.CharField(max_length=200)),
                ('run_count', models.IntegerField(default=0)),
                ('last_run_at', models.DateTimeField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='workflows', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-updated_at'],
            },
        ),

        # ──────────────────────────────────────────────────────────
        # Workflow Actions
        # ──────────────────────────────────────────────────────────
        migrations.CreateModel(
            name='WorkflowAction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('action_type', models.CharField(choices=[('send_email', 'Send Email'), ('create_task', 'Create Task/Ticket'), ('notify_user', 'Send Notification'), ('change_stage', 'Change Deal Stage'), ('assign_user', 'Assign To User'), ('add_note', 'Add Note/Activity'), ('wait', 'Wait (Delay)')], max_length=20)),
                ('action_config', models.JSONField(default=dict, help_text="Action parameters. E.g. {template_id: 1, delay_hours: 24, stage: 'proposal'}")),
                ('order', models.PositiveIntegerField(default=0, help_text='Execution order (0 = first)')),
                ('workflow', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='actions', to='crm.workflow')),
            ],
            options={
                'ordering': ['order'],
            },
        ),

        # ──────────────────────────────────────────────────────────
        # Workflow Logs
        # ──────────────────────────────────────────────────────────
        migrations.CreateModel(
            name='WorkflowLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('trigger_entity_type', models.CharField(max_length=50)),
                ('trigger_entity_id', models.IntegerField()),
                ('trigger_entity_name', models.CharField(blank=True, max_length=255)),
                ('actions_executed', models.JSONField(default=list, help_text='List of action results')),
                ('status', models.CharField(choices=[('success', 'Success'), ('partial', 'Partial'), ('failed', 'Failed')], default='success', max_length=20)),
                ('error_message', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('workflow', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='logs', to='crm.workflow')),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),

        # ──────────────────────────────────────────────────────────
        # Dashboard Widgets
        # ──────────────────────────────────────────────────────────
        migrations.CreateModel(
            name='DashboardWidget',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('widget_type', models.CharField(choices=[('stat_card', 'Stat Card'), ('pipeline_chart', 'Pipeline Chart'), ('revenue_chart', 'Revenue Over Time'), ('activity_feed', 'Activity Feed'), ('deal_funnel', 'Deal Funnel'), ('top_contacts', 'Top Contacts'), ('campaign_stats', 'Campaign Stats'), ('team_leaderboard', 'Team Leaderboard'), ('tasks_due', 'Tasks Due Today'), ('recent_deals', 'Recent Deals')], max_length=30)),
                ('title', models.CharField(max_length=100)),
                ('config', models.JSONField(blank=True, default=dict, help_text='Widget-specific configuration (date range, filters, etc)')),
                ('position_x', models.IntegerField(default=0)),
                ('position_y', models.IntegerField(default=0)),
                ('width', models.IntegerField(default=1, help_text='Grid columns (1-4)')),
                ('height', models.IntegerField(default=1, help_text='Grid rows (1-3)')),
                ('is_visible', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='dashboard_widgets', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['position_y', 'position_x'],
            },
        ),

        # ──────────────────────────────────────────────────────────
        # Dashboard Layouts
        # ──────────────────────────────────────────────────────────
        migrations.CreateModel(
            name='DashboardLayout',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('is_default', models.BooleanField(default=False)),
                ('widget_config', models.JSONField(default=list, help_text='Serialized list of widget configs for this layout')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='dashboard_layouts', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-is_default', '-updated_at'],
            },
        ),
    ]

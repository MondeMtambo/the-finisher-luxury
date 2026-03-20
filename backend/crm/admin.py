from django.contrib import admin
from .models import (Contact, Company, Deal, UserProfile, DeletedUserLog,
                     Asset, AssetCategory, Division, OnboardingLog, OffboardingRequest,
                     Product, LineItem, EmailTemplate, EmailCampaign, CampaignRecipient,
                     Workflow, WorkflowAction, WorkflowLog, DashboardWidget, DashboardLayout)


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'role', 'payment_status', 'is_banned', 'created_at']
    search_fields = ['user__username', 'user__email', 'company_name']
    list_filter = ['role', 'payment_status', 'is_banned', 'created_at']


@admin.register(DeletedUserLog)
class DeletedUserLogAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'deleted_at', 'deleted_reason']
    search_fields = ['username', 'email', 'deleted_reason']
    list_filter = ['deleted_at']


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'phone', 'created_at']
    search_fields = ['name', 'email']


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'email', 'company', 'is_self_employed', 'created_at']
    search_fields = ['first_name', 'last_name', 'email', 'company_name_manual']
    list_filter = ['company', 'is_self_employed', 'created_at']


@admin.register(Deal)
class DealAdmin(admin.ModelAdmin):
    list_display = ['title', 'contact', 'value', 'stage', 'created_at']
    search_fields = ['title', 'contact__first_name', 'contact__last_name']
    list_filter = ['stage', 'created_at']

@admin.register(Division)
class DivisionAdmin(admin.ModelAdmin):
    list_display = ['name', 'company_name', 'manager', 'created_at']
    search_fields = ['name', 'company_name', 'manager__username']
    list_filter = ['company_name', 'created_at']


@admin.register(AssetCategory)
class AssetCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'category_type', 'company_name', 'created_at']
    search_fields = ['name', 'company_name']
    list_filter = ['category_type', 'company_name', 'created_at']


@admin.register(Asset)
class AssetAdmin(admin.ModelAdmin):
    list_display = ['asset_tag', 'name', 'category', 'status', 'condition', 'assigned_to', 'company_name', 'created_at']
    search_fields = ['asset_tag', 'name', 'serial_number', 'company_name']
    list_filter = ['status', 'condition', 'category', 'company_name', 'created_at']
    readonly_fields = ['created_at', 'updated_at']

@admin.register(OnboardingLog)
class OnboardingLogAdmin(admin.ModelAdmin):
    list_display = ['employee_name', 'employee_email', 'action', 'performed_by_name', 'company_name', 'role_assigned', 'created_at']
    search_fields = ['employee_name', 'employee_email', 'performed_by_name', 'company_name']
    list_filter = ['action', 'company_name', 'created_at']
    readonly_fields = ['created_at']


@admin.register(OffboardingRequest)
class OffboardingRequestAdmin(admin.ModelAdmin):
    list_display = ['employee_name', 'employee_email', 'requested_by_name', 'company_name', 'status', 'created_at']
    search_fields = ['employee_name', 'employee_email', 'requested_by_name', 'company_name']
    list_filter = ['status', 'company_name', 'created_at']
    readonly_fields = ['created_at']




@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'sku', 'price', 'category', 'is_active', 'company_name', 'created_at']
    search_fields = ['name', 'sku', 'category', 'company_name']
    list_filter = ['is_active', 'category', 'company_name']


class LineItemInline(admin.TabularInline):
    model = LineItem
    extra = 0
    readonly_fields = ['subtotal', 'tax_amount', 'total']




@admin.register(EmailTemplate)
class EmailTemplateAdmin(admin.ModelAdmin):
    list_display = ['name', 'template_type', 'subject', 'company_name', 'is_active']
    list_filter = ['template_type', 'is_active', 'company_name']


@admin.register(EmailCampaign)
class EmailCampaignAdmin(admin.ModelAdmin):
    list_display = ['name', 'status', 'total_recipients', 'sent_count', 'open_count', 'company_name', 'created_at']
    list_filter = ['status', 'company_name']
    readonly_fields = ['sent_count', 'open_count', 'click_count', 'bounce_count']




class WorkflowActionInline(admin.TabularInline):
    model = WorkflowAction
    extra = 0


@admin.register(Workflow)
class WorkflowAdmin(admin.ModelAdmin):
    list_display = ['name', 'trigger_type', 'is_active', 'run_count', 'company_name', 'created_at']
    list_filter = ['trigger_type', 'is_active', 'company_name']
    inlines = [WorkflowActionInline]




@admin.register(DashboardWidget)
class DashboardWidgetAdmin(admin.ModelAdmin):
    list_display = ['user', 'widget_type', 'title', 'position_x', 'position_y', 'is_visible']
    list_filter = ['widget_type', 'is_visible']


@admin.register(DashboardLayout)
class DashboardLayoutAdmin(admin.ModelAdmin):
    list_display = ['user', 'name', 'is_default', 'created_at']
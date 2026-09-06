from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView
from . import views
from . import auth_views
from . import access_request_views

router = DefaultRouter()
router.register(r'contacts', views.ContactViewSet, basename='contact')
router.register(r'companies', views.CompanyViewSet, basename='company')
router.register(r'deals', views.DealViewSet, basename='deal')
router.register(r'activities', views.ActivityLogViewSet, basename='activity')
router.register(r'tickets', views.TicketViewSet, basename='ticket')
router.register(r'notifications', views.NotificationViewSet, basename='notification')
router.register(r'employees', views.EmployeeViewSet, basename='employee')

router.register(r'assets', views.AssetViewSet, basename='asset')
router.register(r'asset-categories', views.AssetCategoryViewSet, basename='assetcategory')
router.register(r'divisions', views.DivisionViewSet, basename='division')

router.register(r'products', views.ProductViewSet, basename='product')
router.register(r'line-items', views.LineItemViewSet, basename='lineitem')
router.register(r'email-templates', views.EmailTemplateViewSet, basename='emailtemplate')
router.register(r'email-campaigns', views.EmailCampaignViewSet, basename='emailcampaign')
router.register(r'workflows', views.WorkflowViewSet, basename='workflow')
router.register(r'dashboard-widgets', views.DashboardWidgetViewSet, basename='dashboardwidget')
router.register(r'dashboard-layouts', views.DashboardLayoutViewSet, basename='dashboardlayout')
router.register(r'website-leads', views.WebsiteLeadViewSet, basename='websitelead')
router.register(r'audit-trail', views.SecurityAuditTrailViewSet, basename='audittrail')

urlpatterns = [
    path('', views.api_overview, name='api_overview'),

    path('api/auth/register/', auth_views.RegisterView.as_view(), name='register'),
    path('api/auth/login/', auth_views.LoginView.as_view(), name='token_obtain_pair'),
    path('api/auth/verify-mfa/', auth_views.VerifyMFAView.as_view(), name='verify_mfa'),
    path('api/auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/auth/profile/', auth_views.UserProfileView.as_view(), name='user_profile'),
    path('api/auth/force-change-password/', auth_views.ForceChangePasswordView.as_view(), name='force_change_password'),
    path('api/auth/change-password/', auth_views.ChangePasswordView.as_view(), name='change_password'),
    path('api/auth/password-reset/', auth_views.PasswordResetRequestView.as_view(), name='password_reset'),
    path('api/auth/password-reset/verify-otp/', auth_views.PasswordResetVerifyOTPView.as_view(), name='password_reset_verify_otp'),
    path('api/auth/password-reset-confirm/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('api/auth/logout/', auth_views.LogoutView.as_view(), name='logout'),
    
    # Public endpoints (zero auth required)
    path('api/public/leads/', views.public_lead_capture, name='public_lead_capture'),
    path('api/public/request-access/', access_request_views.PublicAccessRequestView.as_view(), name='public_request_access'),
    path('api/public/verify-access-request/', access_request_views.PublicVerifyAccessRequestView.as_view(), name='public_verify_access_request'),
    path('api/public/cancel-access-request/<uuid:pk>/', access_request_views.PublicCancelAccessRequestView.as_view(), name='public_cancel_access_request'),
    path('api/public/search-ceo/', access_request_views.PublicCEOSearchView.as_view(), name='public_search_ceo'),

    path('api/', include(router.urls)),
    path('api/prerequisites/', views.prerequisite_status, name='prerequisite_status'),
    path('health/', views.health, name='health'),
    path('api/performance/me/', views.performance_me, name='performance_me'),
    path('api/performance/user/<int:user_id>/', views.performance_user, name='performance_user'),
    path('api/admin/overview/', views.AdminOverviewView.as_view(), name='admin_overview'),
    path('api/admin/website-leads/inbox/', views.AdminWebsiteLeadInboxView.as_view(), name='admin_website_leads_inbox'),
    path('api/admin/users/', views.UserManagementView.as_view(), name='user_management'),
    path('api/admin/clients-employees/', views.ClientEmployeeManagementView.as_view(), name='client_employee_management'),

    # Corporate Access Requests (Executive Admin Review & Provisioning)
    path('api/admin/access-requests/', access_request_views.AdminAccessRequestListView.as_view(), name='admin_access_requests'),
    path('api/admin/access-requests/<uuid:pk>/action/', access_request_views.AdminAccessRequestActionView.as_view(), name='admin_access_request_action'),

    # Billing & 14-Day VIP Trial Management
    path('api/billing/status/', views.OrganizationBillingStatusView.as_view(), name='billing_status'),
    path('api/billing/checkout/', views.CreateCheckoutSessionView.as_view(), name='billing_checkout'),
    path('api/billing/webhook/', views.BillingWebhookView.as_view(), name='billing_webhook'),
    path('api/admin/sales-ledger/', views.PrivateSalesLedgerView.as_view(), name='private_sales_ledger'),

    # CIPC Business Verification & Compliance
    path('api/tenant/verification/', views.TenantVerificationView.as_view(), name='tenant_verification'),
    path('api/admin/tenant-verifications/', views.AdminTenantVerificationListView.as_view(), name='admin_tenant_verifications'),
    path('api/admin/tenant-verifications/<uuid:pk>/review/', views.AdminTenantVerificationReviewView.as_view(), name='admin_tenant_verification_review'),
]
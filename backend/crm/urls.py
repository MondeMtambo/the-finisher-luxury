from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView
from . import views
from . import auth_views

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

    path('api/', include(router.urls)),
    path('api/prerequisites/', views.prerequisite_status, name='prerequisite_status'),
    path('health/', views.health, name='health'),
    path('api/performance/me/', views.performance_me, name='performance_me'),
    path('api/performance/user/<int:user_id>/', views.performance_user, name='performance_user'),
    path('api/admin/overview/', views.AdminOverviewView.as_view(), name='admin_overview'),
    path('api/admin/users/', views.UserManagementView.as_view(), name='user_management'),
    path('api/admin/clients-employees/', views.ClientEmployeeManagementView.as_view(), name='client_employee_management'),
]
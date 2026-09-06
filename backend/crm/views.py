from rest_framework import viewsets, status
from rest_framework.decorators import api_view, action, permission_classes
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from django.db import IntegrityError, transaction
from django.db.models import Q, Count, Sum
from django.contrib.auth.models import User
from django.conf import settings
from django.core.mail import send_mail
from django.utils import timezone
from datetime import timedelta, datetime
import csv
import io
from .models import Contact, Company, Deal, ActivityLog, UserProfile, DeletedUserLog, Ticket, Notification, Asset, AssetCategory, Division, OnboardingLog, OffboardingRequest, Product, LineItem, EmailTemplate, EmailCampaign, CampaignRecipient, Workflow, WorkflowAction, WorkflowLog, DashboardWidget, DashboardLayout, WebsiteLead, SecurityAuditTrail, TenantVerification, Organization
from .utils import OWNER_ADMIN_USERNAME, is_owner_admin_user, normalize_company_name
from .audit_utils import record_audit_event
from .whatsapp import send_lead_welcome_message
from .serializers import (
    ContactSerializer, 
    CompanySerializer, 
    TenantVerificationSerializer,
    TenantVerificationReviewSerializer, 
    DealSerializer,
    ActivityLogSerializer,
    TicketSerializer,
    NotificationSerializer,
    EmployeeSerializer,
    EmployeeCreateSerializer,
    AssetSerializer,
    AssetCategorySerializer,
    DivisionSerializer,
    OnboardingLogSerializer,
    OffboardingRequestSerializer,
    OffboardingRequestCreateSerializer,
    ProductSerializer,
    SecurityAuditTrailSerializer,
    LineItemSerializer,
    EmailTemplateSerializer,
    EmailCampaignSerializer,
    CampaignRecipientSerializer,
    WorkflowSerializer,
    WorkflowActionSerializer,
    WorkflowLogSerializer,
    DashboardWidgetSerializer,
    DashboardLayoutSerializer,
    WebsiteLeadSerializer,
    WebsiteLeadUpdateSerializer,
    WebsiteLeadReplySerializer,
)
from .tier_limits import LUXURY_TIER_LIMITS, check_org_quota, TIER_QUOTAS, can_add_user, get_remaining_user_slots

def has_user_management_access(request):
    """Determine whether the requester has permission to manage users."""
    user = getattr(request, 'user', None)
    if not user or not user.is_authenticated:
        return False

    if user.is_superuser:
        return True

    if is_owner_admin_user(user):
        return True

    return False


def visible_contacts_queryset(user):
    """Return contacts that should appear in client-facing operational CRM views.
    Enforces strict Organization multi-tenancy with hierarchical team access (POPIA Sec 19).
    Website inquiries are handled in the dedicated Website Leads inbox and must
    not leak into the Clients tab or contact totals.
    CROSS-TENANT ISOLATION: Operational views NEVER bleed other businesses' clients,
    even for superusers/staff. Multi-tenant oversight across all companies is exclusively 
    handled in the Master Admin Control Deck.
    """
    queryset = Contact.objects.select_related('company', 'organization').filter(website_lead__isnull=True)

    profile = getattr(user, 'profile', None)
    if not profile:
        return queryset.filter(user=user)

    # 1. First-class Organization tenancy (Guaranteed zero cross-tenant data bleed)
    if profile.organization:
        return queryset.filter(organization=profile.organization)

    # 2. Backward compatibility fallback for legacy company_name string
    if profile.company_name:
        company = normalize_company_name(profile.company_name)
        return queryset.filter(
            Q(organization__name__iexact=company) |
            Q(user__profile__company_name__iexact=company)
        )

    # 3. Dedicated owner-admin operational fallback (Mtambo Holdings workspace)
    if is_owner_admin_user(user):
        return queryset.filter(
            Q(organization__slug='mtambo-holdings') |
            Q(user__username=OWNER_ADMIN_USERNAME) |
            Q(user=user)
        )

    return queryset.filter(user=user)


@api_view(['GET'])
@permission_classes([AllowAny])
def api_overview(request):
    """
    API overview endpoint - no auth required.
    """
    return Response({
    'message': 'Welcome to THE FINISHER LUXURY API!',
        'version': '1.0',
        'endpoints': {
            'auth': {
                'register': '/api/auth/register/',
                'login': '/api/auth/login/',
                'refresh': '/api/auth/refresh/',
                'profile': '/api/auth/profile/',
                'change-password': '/api/auth/change-password/',
                'password-reset': '/api/auth/password-reset/',
                'logout': '/api/auth/logout/',
            },
            'crm': {
                'contacts': '/api/contacts/',
                'companies': '/api/companies/',
                'deals': '/api/deals/',
                'activities': '/api/activities/',
            }
        }
    })


@api_view(['GET'])
@permission_classes([AllowAny])
def health(request):
    """Simple health endpoint for load balancers and readiness checks."""
    return Response({
        'status': 'ok',
        'service': 'the-finisher-luxury',
    }, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def public_lead_capture(request):
    """
    Public lead capture endpoint - captures leads from website forms.
    No authentication required.
    
    Expected POST data:
    {
        "first_name": "John",
        "last_name": "Doe",
        "email": "john@example.com",
        "phone": "+27821234567",
        "message": "Interested in your services"
    }
    
    Returns:
    {
        "success": true,
        "lead_id": 123,
        "message": "Lead captured successfully",
        "whatsapp_sent": true
    }
    """
    try:
        data = request.data
        first_name = data.get('first_name', '').strip()
        last_name = data.get('last_name', '').strip()
        email = data.get('email', '').strip()
        phone = data.get('phone', '').strip()
        message = data.get('message', '').strip()
        
        # Validate required fields
        if not all([first_name, last_name, email, phone]):
            return Response({
                'success': False,
                'error': 'Missing required fields: first_name, last_name, email, phone'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Resolve website lead owner to configured account, defaulting to the owner admin username.
        configured_owner_email = getattr(settings, 'PUBLIC_LEAD_OWNER_EMAIL', '').strip()
        configured_owner_username = (
            getattr(settings, 'PUBLIC_LEAD_OWNER_USERNAME', '').strip() or OWNER_ADMIN_USERNAME
        )
        configured_company = getattr(settings, 'PUBLIC_LEAD_COMPANY_NAME', 'Mtambo Holdings').strip() or 'Mtambo Holdings'

        lead_owner = None
        if configured_owner_email:
            lead_owner = User.objects.filter(email__iexact=configured_owner_email).first()
        if not lead_owner and configured_owner_username:
            lead_owner = User.objects.filter(username__iexact=configured_owner_username).first()

        if not lead_owner:
            return Response({
                'success': False,
                'error': (
                    'Website lead owner account not found. '
                    f'Expected username "{configured_owner_username}" or configured owner email.'
                )
            }, status=status.HTTP_503_SERVICE_UNAVAILABLE)

        # Ensure the lead owner profile is tagged to the configured company so company admins can see these contacts.
        lead_profile, _ = UserProfile.objects.get_or_create(
            user=lead_owner,
            defaults={
                'role': 'admin',
                'company_name': configured_company,
                'payment_status': 'paid',
            }
        )
        profile_updates = []
        if not lead_profile.company_name:
            lead_profile.company_name = configured_company
            profile_updates.append('company_name')
        if lead_profile.role != 'admin':
            lead_profile.role = 'admin'
            profile_updates.append('role')
        if profile_updates:
            lead_profile.save(update_fields=profile_updates)
        
        # The Bullshit Filter Engine
        spam_score = 0
        is_spam_risk = False
        
        # Domain check
        email_domain = email.split('@')[-1].lower() if '@' in email else ''
        free_domains = ['gmail.com', 'yahoo.com', 'hotmail.com', 'outlook.com', 'live.com', 'icloud.com']
        spam_domains = ['tempmail.com', '10minutemail.com', 'mailinator.com', 'guerrillamail.com']
        
        if email_domain in spam_domains:
            spam_score -= 50
            is_spam_risk = True
        elif email_domain not in free_domains:
            spam_score += 50  # Corporate domain
            
        # Keyword check
        msg_lower = message.lower()
        spam_keywords = ['seo', 'boost your traffic', 'generate leads', 'dear sir/madam', 'crypto', 'investment', 'guarantee', 'marketing agency', 'web design services']
        good_keywords = ['budget', 'quote', 'timeline', 'looking to hire', 'project', 'pricing', 'interested in']
        
        for kw in spam_keywords:
            if kw in msg_lower:
                spam_score -= 20
                is_spam_risk = True
                
        for kw in good_keywords:
            if kw in msg_lower:
                spam_score += 20
                
        if spam_score < 0:
            is_spam_risk = True

        website_source = data.get('source', 'contact_form')
        if website_source not in ['contact_form', 'chat_widget']:
            website_source = 'contact_form'

        # 👻 Ghost Lead Creation - We STOP creating fake contacts here!
        website_lead = WebsiteLead.objects.create(
            owner=lead_owner,
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone=phone,
            source=website_source,
            inbound_message=message,
            spam_score=spam_score,
            is_spam_risk=is_spam_risk
        )

        Notification.objects.create(
            recipient=lead_owner,
            title='New Website Lead',
            message=f'New website inquiry from {first_name} {last_name}',
            entity_type='website_lead',
            entity_id=website_lead.id,
            meta={
                'source': website_source,
                'spam_score': spam_score,
                'is_spam_risk': is_spam_risk,
            },
        )
        
        # Send WhatsApp welcome message
        whatsapp_result = send_lead_welcome_message(
            contact_name=first_name,
            phone=phone,
            calendar_link='https://calendly.com/mtamboholdings' if data.get('calendar_enabled') else None
        )
        
        return Response({
            'success': True,
            'lead_id': website_lead.id,
            'message': 'Lead captured successfully. Check your WhatsApp!',
            'whatsapp_sent': whatsapp_result['success'],
            'whatsapp_error': whatsapp_result.get('error'),
        }, status=status.HTTP_201_CREATED)
        
    except Exception as e:
        logger.error(f"Error capturing lead: {str(e)}", exc_info=True)
        return Response({
            'success': False,
            'error': f'Error capturing lead: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def trigger_workflows_for_lead(contact, lead_owner):
    """
    Trigger workflows with 'contact_created' trigger for new leads.
    """
    import logging
    logger = logging.getLogger(__name__)
    
    try:
        workflows = Workflow.objects.filter(
            trigger_type='contact_created',
            company_name__iexact='Mtambo Holdings',
            is_active=True
        )
        
        for workflow in workflows:
            try:
                workflow_log = WorkflowLog.objects.create(
                    workflow=workflow,
                    trigger_entity_type='contact',
                    trigger_entity_id=contact.id,
                    trigger_entity_name=f"{contact.first_name} {contact.last_name}",
                    actions_executed=[],
                    status='success'
                )
                
                # Execute workflow actions
                for action in workflow.actions.all().order_by('order'):
                    try:
                        if action.action_type == 'send_whatsapp':
                            # WhatsApp already sent above, but can add more here
                            pass
                        elif action.action_type == 'send_email':
                            # Email notifications can be added here
                            pass
                        elif action.action_type == 'notify_user':
                            Notification.objects.create(
                                recipient=lead_owner,
                                title='New Website Lead',
                                message=f"New website inquiry from {contact.first_name} {contact.last_name}",
                                entity_type='website_lead',
                                entity_id=contact.id
                            )
                    except Exception as e:
                        logger.warning(f"Error executing workflow action {action.id}: {str(e)}")
                        workflow_log.status = 'partial'
                
                workflow_log.save()
                workflow.run_count += 1
                workflow.last_run_at = timezone.now()
                workflow.save()
                
            except Exception as e:
                logger.error(f"Error running workflow {workflow.id}: {str(e)}")
    
    except Exception as e:
        logger.error(f"Error triggering workflows: {str(e)}")


import logging
logger = logging.getLogger(__name__)


def log_activity(user, action, entity_type, entity_id, entity_name, details=''):
    """
    Helper function to log CRUD activities.
    """
    ActivityLog.objects.create(
        user=user,
        action=action,
        entity_type=entity_type,
        entity_id=entity_id,
        entity_name=entity_name,
        details=details
    )


def ensure_company_for_contact(contact):
    """
    Ensure the contact is linked to a company, creating one if needed.
    This function MUST be called after contact.save() to ensure all fields are persisted.
    """

    contact.refresh_from_db()

    potential_names = [
        getattr(contact.company, 'name', '') or '',
        (contact.company_name_manual or '')
    ]
    company_name = next((name.strip() for name in potential_names if name and name.strip()), '')
    
    if not company_name:

        return

    org = getattr(contact, 'organization', None)
    if org:
        company = Company.objects.filter(organization=org, name__iexact=company_name).first()
    else:
        company = Company.objects.filter(user=contact.user, name__iexact=company_name).first()

    if not company:
        company = Company.objects.create(
            user=contact.user, 
            name=company_name,
            organization=org
        )
        log_activity(
            user=contact.user,
            action='create',
            entity_type='company',
            entity_id=company.id,
            entity_name=company.name,
            details=f"Auto-created from contact: {contact.first_name} {contact.last_name}"
        )

    updated_fields = []
    preferred_phone = contact.company_direct_line or contact.phone
    if preferred_phone and not company.phone:
        company.phone = preferred_phone
        updated_fields.append('phone')

    if contact.email and not company.email and not contact.is_self_employed:
        company.email = contact.email
        updated_fields.append('email')

    if getattr(contact, 'cipc_number', None) and not company.registration_number:
        company.registration_number = contact.cipc_number
        updated_fields.append('registration_number')

    if getattr(contact, 'tax_number', None) and not company.tax_number:
        company.tax_number = contact.tax_number
        updated_fields.append('tax_number')

    if updated_fields:
        company.save(update_fields=updated_fields)

    if contact.company_id != company.id:
        contact.company = company
        contact.save(update_fields=['company'])


class ContactViewSet(viewsets.ModelViewSet):
    """
    Contact viewset with strict Organization multi-tenant isolation.
    """
    serializer_class = ContactSerializer
    parser_classes = [MultiPartParser, FormParser, JSONParser]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return visible_contacts_queryset(user)

    def perform_create(self, serializer):
        user = self.request.user
        if not (user.is_superuser or user.is_staff or (getattr(user, 'profile', None) and user.profile.is_admin)):
            raise PermissionDenied('Only administrators can create contacts.')

        profile = getattr(user, 'profile', None)
        org = getattr(profile, 'organization', None) if profile else None

        # ─── CONTACT ALLOCATION QUOTA (Luxury Basic: 5 Contacts max; Trial & Team: Unlimited) ───
        if org:
            existing_count = Contact.objects.filter(organization=org).count()
            allowed, limit, msg = check_org_quota(org, 'contacts', existing_count)
            if not allowed:
                raise ValidationError({'detail': msg})

        contact = serializer.save(user=user, organization=org)
        ensure_company_for_contact(contact)
        log_activity(
            user=self.request.user,
            action='create',
            entity_type='contact',
            entity_id=contact.id,
            entity_name=f"{contact.first_name} {contact.last_name}",
            details=f"Email: {contact.email}"
        )

    def perform_update(self, serializer):

        user = self.request.user
        if not (user.is_superuser or user.is_staff or (getattr(user, 'profile', None) and user.profile.is_admin)):
            raise PermissionDenied('Only administrators can update contacts.')
        contact = serializer.save()
        ensure_company_for_contact(contact)
        log_activity(
            user=self.request.user,
            action='update',
            entity_type='contact',
            entity_id=contact.id,
            entity_name=f"{contact.first_name} {contact.last_name}"
        )

    def perform_destroy(self, instance):

        user = self.request.user
        if not (user.is_superuser or user.is_staff or (getattr(user, 'profile', None) and user.profile.is_admin)):
            raise PermissionDenied('Only administrators can delete contacts.')
        contact_name = f"{instance.first_name} {instance.last_name}"
        contact_id = instance.id
        instance.delete()
        log_activity(
            user=self.request.user,
            action='delete',
            entity_type='contact',
            entity_id=contact_id,
            entity_name=contact_name
        )

    @action(detail=False, methods=['post'], parser_classes=[MultiPartParser, FormParser])
    def import_csv(self, request):
        """
        Import contacts from CSV file.
        LUXURY edition feature.
        POST /api/contacts/import_csv/
        """
        user = request.user
        profile = getattr(user, 'profile', None)
        org = getattr(profile, 'organization', None) if profile else None
        if org and org.subscription_tier == 'basic':
            return Response({
                'error': 'Bulk CSV Import is reserved for Luxury Team. Luxury Basic is limited to 5 VIP contacts.'
            }, status=status.HTTP_403_FORBIDDEN)

        file = request.FILES.get('file')
        
        if not file:
            return Response({'error': 'No file provided.'}, status=status.HTTP_400_BAD_REQUEST)
        
        if not file.name.endswith('.csv'):
            return Response({'error': 'File must be CSV format.'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            decoded_file = file.read().decode('utf-8')
            io_string = io.StringIO(decoded_file)
            reader = csv.DictReader(io_string)
            
            created_count = 0
            errors = []
            
            for row_num, row in enumerate(reader, start=2):
                try:

                    first_name = row.get('first_name', '').strip()
                    last_name = row.get('last_name', '').strip()
                    email = row.get('email', '').strip()
                    
                    if not all([first_name, last_name, email]):
                        errors.append(f"Row {row_num}: Missing required fields")
                        continue

                    if Contact.objects.filter(user=request.user, email=email).exists():
                        errors.append(f"Row {row_num}: Duplicate email {email}")
                        continue

                    contact = Contact.objects.create(
                        user=request.user,
                        first_name=first_name,
                        last_name=last_name,
                        email=email,
                        phone=row.get('phone', '').strip(),
                        company_name_manual=row.get('company_name_manual', '').strip()
                    )
                    ensure_company_for_contact(contact)
                    created_count += 1
                    
                except Exception as e:
                    errors.append(f"Row {row_num}: {str(e)}")
            
            log_activity(
                user=request.user,
                action='create',
                entity_type='contact',
                entity_id=0,
                entity_name='CSV Import',
                details=f"Imported {created_count} contacts"
            )
            
            return Response({
                'message': f'Successfully imported {created_count} contacts.',
                'created': created_count,
                'errors': errors
            }, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class CompanyViewSet(viewsets.ModelViewSet):
    """
    Company viewset with user isolation.
    LUXURY EDITION: Requires at least one contact to create a company. Unlimited companies.
    """
    serializer_class = CompanySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        profile = getattr(user, 'profile', None)
        if not profile:
            return Company.objects.filter(user=user)

        if profile.organization:
            return Company.objects.filter(organization=profile.organization)

        if profile.company_name:
            company = normalize_company_name(profile.company_name)
            return Company.objects.filter(
                Q(organization__name__iexact=company) |
                Q(user__profile__company_name__iexact=company)
            )

        if is_owner_admin_user(user):
            return Company.objects.filter(
                Q(organization__slug='mtambo-holdings') |
                Q(user__username=OWNER_ADMIN_USERNAME) |
                Q(user=user)
            )

        return Company.objects.filter(user=user)

    def perform_create(self, serializer):

        user = self.request.user
        if not (user.is_superuser or user.is_staff or (getattr(user, 'profile', None) and user.profile.is_admin)):
            raise PermissionDenied('Only administrators can create companies.')

        if not visible_contacts_queryset(user).exists():
            raise ValidationError({
                'error': 'You need at least one contact before you can register a company.',
                'action': 'Capture a contact with their company name, then create the company profile.'
            })
        profile = getattr(user, 'profile', None)
        org = getattr(profile, 'organization', None) if profile else None

        if org:
            current_count = Company.objects.filter(organization=org).count()
            allowed, limit, msg = check_org_quota(org, 'companies', current_count)
            if not allowed:
                raise ValidationError({'detail': msg})

        company = serializer.save(user=user, organization=org)
        log_activity(
            user=self.request.user,
            action='create',
            entity_type='company',
            entity_id=company.id,
            entity_name=company.name
        )

    def perform_update(self, serializer):

        user = self.request.user
        if not (user.is_superuser or user.is_staff or (getattr(user, 'profile', None) and user.profile.is_admin)):
            raise PermissionDenied('Only administrators can update companies.')
        company = serializer.save()
        log_activity(
            user=self.request.user,
            action='update',
            entity_type='company',
            entity_id=company.id,
            entity_name=company.name
        )

    def perform_destroy(self, instance):

        user = self.request.user
        if not (user.is_superuser or user.is_staff or (getattr(user, 'profile', None) and user.profile.is_admin)):
            raise PermissionDenied('Only administrators can delete companies.')
        company_name = instance.name
        company_id = instance.id
        instance.delete()
        log_activity(
            user=self.request.user,
            action='delete',
            entity_type='company',
            entity_id=company_id,
            entity_name=company_name
        )


class DealViewSet(viewsets.ModelViewSet):
    """
    Deal viewset with strict Organization multi-tenant isolation.
    """
    serializer_class = DealSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        profile = getattr(user, 'profile', None)
        if not profile:
            return Deal.objects.filter(user=user)

        if profile.organization:
            return Deal.objects.filter(organization=profile.organization)

        if profile.company_name:
            company = normalize_company_name(profile.company_name)
            return Deal.objects.filter(
                Q(organization__name__iexact=company) |
                Q(user__profile__company_name__iexact=company)
            )

        if is_owner_admin_user(user):
            return Deal.objects.filter(
                Q(organization__slug='mtambo-holdings') |
                Q(user__username=OWNER_ADMIN_USERNAME) |
                Q(user=user)
            )

        return Deal.objects.filter(user=user)

    def perform_create(self, serializer):

        user = self.request.user
        if not (user.is_superuser or user.is_staff or (getattr(user, 'profile', None) and user.profile.is_admin)):
            raise PermissionDenied('Only administrators can create deals.')
        profile = getattr(user, 'profile', None)
        org = getattr(profile, 'organization', None) if profile else None

        if org:
            current_count = Deal.objects.filter(organization=org).count()
            allowed, limit, msg = check_org_quota(org, 'deals', current_count)
            if not allowed:
                raise ValidationError({'detail': msg})

        deal = serializer.save(user=user, organization=org)
        log_activity(
            user=self.request.user,
            action='create',
            entity_type='deal',
            entity_id=deal.id,
            entity_name=deal.title,
            details=f"Value: R{deal.value}, Stage: {deal.stage}"
        )

    def perform_update(self, serializer):

        user = self.request.user
        if not (user.is_superuser or user.is_staff or (getattr(user, 'profile', None) and user.profile.is_admin)):
            raise PermissionDenied('Only administrators can update deals.')
        deal = serializer.save()
        log_activity(
            user=self.request.user,
            action='update',
            entity_type='deal',
            entity_id=deal.id,
            entity_name=deal.title,
            details=f"Stage: {deal.stage}"
        )

    def perform_destroy(self, instance):

        user = self.request.user
        if not (user.is_superuser or user.is_staff or (getattr(user, 'profile', None) and user.profile.is_admin)):
            raise PermissionDenied('Only administrators can delete deals.')
        deal_name = instance.title
        deal_id = instance.id
        instance.delete()
        log_activity(
            user=self.request.user,
            action='delete',
            entity_type='deal',
            entity_id=deal_id,
            entity_name=deal_name
        )
    
    @action(detail=True, methods=['post'])
    def start_timer(self, request, pk=None):
        """Start time tracking for this deal"""
        try:
            deal = self.get_object()
            if deal.timer_running:
                return Response(
                    {'error': 'Timer already running'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            deal.start_timer()
            return Response({
                'message': 'Timer started',
                'timer_running': True,
                'timer_started_at': deal.timer_started_at
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                'error': 'Failed to start timer',
                'detail': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @action(detail=True, methods=['post'])
    def stop_timer(self, request, pk=None):
        """Stop time tracking for this deal"""
        try:
            deal = self.get_object()
            if not deal.timer_running:
                return Response(
                    {'error': 'Timer not running'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            deal.stop_timer()
            return Response({
                'message': 'Timer stopped',
                'timer_running': False,
                'time_spent_hours': float(deal.time_spent_hours),
                'total_hours_display': deal.total_hours_display
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                'error': 'Failed to stop timer',
                'detail': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ActivityLogViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Activity log viewset.
    LUXURY edition: Returns all activities.
    """
    serializer_class = ActivityLogSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        profile = getattr(user, 'profile', None)

        if profile and profile.organization:
            return ActivityLog.objects.filter(
                Q(user__profile__organization=profile.organization) | Q(user=user)
            )

        if profile and profile.company_name:
            company = normalize_company_name(profile.company_name)
            return ActivityLog.objects.filter(
                user__profile__company_name__iexact=company
            )

        if is_owner_admin_user(user):
            return ActivityLog.objects.filter(
                Q(user__profile__organization__slug='mtambo-holdings') |
                Q(user__username=OWNER_ADMIN_USERNAME) |
                Q(user=user)
            )

        return ActivityLog.objects.filter(user=user)


class WebsiteLeadViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = WebsiteLeadSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        if not (user.is_superuser or is_owner_admin_user(user)):
            raise PermissionDenied('Only the owner admin can access website lead inbox.')

        if user.is_superuser:
            return WebsiteLead.objects.select_related('contact', 'owner', 'handled_by').all()

        return WebsiteLead.objects.select_related('contact', 'owner', 'handled_by').filter(
            owner=user
        )

    @action(detail=True, methods=['post'])
    def update_workflow(self, request, pk=None):
        lead = self.get_object()
        serializer = WebsiteLeadUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        update_fields = []

        if 'response_status' in data:
            lead.response_status = data['response_status']
            update_fields.append('response_status')
            if data['response_status'] == 'responded':
                lead.responded_at = timezone.now()
                update_fields.append('responded_at')

        if 'response_notes' in data:
            lead.response_notes = data['response_notes']
            update_fields.append('response_notes')

        if 'call_notes' in data:
            lead.call_notes = data['call_notes']
            lead.called_at = timezone.now()
            update_fields.extend(['call_notes', 'called_at'])

        if 'meeting_status' in data:
            lead.meeting_status = data['meeting_status']
            update_fields.append('meeting_status')

        if 'meeting_datetime' in data:
            lead.meeting_datetime = data['meeting_datetime']
            update_fields.append('meeting_datetime')

        if 'meeting_notes' in data:
            lead.meeting_notes = data['meeting_notes']
            update_fields.append('meeting_notes')

        lead.handled_by = request.user
        update_fields.append('handled_by')

        if update_fields:
            lead.save(update_fields=list(dict.fromkeys(update_fields)))
            
        entity_name = f"{lead.contact.first_name} {lead.contact.last_name}" if lead.contact else f"{lead.first_name} {lead.last_name}"

        ActivityLog.objects.create(
            user=request.user,
            action='update',
            entity_type='website_lead',
            entity_id=lead.id,
            entity_name=entity_name,
            details=(
                f"Website lead workflow updated | response_status={lead.response_status} | "
                f"meeting_status={lead.meeting_status}"
            )
        )

        return Response(WebsiteLeadSerializer(lead).data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def reply(self, request, pk=None):
        lead = self.get_object()
        serializer = WebsiteLeadReplySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        payload = serializer.validated_data

        subject = payload['subject'].strip()
        message = payload['message'].strip()
        response_notes = payload.get('response_notes', '').strip()
        target_email = lead.contact.email if lead.contact else lead.email

        if not subject or not message:
            return Response({'error': 'Subject and message are required.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            from .email_service import send_email_async, render_luxury_email_html
            recipient_label = lead.contact.first_name if lead.contact else lead.first_name
            lead_html = render_luxury_email_html(
                title="Executive Concierge Dispatch",
                subtitle="Mtambo Holdings &middot; Official Correspondence",
                recipient_name=recipient_label or "Valued Client",
                message_paragraphs=[p.strip() for p in message.split('\n\n') if p.strip()] or [message],
                security_note="Official correspondence from Mtambo Holdings (Pty) Ltd. Cryptographically verified under POPIA Section 19 standards."
            )
            send_email_async(
                subject=subject,
                text_body=message,
                recipient_list=[target_email],
                from_email=settings.DEFAULT_FROM_EMAIL,
                html_body=lead_html,
            )
        except Exception as exc:
            return Response(
                {'error': f'Failed to send reply email: {str(exc)}'},
                status=status.HTTP_502_BAD_GATEWAY,
            )

        lead.response_status = 'responded'
        lead.responded_at = timezone.now()
        lead.response_notes = response_notes or lead.response_notes
        lead.handled_by = request.user
        lead.save(update_fields=['response_status', 'responded_at', 'response_notes', 'handled_by'])
        
        entity_name = f"{lead.contact.first_name} {lead.contact.last_name}" if lead.contact else f"{lead.first_name} {lead.last_name}"

        log_activity(
            user=request.user,
            action='update',
            entity_type='website_lead',
            entity_id=lead.id,
            entity_name=entity_name,
            details=f"Website lead reply sent to {target_email} | subject={subject}",
        )

        return Response(
            {
                'success': True,
                'message': 'Reply sent successfully.',
                'lead': WebsiteLeadSerializer(lead).data,
            },
            status=status.HTTP_200_OK,
        )

    @action(detail=True, methods=['post'])
    def promote_to_deal(self, request, pk=None):
        lead = self.get_object()
        
        if lead.response_status == 'promoted':
            return Response({'error': 'This lead has already been promoted to a deal.'}, status=status.HTTP_400_BAD_REQUEST)
            
        contact = lead.contact
        ensure_company_for_contact(contact)
        
        deal_value = request.data.get('value', 0.00)
        deal_title = request.data.get('title', f"Lead Deal: {contact.first_name} {contact.last_name}")
        
        with transaction.atomic():
            contact = lead.contact
            if not contact:
                contact = Contact.objects.filter(email__iexact=lead.email, user=lead.owner).first()
                if not contact:
                    contact = Contact.objects.create(
                        user=lead.owner,
                        first_name=lead.first_name,
                        last_name=lead.last_name,
                        email=lead.email,
                        phone=lead.phone,
                        company_name_manual=f"{lead.first_name} {lead.last_name} Business"
                    )
                lead.contact = contact
            
            ensure_company_for_contact(contact)
            
            deal_value = request.data.get('value', 0.00)
            deal_title = request.data.get('title', f"Lead Deal: {contact.first_name} {contact.last_name}")
            
            deal = Deal.objects.create(
                user=lead.owner,
                title=deal_title,
                contact=contact,
                company=contact.company,
                value=deal_value,
                stage='lead'
            )
            
            lead.response_status = 'promoted'
            lead.handled_by = request.user
            lead.save(update_fields=['contact', 'response_status', 'handled_by'])
            
            log_activity(
                user=request.user,
                action='create',
                entity_type='deal',
                entity_id=deal.id,
                entity_name=deal.title,
                details=f"Promoted from Website Lead ({contact.email})"
            )
            
        return Response({
            'success': True,
            'message': 'Lead successfully promoted to Deal!',
            'deal': DealSerializer(deal).data,
            'lead': WebsiteLeadSerializer(lead).data
        }, status=status.HTTP_200_OK)


class TicketViewSet(viewsets.ModelViewSet):
    serializer_class = TicketSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        profile = getattr(user, 'profile', None)
        if not profile:
            return Ticket.objects.filter(Q(created_by=user) | Q(assigned_to=user))

        if profile.organization:
            if profile.role in ['admin', 'executive', 'manager']:
                return Ticket.objects.filter(organization=profile.organization)
            return Ticket.objects.filter(
                organization=profile.organization
            ).filter(Q(created_by=user) | Q(assigned_to=user)).distinct()

        company_name = profile.company_name
        if company_name:
            if profile.role in ['admin', 'executive', 'manager'] or profile.is_admin:
                return Ticket.objects.filter(
                    Q(created_by__profile__company_name=company_name) |
                    Q(assigned_to__profile__company_name=company_name)
                ).distinct()
            return Ticket.objects.filter(
                Q(created_by=user) | Q(assigned_to=user)
            ).distinct()

        if is_owner_admin_user(user):
            return Ticket.objects.filter(
                Q(organization__slug='mtambo-holdings') |
                Q(created_by=user) | Q(assigned_to=user)
            ).distinct()

        return Ticket.objects.filter(Q(assigned_to=user) | Q(created_by=user)).distinct()

    def perform_create(self, serializer):
        user = self.request.user
        profile = getattr(user, 'profile', None)
        org = getattr(profile, 'organization', None) if profile else None

        if not (user.is_superuser or user.is_staff or (profile and profile.is_admin)):
            assigned_to = serializer.validated_data.get('assigned_to')
            assigned_profile = getattr(assigned_to, 'profile', None)
            if not assigned_profile or assigned_profile.role not in ['admin', 'executive', 'manager']:
                raise PermissionDenied('You can only escalate tickets to your company leadership.')

            if org and getattr(assigned_profile, 'organization', None) != org:
                raise PermissionDenied('You can only assign within your organization.')
        if org:
            current_count = Ticket.objects.filter(organization=org).count()
            allowed, limit, msg = check_org_quota(org, 'tickets', current_count)
            if not allowed:
                raise ValidationError({'detail': msg})

        # Compute sale value if product attached
        product = serializer.validated_data.get('product')
        quantity = serializer.validated_data.get('quantity', 1) or 1
        unit_price = serializer.validated_data.get('unit_price')
        if product and (unit_price is None or unit_price == 0):
            unit_price = product.unit_price
            serializer.validated_data['unit_price'] = unit_price
        
        if product:
            serializer.validated_data['sale_value'] = (unit_price or 0) * quantity

        ticket = serializer.save(created_by=user, organization=org)

        # Automated Pipeline Integration: If sale initiated and contact provided, bridge into Deal pipeline
        if ticket.is_sale_initiated and ticket.contact and not ticket.deal:
            deal_title = f"{ticket.product.name if ticket.product else 'Sale'} — {ticket.contact.first_name} {ticket.contact.last_name}"
            deal = Deal.objects.create(
                organization=org,
                user=user,
                title=deal_title,
                contact=ticket.contact,
                company=ticket.company or getattr(ticket.contact, 'company', None),
                value=ticket.sale_value or 0,
                stage='proposal'
            )
            ticket.deal = deal
            ticket.save(update_fields=['deal'])

        Notification.objects.create(
            recipient=ticket.assigned_to,
            title='New Ticket Assigned',
            message=f"{user.username} assigned you a ticket: {ticket.title}",
            entity_type='ticket',
            entity_id=ticket.id,
            meta={'status': ticket.status}
        )

    def perform_update(self, serializer):
        user = self.request.user
        if not (user.is_superuser or user.is_staff or getattr(user, 'profile', None) and user.profile.is_admin):
            raise PermissionDenied('Only administrators can update tickets.')

        product = serializer.validated_data.get('product', serializer.instance.product)
        quantity = serializer.validated_data.get('quantity', serializer.instance.quantity) or 1
        unit_price = serializer.validated_data.get('unit_price', serializer.instance.unit_price)
        if product and (unit_price is None or unit_price == 0):
            unit_price = product.unit_price
            serializer.validated_data['unit_price'] = unit_price
        if product:
            serializer.validated_data['sale_value'] = (unit_price or 0) * quantity

        ticket = serializer.save()

        if ticket.is_sale_initiated and ticket.contact and not ticket.deal:
            deal_title = f"{ticket.product.name if ticket.product else 'Sale'} — {ticket.contact.first_name} {ticket.contact.last_name}"
            deal = Deal.objects.create(
                organization=ticket.organization,
                user=user,
                title=deal_title,
                contact=ticket.contact,
                company=ticket.company or getattr(ticket.contact, 'company', None),
                value=ticket.sale_value or 0,
                stage='proposal'
            )
            ticket.deal = deal
            ticket.save(update_fields=['deal'])

    def perform_destroy(self, instance):
        user = self.request.user
        if not (user.is_superuser or user.is_staff or getattr(user, 'profile', None) and user.profile.is_admin):
            raise PermissionDenied('Only administrators can delete tickets.')
        instance.delete()

    @action(detail=True, methods=['post'], url_path='complete_sale')
    def complete_sale(self, request, pk=None):
        """1-Click Complete Sale & Issue License directly from Ticket."""
        ticket = self.get_object()
        ticket.sale_status = 'paid'
        ticket.status = 'completed'
        ticket.completed_at = timezone.now()
        if ticket.deal:
            ticket.deal.stage = 'closed_won'
            ticket.deal.save(update_fields=['stage'])
        ticket.save(update_fields=['sale_status', 'status', 'completed_at'])
        return Response({'message': 'Sale marked as completed and Deal won!', 'status': ticket.sale_status})

    @action(detail=True, methods=['post'])
    def start(self, request, pk=None):
        ticket = self.get_object()
        user = request.user
        if not (user.is_superuser or user.is_staff or getattr(user, 'profile', None) and user.profile.is_admin):
            return Response({'error': 'Only administrators can start tickets.'}, status=403)
        ticket.start()
        return Response({'message': 'Ticket started', 'started_at': ticket.started_at, 'status': ticket.status})

    @action(detail=True, methods=['post'])
    def stop(self, request, pk=None):
        ticket = self.get_object()
        user = request.user
        if not (user.is_superuser or user.is_staff or getattr(user, 'profile', None) and user.profile.is_admin):
            return Response({'error': 'Only administrators can stop tickets.'}, status=403)
        ticket.stop()
        return Response({'message': 'Ticket stopped', 'duration_seconds': ticket.duration_seconds})

    @action(detail=True, methods=['post'])
    def complete(self, request, pk=None):
        ticket = self.get_object()
        user = request.user

        if not (user == ticket.assigned_to or user.is_superuser or user.is_staff or getattr(user, 'profile', None) and user.profile.is_admin):
            return Response({'error': 'You cannot complete this ticket.'}, status=403)
        ticket.mark_completed()

        Notification.objects.create(
            recipient=ticket.created_by,
            title='Ticket Completed',
            message=f"{user.username} completed ticket: {ticket.title}",
            entity_type='ticket',
            entity_id=ticket.id,
            meta={'status': ticket.status}
        )
        return Response({'message': 'Ticket marked as completed', 'completed_at': ticket.completed_at, 'status': ticket.status})


class NotificationViewSet(viewsets.ModelViewSet):
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        scope = (self.request.query_params.get('scope') or 'mine').lower()

        qs = Notification.objects.filter(recipient=user)

        if scope == 'all' and (user.is_superuser or user.is_staff):
            return Notification.objects.all()
        if scope == 'company':
            profile = getattr(user, 'profile', None)
            if profile and profile.is_admin and profile.company_name:
                return Notification.objects.filter(recipient__profile__company_name=profile.company_name)
        return qs

    def perform_create(self, serializer):

        user = self.request.user
        if not (user.is_superuser or user.is_staff or getattr(user, 'profile', None) and user.profile.is_admin):
            raise PermissionDenied('Only administrators can create notifications.')
        serializer.save()

    def perform_update(self, serializer):

        instance = serializer.save()
        if instance.recipient != self.request.user and not (self.request.user.is_superuser or self.request.user.is_staff or getattr(self.request.user, 'profile', None) and self.request.user.profile.is_admin):
            raise PermissionDenied('You cannot modify this notification.')

    def perform_destroy(self, instance):

        user = self.request.user
        if instance.recipient != user and not (user.is_superuser or user.is_staff or getattr(user, 'profile', None) and user.profile.is_admin):
            raise PermissionDenied('You cannot delete this notification.')
        instance.delete()

    @action(detail=True, methods=['post'])
    def mark_read(self, request, pk=None):
        notif = self.get_object()
        if notif.recipient != request.user and not (request.user.is_superuser or request.user.is_staff or getattr(request.user, 'profile', None) and request.user.profile.is_admin):
            return Response({'error': 'Not allowed'}, status=403)
        notif.mark_read()
        return Response({'message': 'Notification marked as read', 'read_at': notif.read_at})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def prerequisite_status(request):
    """Return counts that drive navigation prerequisites."""
    contacts_count = Contact.objects.filter(user=request.user).count()
    companies_count = Company.objects.filter(user=request.user).count()
    deals_count = Deal.objects.filter(user=request.user).count()
    orphan_contacts = Contact.objects.filter(user=request.user, company__isnull=True).count()

    return Response({
        'contacts': contacts_count,
        'companies': companies_count,
        'deals': deals_count,
        'contacts_missing_company': orphan_contacts
    })


def _compute_ticket_elapsed_seconds(ticket):
    total = int(getattr(ticket, 'duration_seconds', 0) or 0)
    if getattr(ticket, 'started_at', None):

        total += int((timezone.now() - ticket.started_at).total_seconds())
    return max(total, 0)


def _build_performance_response(target_user: User, days: int = 14):

    assigned_qs = Ticket.objects.filter(assigned_to=target_user)
    status_counts = assigned_qs.values('status').annotate(count=Count('id'))
    counts = {s['status']: s['count'] for s in status_counts}
    total_assigned = assigned_qs.count()
    completed = counts.get('completed', 0)
    in_progress = counts.get('in_progress', 0)
    open_count = counts.get('open', 0)
    failed = counts.get('failed', 0)

    total_seconds = 0
    for t in assigned_qs.only('duration_seconds', 'started_at'):
        total_seconds += _compute_ticket_elapsed_seconds(t)

    current_ticket = assigned_qs.filter(status='in_progress').order_by('-started_at').first()

    end_date = timezone.localdate()
    start_date = end_date - timezone.timedelta(days=days - 1)
    day_buckets = { (start_date + timezone.timedelta(days=i)).isoformat(): 0.0 for i in range(days) }

    completed_qs = assigned_qs.filter(completed_at__date__gte=start_date, completed_at__date__lte=end_date)
    for t in completed_qs.only('completed_at', 'duration_seconds'):
        day_key = t.completed_at.date().isoformat()
        secs = int(getattr(t, 'duration_seconds', 0) or 0)
        day_buckets[day_key] = day_buckets.get(day_key, 0.0) + round(secs / 3600.0, 2)

    today_key = end_date.isoformat()
    for t in assigned_qs.filter(status='in_progress').only('started_at', 'duration_seconds'):
        day_buckets[today_key] = day_buckets.get(today_key, 0.0) + round(_compute_ticket_elapsed_seconds(t) / 3600.0, 2)

    days_busy = sum(1 for h in day_buckets.values() if h > 0)

    data = {
        'user': {
            'id': target_user.id,
            'username': target_user.username,
            'first_name': target_user.first_name,
            'last_name': target_user.last_name,
        },
        'counts': {
            'assigned': total_assigned,
            'completed': completed,
            'in_progress': in_progress,
            'open': open_count,
            'failed': failed,
        },
        'time': {
            'total_seconds': total_seconds,
            'total_hours': round(total_seconds / 3600.0, 2),
            'days_busy': days_busy,
        },
        'current_ticket': (
            {
                'id': current_ticket.id,
                'title': current_ticket.title,
                'priority': current_ticket.priority,
                'category': current_ticket.category,
                'department': current_ticket.department,
                'started_at': current_ticket.started_at,
                'elapsed_seconds': _compute_ticket_elapsed_seconds(current_ticket),
            } if current_ticket else None
        ),
        'daily_hours': {
            'labels': list(day_buckets.keys()),
            'values': list(day_buckets.values())
        }
    }
    return data


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def performance_me(request):
    return Response(_build_performance_response(request.user))


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def performance_user(request, user_id: int):
    requester = request.user

    try:
        target = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=404)

    if requester.is_superuser or requester.is_staff:
        return Response(_build_performance_response(target))

    req_profile = getattr(requester, 'profile', None)
    tgt_profile = getattr(target, 'profile', None)
    if req_profile and req_profile.is_admin and req_profile.company_name and tgt_profile and tgt_profile.company_name == req_profile.company_name:
        return Response(_build_performance_response(target))

    return Response({'error': 'Not authorized to view this performance'}, status=403)


class AdminOverviewView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if not has_user_management_access(request):
            raise PermissionDenied('Admin access required.')

        company_payload = []
        # Ghost account exclusion: adminluxury and superusers never appear in client data
        admin_users = User.objects.filter(companies__isnull=False).exclude(
            username__iexact='adminluxury'
        ).exclude(
            is_superuser=True
        ).distinct()
        for user in admin_users:
            companies = []
            for company in user.companies.all().order_by('name'):
                contacts_qs = visible_contacts_queryset(user).filter(company=company).order_by('first_name', 'last_name')
                deals_qs = company.deals.filter(user=user)
                companies.append({
                    'id': company.id,
                    'name': company.name,
                    'contact_count': contacts_qs.count(),
                    'contacts': [
                        {
                            'id': contact.id,
                            'name': f"{contact.first_name} {contact.last_name}",
                            'email': contact.email,
                            'phone': contact.phone,
                            'company_hint': contact.company_name_manual,
                        }
                        for contact in contacts_qs
                    ],
                    'deal_count': deals_qs.count(),
                    'pipeline_value': str(deals_qs.aggregate(total=Sum('value'))['total'] or 0),
                })

            company_payload.append({
                'user_id': user.id,
                'username': user.username,
                'email': user.email,
                'companies': companies,
                'total_contacts': visible_contacts_queryset(user).count(),
                'total_deals': Deal.objects.filter(user=user).count(),
            })

        analytics = Deal.objects.aggregate(
            total_deals=Count('id'),
            active_deals=Count('id', filter=Q(stage__in=['lead', 'qualified', 'proposal', 'negotiation'])),
            closed_won=Count('id', filter=Q(stage='closed_won')),
            pipeline_value=Sum('value', filter=Q(stage__in=['lead', 'qualified', 'proposal', 'negotiation'])),
            won_value=Sum('value', filter=Q(stage='closed_won')),
        )

        if request.user.is_superuser or request.user.is_staff or is_owner_admin_user(request.user):
            lead_scope = WebsiteLead.objects.all()
        else:
            lead_scope = WebsiteLead.objects.filter(owner=request.user)
            if not lead_scope.exists():
                profile = getattr(request.user, 'profile', None)
                if profile and profile.company_name:
                    company = normalize_company_name(profile.company_name)
                    lead_scope = WebsiteLead.objects.filter(owner__profile__company_name__iexact=company)

        support_catalog = [
            {
                'name': 'Velocity Titans',
                'industry': 'Sports Retail',
                'focus': 'Omni-channel sales enablement',
                'next_step': 'Build assisted upsell journeys for Q1 campaigns.'
            },
            {
                'name': 'Apex Solar United',
                'industry': 'Renewable Energy',
                'focus': 'Dealer onboarding and SLA monitoring',
                'next_step': 'Design automated partner scorecards for service delivery.'
            },
            {
                'name': 'Pulse Logistics FC',
                'industry': 'Logistics & Courier',
                'focus': 'Client retention and support desk insights',
                'next_step': 'Deploy proactive support workflows and playbooks.'
            }
        ]

        return Response({
            'clients': company_payload,
            'analytics': {
                'total_deals': analytics['total_deals'] or 0,
                'active_deals': analytics['active_deals'] or 0,
                'closed_won': analytics['closed_won'] or 0,
                'pipeline_value': str(analytics['pipeline_value'] or 0),
                'won_value': str(analytics['won_value'] or 0),
                'website_leads_total': lead_scope.count(),
                'website_leads_new': lead_scope.filter(response_status='new').count(),
                'website_leads_responded': lead_scope.filter(response_status='responded').count(),
            },
            'support_catalog': support_catalog
        })


class AdminWebsiteLeadInboxView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if not (request.user.is_superuser or is_owner_admin_user(request.user)):
            raise PermissionDenied('Only the owner admin can access website lead inbox.')

        if request.user.is_superuser or is_owner_admin_user(request.user):
            base_qs = WebsiteLead.objects.select_related('contact', 'owner', 'handled_by').all()
        else:
            base_qs = WebsiteLead.objects.select_related('contact', 'owner', 'handled_by').filter(owner=request.user)

        response_status = request.query_params.get('status', '').strip().lower()
        if response_status in {'new', 'responded', 'promoted', 'closed'}:
            results_qs = base_qs.filter(response_status=response_status)
        else:
            results_qs = base_qs

        meeting_status = request.query_params.get('meeting_status', '').strip().lower()
        if meeting_status in {'none', 'proposed', 'accepted', 'declined', 'completed'}:
            results_qs = results_qs.filter(meeting_status=meeting_status)

        try:
            limit = int(request.query_params.get('limit', 50))
        except (TypeError, ValueError):
            limit = 50
        limit = max(1, min(200, limit))

        results = results_qs.order_by('-inbound_received_at')[:limit]

        return Response({
            'summary': {
                'total': base_qs.count(),
                'new': base_qs.filter(response_status='new').count(),
                'responded': base_qs.filter(response_status='responded').count(),
                'promoted': base_qs.filter(response_status='promoted').count(),
                'closed': base_qs.filter(response_status='closed').count(),
                'meeting_proposed': base_qs.filter(meeting_status='proposed').count(),
                'meeting_accepted': base_qs.filter(meeting_status='accepted').count(),
                'meeting_declined': base_qs.filter(meeting_status='declined').count(),
            },
            'results': WebsiteLeadSerializer(results, many=True).data,
        })


class UserManagementView(APIView):
    """
    Admin endpoint to view, manage, and ban users
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """Get all users with detailed info including IP addresses and payment status"""
        if not has_user_management_access(request):
            raise PermissionDenied('Admin access required.')
        
        # ─── GHOST ACCOUNT ISOLATION ───
        # adminluxury and superusers are INVISIBLE in the user management console.
        # They exist only at the database level — like a ghost.
        users = User.objects.all().select_related('profile').exclude(
            username__iexact='adminluxury'
        ).exclude(
            is_superuser=True
        ).order_by('-date_joined')
        
        user_list = []
        for user in users:
            profile = user.profile if hasattr(user, 'profile') else None

            contact_count = visible_contacts_queryset(user).count()
            company_count = Company.objects.filter(user=user).count()
            deal_count = Deal.objects.filter(user=user).count()
            
            user_data = {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'full_name': f"{user.first_name} {user.last_name}".strip() or user.username,
                'date_joined': user.date_joined,
                'last_login': user.last_login,
                'is_active': user.is_active,
                'is_staff': user.is_staff,
                'is_superuser': user.is_superuser,

                'tier': profile.tier if profile else 'luxury',
                'role': profile.role if profile else 'user',
                'company_name': profile.company_name if profile else '',
                'phone': profile.phone if profile else '',

                'registration_ip': profile.registration_ip if profile else None,
                'last_login_ip': profile.last_login_ip if profile else None,

                'is_banned': profile.is_banned if profile else False,
                'ban_reason': profile.ban_reason if profile else '',
                'banned_at': profile.banned_at if profile else None,

                'payment_status': profile.payment_status if profile else 'pending',
                'trial_ends_at': profile.trial_ends_at if profile else None,
                'days_until_trial_end': profile.days_until_trial_end if profile else 0,

                'contact_count': contact_count,
                'company_count': company_count,
                'deal_count': deal_count,
                'total_activity': contact_count + company_count + deal_count,
            }

            if profile and profile.registration_ip:
                deleted_with_same_ip = DeletedUserLog.objects.filter(
                    registration_ip=profile.registration_ip
                ).exclude(email=user.email)
                
                if deleted_with_same_ip.exists():
                    user_data['warning'] = {
                        'type': 'duplicate_ip',
                        'message': f'⚠️ IP {profile.registration_ip} was used by deleted user(s)',
                        'deleted_users': list(deleted_with_same_ip.values('username', 'email', 'deleted_at', 'deleted_reason')[:3])
                    }

            if user.email:
                previously_deleted = DeletedUserLog.objects.filter(email=user.email).first()
                if previously_deleted:
                    user_data['warning'] = {
                        'type': 're_registration',
                        'message': f'🔄 User re-registered! Previously deleted on {previously_deleted.deleted_at.strftime("%Y-%m-%d")}',
                        'previous_username': previously_deleted.username,
                        'deleted_reason': previously_deleted.deleted_reason,
                        'previous_activity': {
                            'contacts': previously_deleted.contact_count,
                            'companies': previously_deleted.company_count,
                            'deals': previously_deleted.deal_count
                        }
                    }
            
            user_list.append(user_data)

        total_users = len(user_list)
        active_users = sum(1 for u in user_list if u['is_active'] and not u['is_banned'])
        banned_users = sum(1 for u in user_list if u['is_banned'])
        trial_users = sum(1 for u in user_list if u['payment_status'] == 'trial')
        paid_users = sum(1 for u in user_list if u['payment_status'] == 'paid')
        overdue_users = sum(1 for u in user_list if u['payment_status'] == 'overdue')
        
        return Response({
            'users': user_list,
            'summary': {
                'total_users': total_users,
                'active_users': active_users,
                'banned_users': banned_users,
                'trial_users': trial_users,
                'paid_users': paid_users,
                'overdue_users': overdue_users,
            }
        })
    
    def post(self, request):
        """Ban or unban a user"""
        if not has_user_management_access(request):
            raise PermissionDenied('Admin access required.')
        
        action = request.data.get('action')  # 'ban' or 'unban'
        user_id = request.data.get('user_id')
        reason = request.data.get('reason', 'Admin action')
        
        if not action or not user_id:
            return Response({'error': 'action and user_id required'}, status=400)
        
        try:
            user = User.objects.get(id=user_id)
            
            if not hasattr(user, 'profile'):
                return Response({'error': 'User profile not found'}, status=404)
            
            if action == 'ban':
                user.profile.ban_user(reason=reason)
                return Response({
                    'success': True,
                    'message': f'User {user.username} has been banned',
                    'user': {
                        'id': user.id,
                        'username': user.username,
                        'is_banned': True,
                        'ban_reason': reason
                    }
                })
            
            elif action == 'unban':
                user.profile.unban_user()
                return Response({
                    'success': True,
                    'message': f'User {user.username} has been unbanned',
                    'user': {
                        'id': user.id,
                        'username': user.username,
                        'is_banned': False
                    }
                })
            
            elif action == 'update_payment':
                payment_status = request.data.get('payment_status')
                if payment_status in ['pending', 'paid', 'overdue', 'trial']:
                    user.profile.payment_status = payment_status
                    user.profile.save()
                    return Response({
                        'success': True,
                        'message': f'Payment status updated to {payment_status}',
                        'user': {
                            'id': user.id,
                            'username': user.username,
                            'payment_status': payment_status
                        }
                    })
                else:
                    return Response({'error': 'Invalid payment_status'}, status=400)
            
            elif action == 'delete':

                profile = user.profile

                contact_count = visible_contacts_queryset(user).count()
                company_count = Company.objects.filter(user=user).count()
                deal_count = Deal.objects.filter(user=user).count()

                DeletedUserLog.objects.create(
                    username=user.username,
                    email=user.email,
                    registration_ip=profile.registration_ip if profile else None,
                    last_login_ip=profile.last_login_ip if profile else None,
                    company_name=profile.company_name if profile else '',
                    deleted_reason=request.data.get('delete_reason', 'Admin deletion'),
                    contact_count=contact_count,
                    company_count=company_count,
                    deal_count=deal_count
                )

                username = user.username
                user.delete()
                
                return Response({
                    'success': True,
                    'message': f'User {username} has been deleted and logged',
                    'logged_data': {
                        'username': username,
                        'ip_addresses_logged': True,
                        'activity_logged': True
                    }
                })
            
            else:
                return Response({'error': 'Invalid action'}, status=400)
        
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=404)


class EmployeeViewSet(viewsets.ModelViewSet):
    """
    Employee Management ViewSet
    - System admins (programmers) can view/edit/delete all client employees
    - Client company users are view-only in this endpoint
    """
    serializer_class = EmployeeSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        profile = getattr(user, 'profile', None)

        if user.is_superuser or user.is_staff:
            return UserProfile.objects.filter(
                user__is_superuser=False,
                user__is_staff=False
            ).select_related('user')

        if not profile:
            return UserProfile.objects.none()


        client_company_name = normalize_company_name(profile.company_name)
        if client_company_name:

            return UserProfile.objects.filter(
                Q(company_name__iexact=client_company_name) | Q(onboarded_by=user) | Q(reports_to=user),
                user__is_superuser=False,
                user__is_staff=False
            ).select_related('user')


        return UserProfile.objects.filter(user=user)
    
    def create(self, request, *args, **kwargs):
        """
        ADMP Onboarding — hierarchical employee creation.
        - CEO/Admin can onboard: executive, manager, supervisor, user
        - Executive can onboard: manager, supervisor, user
        - All others: cannot onboard
        """
        user = request.user
        profile = getattr(user, 'profile', None)
        if not profile:
            return Response({'error': 'User profile not found'}, status=400)

        is_system_admin = user.is_superuser or user.is_staff

        ONBOARDING_HIERARCHY = {
            'admin': ['executive', 'manager', 'supervisor', 'user'],
            'executive': ['manager', 'supervisor', 'user'],
            'manager': ['supervisor', 'user'],
        }

        if is_system_admin:

            company_name = normalize_company_name(request.data.get('company_name', ''))
            if not company_name:
                return Response({'error': 'Company name is required when onboarding as admin'}, status=400)
        else:

            company_name = normalize_company_name(profile.company_name)

        # Determine organization tier limits (Luxury Basic=3, Luxury Team=5, Executive=15, Enterprise=999, Trial=999)
        user_tier = getattr(profile, 'tier', 'luxury')
        org = getattr(profile, 'organization', None)
        if org:
            user_tier = getattr(org, 'subscription_tier', 'luxury')
        
        is_trial = (user_tier == 'trial') or (org and getattr(org, 'is_trial_active', False))

        TIER_SEAT_LIMITS = {
            'basic': 3,
            'classic': 3,
            'luxury': 5,
            'trial': 999,
            'executive': 15,
            'enterprise': 999,
        }
        max_users = 999 if is_trial else TIER_SEAT_LIMITS.get((user_tier or 'luxury').lower(), 5)

        # Basic Tier Rule: Only CEO (admin) can onboard employees
        if not is_system_admin and not is_trial and (user_tier == 'basic' or user_tier == 'classic'):
            if profile.role != 'admin':
                return Response({
                    'error': 'On Luxury Basic, only the CEO/Administrator may onboard team members. Upgrade to Luxury Team (R999/mo) to delegate onboarding permissions to Managers.',
                    'upgrade_required': True
                }, status=403)

        # Luxury Team Tier Rule: Manager can onboard up to 2 subordinates
        if not is_system_admin and not is_trial and user_tier == 'luxury' and profile.role == 'manager':
            manager_subordinates_count = UserProfile.objects.filter(
                Q(onboarded_by=user) | Q(reports_to=user),
                company_name__iexact=company_name
            ).count()
            if manager_subordinates_count >= 2:
                return Response({
                    'error': 'Managers on Luxury Team can onboard up to 2 subordinates under their supervision. Additional seats must be onboarded by the CEO or upgrade to Executive Suite.',
                    'upgrade_required': True
                }, status=403)

        client_user_count = User.objects.filter(
            is_superuser=False,
            is_staff=False,
            profile__company_name__iexact=company_name
        ).count()
        
        if not is_system_admin and not is_trial and client_user_count >= max_users:
            tier_display = "Luxury Basic" if user_tier == "basic" else (user_tier or 'Luxury Team').upper()
            return Response({
                'error': f'Seat limit reached ({client_user_count}/{max_users} active). Your {tier_display} plan includes up to {max_users} collaborative seats. Upgrade to Executive Suite (15 seats) or Enterprise for additional capacity.',
                'current_users': client_user_count,
                'max_users': max_users,
                'remaining_slots': 0,
                'upgrade_required': True
            }, status=400)

        import random
        import string

        create_serializer = EmployeeCreateSerializer(data=request.data)
        create_serializer.is_valid(raise_exception=True)
        user_data = create_serializer.validated_data
        assigned_role = user_data.get('role')

        raw_password = user_data.get('password')
        if not raw_password:
            # Generate clean high-entropy executive credential: e.g. Fin-8K2P-9M4X
            p1 = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
            p2 = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
            raw_password = f"Fin-{p1}-{p2}"

        if user.check_password(raw_password):
            return Response({
                'error': 'Security: Employee password cannot be the same as your password. Please use a unique password.'
            }, status=400)

        if not is_system_admin:
            allowed_roles = ONBOARDING_HIERARCHY.get(profile.role, [])
            if not allowed_roles:
                return Response({
                    'error': 'Only CEOs (Administrators), Executives, and Managers can onboard employees. '
                             'Contact your supervisor if you need to add team members.'
                }, status=403)

            if assigned_role not in allowed_roles:
                role_display = dict(UserProfile.ROLE_CHOICES).get(profile.role, profile.role)
                return Response({
                    'error': f'Your role ({role_display}) cannot onboard employees at the "{assigned_role}" level.'
                }, status=403)


        division_obj = user_data.get('division')
        division_id = str(division_obj.id) if division_obj else None
        
        if assigned_role in ['manager', 'supervisor', 'user']:
            if not division_id:
                return Response({
                    'error': f'Division is required for {dict(UserProfile.ROLE_CHOICES).get(assigned_role, assigned_role)} role. Please assign employee to a division.'
                }, status=400)

            try:
                Division.objects.get(id=division_id, company_name__iexact=company_name)
            except Division.DoesNotExist:
                return Response({'error': 'Invalid division or division does not belong to your company'}, status=400)

        reports_to_user = user_data.get('reports_to')
        if reports_to_user:

            reports_to_profile = getattr(reports_to_user, 'profile', None)
            if not reports_to_profile:
                return Response({'error': 'Invalid supervisor selection'}, status=400)
            
            if not is_system_admin:
                supervisor_company = normalize_company_name(reports_to_profile.company_name)
                if supervisor_company != company_name:
                    return Response({'error': 'Supervisor must be from the same company'}, status=403)

                ROLE_RANK = {'admin': 5, 'executive': 4, 'manager': 3, 'supervisor': 2, 'user': 1}
                if ROLE_RANK.get(assigned_role, 0) >= ROLE_RANK.get(reports_to_profile.role, 0):
                    return Response({
                        'error': f'{dict(UserProfile.ROLE_CHOICES).get(assigned_role)} cannot report to {reports_to_profile.get_role_display()}. Choose a higher-level supervisor.'
                    }, status=400)

        email_identity = (user_data['email'] or '').strip().lower()
        try:
            with transaction.atomic():
                new_user = User.objects.create_user(
                    username=email_identity,
                    email=email_identity,
                    first_name=user_data['first_name'],
                    last_name=user_data['last_name'],
                    password=raw_password,
                )

                new_profile = new_user.profile
                new_profile.company_name = company_name
                new_profile.role = assigned_role
                new_profile.phone = user_data.get('phone', '')
                new_profile.job_title = user_data.get('job_title', '')
                new_profile.department = user_data.get('department', '')
                new_profile.employee_id = user_data.get('employee_id', '')
                new_profile.date_of_birth = user_data.get('date_of_birth')
                new_profile.address = user_data.get('address', '')
                new_profile.emergency_contact_name = user_data.get('emergency_contact_name', '')
                new_profile.emergency_contact_phone = user_data.get('emergency_contact_phone', '')
                new_profile.start_date = user_data.get('start_date')
                new_profile.notes = user_data.get('notes', '')
                new_profile.payment_status = 'paid'
                new_profile.requires_password_reset = True
                new_profile.can_manage_assets = bool(user_data.get('can_manage_assets', False)) if assigned_role == 'manager' else False

                if org and not new_profile.organization:
                    new_profile.organization = org

                new_profile.reports_to = reports_to_user if reports_to_user else user  # default: reports to whoever onboarded them
                new_profile.onboarded_by = user
                new_profile.onboarded_at = timezone.now()

                if division_id:
                    new_profile.division_id = division_id

                new_profile.save()

                OnboardingLog.objects.create(
                    employee=new_user,
                    employee_name=f"{new_user.first_name} {new_user.last_name}",
                    employee_email=new_user.email,
                    action='onboard',
                    performed_by=user,
                    performed_by_name=f"{user.first_name} {user.last_name}".strip() or user.username,
                    company_name=company_name,
                    role_assigned=new_profile.role,
                    department=new_profile.department,
                )

                try:
                    from .email_service import send_email_async, render_luxury_email_html
                    sender_email = getattr(settings, 'DEFAULT_FROM_EMAIL', 'The Finisher Luxury Registrations <noreply@mtamboholdings.dev>')
                    ceo_display = user.get_full_name() or user.username
                    role_label = dict(UserProfile.ROLE_CHOICES).get(new_profile.role, new_profile.role)

                    email_subject = f"Welcome to {company_name} — Your Finisher Luxury Credentials"
                    email_text = f"""Dear {new_user.first_name},

You have been provisioned access to the {company_name} Private Operating System on THE FINISHER LUXURY by {ceo_display}.

Your secure temporary credentials are:
--------------------------------------------------
Login Portal: https://www.thefinishercrm.tech/#/login
Work Email / Username: {email_identity}
Temporary Password: {raw_password}
Assigned Role: {role_label}
--------------------------------------------------

ACTIVATION INSTRUCTIONS:
1. Navigate to the secure portal: https://www.thefinishercrm.tech/#/login
2. Sign in using your work email ({email_identity}) and the temporary password above.
3. You will immediately be prompted to create your private, permanent password.
4. Once updated, your enterprise workspace will be unlocked.

SECURITY NOTICE:
This temporary password is cryptographically generated and valid for first-time activation. Never share this credential with anyone.

Sincerely,
The Executive Directorate
THE FINISHER LUXURY | Mtambo Holdings
https://www.thefinishercrm.tech
"""
                    email_html = render_luxury_email_html(
                        title="Corporate Identity Provisioning",
                        subtitle=f"{company_name} &middot; Private Fleet Workspace",
                        recipient_name=f"{new_user.first_name} {new_user.last_name}".strip() or new_user.first_name,
                        message_paragraphs=[
                            f"You have been officially provisioned enterprise access to the private operating system for <strong>{company_name}</strong> on <strong>THE FINISHER LUXURY</strong> by Executive Authority <strong>{ceo_display}</strong>.",
                            "Your dedicated corporate seat has been allocated with high-performance CRM architecture, automated pipeline intelligence, and luxury cryptographic security protocols."
                        ],
                        credentials={
                            "Authorized Portal": "https://www.thefinishercrm.tech/#/login",
                            "Work Identity (Login)": email_identity,
                            "Temporary Passcode": raw_password,
                            "Assigned Enterprise Role": role_label
                        },
                        cta_text="Access Private Workspace",
                        cta_url="https://www.thefinishercrm.tech/#/login",
                        activation_steps=[
                            "Navigate to the secure corporate portal at https://www.thefinishercrm.tech/#/login",
                            f"Sign in using your authorized work email (<strong>{email_identity}</strong>) and temporary passcode.",
                            "Upon initial authentication, you will be prompted to establish your private, permanent master password.",
                            "Once confirmed, your corporate workspace and role permissions will be immediately unlocked."
                        ],
                        security_note="In compliance with POPIA Section 19 and ISO 27001 data governance, this temporary passcode expires immediately upon initial sign-in. Never share these credentials."
                    )
                    send_email_async(
                        subject=email_subject,
                        text_body=email_text,
                        recipient_list=[email_identity],
                        from_email=sender_email,
                        html_body=email_html,
                    )
                except Exception as e:
                    import logging
                    logger = logging.getLogger(__name__)
                    logger.error(f"Failed to queue onboarding email to {email_identity}: {e}")

                response_serializer = EmployeeSerializer(new_profile)
                return Response(response_serializer.data, status=201)
        except IntegrityError as e:
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f'Onboarding integrity error: {str(e)}', exc_info=True)
            return Response({'error': f'Onboarding integrity error: {str(e)}'}, status=400)
        except UserProfile.DoesNotExist:
            return Response({'error': 'Failed to create user profile. Please try again.'}, status=400)
        except Exception as e:

            import logging
            logger = logging.getLogger(__name__)
            logger.error(f'Onboarding error: {str(e)}', exc_info=True)
            return Response({'error': 'An error occurred during onboarding. Please try again.'}, status=400)
    
    def update(self, request, *args, **kwargs):
        """Update employee details - system admin or CEO/Executive within same company."""
        user = request.user
        profile = getattr(user, 'profile', None)
        is_system_admin = user.is_superuser or user.is_staff
        
        instance = self.get_object()
        target_profile = instance
        
        if not is_system_admin:

            if not profile or not profile.can_onboard:
                return Response({'error': 'Only CEOs, Executives, or system administrators can update employees.'}, status=403)
            
            my_company = normalize_company_name(profile.company_name)
            target_company = normalize_company_name(target_profile.company_name)
            if my_company != target_company:
                return Response({'error': 'Cannot update employees from other companies.'}, status=403)

            ROLE_RANK = {'admin': 5, 'executive': 4, 'manager': 3, 'supervisor': 2, 'user': 1}
            new_role = request.data.get('role')
            if new_role and ROLE_RANK.get(new_role, 0) >= ROLE_RANK.get(profile.role, 0):
                return Response({'error': f'Cannot assign role equal to or higher than your own ({profile.get_role_display()}).'}, status=403)
        
        partial = kwargs.pop('partial', False)

        user_obj = instance.user
        if 'first_name' in request.data:
            user_obj.first_name = request.data['first_name']
        if 'last_name' in request.data:
            user_obj.last_name = request.data['last_name']
        if 'email' in request.data:
            user_obj.email = request.data['email']
        user_obj.save()

        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        
        return Response(serializer.data)
    
    def destroy(self, request, *args, **kwargs):
        """
        Delete employee - SYSTEM ADMINS ONLY.
        Client admins (CEOs) can view and add employees, but cannot delete.
        Deletion must go through offboarding request or Admin Console.
        """

        if not (request.user.is_superuser or request.user.is_staff):
            return Response({
                'error': 'Only system administrators can delete employee accounts. '
                         'Use "Request Offboarding" to submit a deletion request to your system admin.'
            }, status=403)
        
        instance = self.get_object()
        if instance.user == request.user:
            return Response({'error': 'Cannot delete your own account'}, status=400)

        OnboardingLog.objects.create(
            employee=None,  # Will be deleted
            employee_name=f"{instance.user.first_name} {instance.user.last_name}".strip() or instance.user.username,
            employee_email=instance.user.email,
            action='offboard',
            performed_by=request.user,
            performed_by_name=f"{request.user.first_name} {request.user.last_name}".strip() or request.user.username,
            company_name=instance.company_name or '',
            reason='Account deleted by system administrator',
        )

        from .models import DeletedUserLog
        DeletedUserLog.objects.create(
            username=instance.user.username,
            email=instance.user.email,
            registration_ip=instance.registration_ip,
            last_login_ip=instance.last_login_ip,
            company_name=instance.company_name,
        )
        
        instance.user.delete()  # Cascades to profile
        return Response({'message': 'Employee deleted successfully'}, status=204)
    
    @action(detail=False, methods=['get'])
    def available_slots(self, request):
        """Get remaining employee slots based on tier, scoped per company"""
        user = request.user

        if user.is_superuser or user.is_staff:
            return Response({
                'remaining_slots': 999,
                'current_users': User.objects.filter(is_superuser=False, is_staff=False).count(),
                'max_users': 999,
                'can_add_more': True,
                'tier': 'ultimate'
            })

        profile = getattr(user, 'profile', None)
        company_name = normalize_company_name((profile.company_name if profile else '') or '')

        user_tier = getattr(profile, 'tier', 'luxury')
        org = getattr(profile, 'organization', None)
        if org:
            user_tier = getattr(org, 'subscription_tier', 'luxury')

        is_trial = (user_tier == 'trial') or (org and getattr(org, 'is_trial_active', False))

        TIER_SEAT_LIMITS = {
            'basic': 3,
            'classic': 3,
            'luxury': 5,
            'trial': 999,
            'executive': 15,
            'enterprise': 999,
        }
        max_users = 999 if is_trial else TIER_SEAT_LIMITS.get((user_tier or 'luxury').lower(), 5)

        client_user_count = User.objects.filter(
            is_superuser=False,
            is_staff=False,
            profile__company_name__iexact=company_name
        ).count()
        remaining = 999 if is_trial else max(0, max_users - client_user_count)

        can_add = remaining > 0
        blocked_reason = None
        if not is_trial and (user_tier == 'basic' or user_tier == 'classic') and profile and profile.role != 'admin':
            can_add = False
            blocked_reason = 'Only the CEO/Administrator can onboard employees on Luxury Basic'
        elif not is_trial and user_tier == 'luxury' and profile and profile.role == 'manager':
            manager_subordinates = UserProfile.objects.filter(
                Q(onboarded_by=user) | Q(reports_to=user),
                company_name__iexact=company_name
            ).count()
            if manager_subordinates >= 2:
                can_add = False
                blocked_reason = 'Managers on Luxury Team can onboard up to 2 subordinates'
        
        return Response({
            'tier': 'trial' if is_trial else user_tier,
            'remaining_slots': remaining,
            'current_users': client_user_count,
            'max_users': max_users,
            'can_add_more': can_add,
            'upgrade_required': (remaining == 0 and not is_trial),
            'blocked_reason': blocked_reason,
            'is_trial': is_trial
        })
    
    @action(detail=False, methods=['post'])
    def confirm_add(self, request):
        """Disabled - all onboarding goes through hierarchy now."""
        return Response({'error': 'Delegated employee creation is disabled. Use hierarchy-based onboarding.'}, status=403)
    
    @action(detail=True, methods=['post'])
    def toggle_add_permission(self, request, pk=None):
        """Disabled - onboarding is controlled by role hierarchy."""
        return Response({'error': 'Onboarding permissions are now based on role hierarchy (CEO → Executive).'}, status=403)

    @action(detail=False, methods=['get'])
    def onboarding_logs(self, request):
        """
        ADMP: Get onboarding/offboarding audit logs for the company.
        GET /api/employees/onboarding_logs/
        """
        user = request.user
        profile = getattr(user, 'profile', None)
        
        if user.is_superuser or user.is_staff:
            logs = OnboardingLog.objects.all()
        elif profile and profile.company_name:
            company_name = normalize_company_name(profile.company_name)
            logs = OnboardingLog.objects.filter(company_name__iexact=company_name)
        else:
            logs = OnboardingLog.objects.none()
        
        action_filter = request.query_params.get('action')
        if action_filter in ['onboard', 'offboard']:
            logs = logs.filter(action=action_filter)
        
        serializer = OnboardingLogSerializer(logs[:100], many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get', 'post'])
    def offboarding_requests(self, request):
        """
        ADMP: Manage offboarding requests.
        GET  /api/employees/offboarding_requests/ — list requests
        POST /api/employees/offboarding_requests/ — create request (CEO/Executive)
        """
        user = request.user
        profile = getattr(user, 'profile', None)
        
        if request.method == 'GET':
            if user.is_superuser or user.is_staff:
                requests_qs = OffboardingRequest.objects.all()
            elif profile and profile.company_name:
                company_name = normalize_company_name(profile.company_name)
                requests_qs = OffboardingRequest.objects.filter(company_name__iexact=company_name)
            else:
                requests_qs = OffboardingRequest.objects.none()
            
            status_filter = request.query_params.get('status')
            if status_filter in ['pending', 'approved', 'rejected']:
                requests_qs = requests_qs.filter(status=status_filter)
            
            serializer = OffboardingRequestSerializer(requests_qs[:50], many=True)
            return Response(serializer.data)

        if not profile:
            return Response({'error': 'Profile not found'}, status=400)

        if not profile.can_onboard and not (user.is_superuser or user.is_staff):
            return Response({
                'error': 'Only CEOs and Executives can request employee offboarding. Contact your supervisor.'
            }, status=403)
        
        create_ser = OffboardingRequestCreateSerializer(data=request.data)
        create_ser.is_valid(raise_exception=True)
        
        employee_id = create_ser.validated_data['employee_id']
        reason = create_ser.validated_data['reason']
        
        try:
            target_user = User.objects.get(id=employee_id)
        except User.DoesNotExist:
            return Response({'error': 'Employee not found'}, status=404)

        if target_user == user:
            return Response({'error': 'You cannot request your own offboarding'}, status=400)

        target_profile = getattr(target_user, 'profile', None)
        if target_profile:
            target_company = normalize_company_name(target_profile.company_name)
            my_company = normalize_company_name(profile.company_name)
            if target_company != my_company and not (user.is_superuser or user.is_staff):
                return Response({'error': 'Cannot offboard employees from other companies'}, status=403)

        if OffboardingRequest.objects.filter(employee=target_user, status='pending').exists():
            return Response({'error': 'An offboarding request is already pending for this employee'}, status=400)
        
        offboard_request = OffboardingRequest.objects.create(
            employee=target_user,
            employee_name=f"{target_user.first_name} {target_user.last_name}".strip() or target_user.username,
            employee_email=target_user.email,
            requested_by=user,
            requested_by_name=f"{user.first_name} {user.last_name}".strip() or user.username,
            company_name=normalize_company_name(profile.company_name),
            reason=reason,
        )
        
        serializer = OffboardingRequestSerializer(offboard_request)
        return Response(serializer.data, status=201)
    
    @action(detail=False, methods=['post'], url_path='process_offboarding')
    def process_offboarding(self, request):
        """
        ADMP: System admin processes offboarding request.
        POST /api/employees/process_offboarding/
        Body: { request_id, action: 'approve'|'reject', admin_notes }
        """
        if not (request.user.is_superuser or request.user.is_staff):
            return Response({'error': 'Only system administrators can process offboarding requests'}, status=403)
        
        request_id = request.data.get('request_id')
        action_type = request.data.get('action')  # 'approve' or 'reject'
        admin_notes = request.data.get('admin_notes', '')
        
        if action_type not in ['approve', 'reject']:
            return Response({'error': 'Action must be "approve" or "reject"'}, status=400)
        
        try:
            offboard_req = OffboardingRequest.objects.get(id=request_id, status='pending')
        except OffboardingRequest.DoesNotExist:
            return Response({'error': 'Pending offboarding request not found'}, status=404)
        
        offboard_req.processed_by = request.user
        offboard_req.processed_at = timezone.now()
        offboard_req.admin_notes = admin_notes
        
        if action_type == 'approve':
            offboard_req.status = 'approved'
            offboard_req.save()

            target_profile = getattr(offboard_req.employee, 'profile', None)
            if target_profile:
                target_profile.is_offboarded = True
                target_profile.offboarded_at = timezone.now()
                target_profile.save()

            offboard_req.employee.is_active = False
            offboard_req.employee.save()

            OnboardingLog.objects.create(
                employee=offboard_req.employee,
                employee_name=offboard_req.employee_name,
                employee_email=offboard_req.employee_email,
                action='offboard',
                performed_by=request.user,
                performed_by_name=f"{request.user.first_name} {request.user.last_name}".strip() or request.user.username,
                company_name=offboard_req.company_name,
                reason=offboard_req.reason,
            )
            
            return Response({'message': f'{offboard_req.employee_name} has been offboarded successfully.'})
        else:
            offboard_req.status = 'rejected'
            offboard_req.save()
            return Response({'message': f'Offboarding request for {offboard_req.employee_name} has been rejected.'})
    
    @action(detail=False, methods=['get'])
    def org_chart(self, request):
        """
        ADMP: Get organizational hierarchy for the company.
        GET /api/employees/org_chart/
        Returns a flat list with reports_to relationships for building tree view.
        """
        user = request.user
        profile = getattr(user, 'profile', None)
        
        if user.is_superuser or user.is_staff:
            profiles = UserProfile.objects.filter(
                user__is_superuser=False, user__is_staff=False, is_offboarded=False
            ).select_related('user', 'reports_to')
        elif profile and profile.company_name:
            company_name = normalize_company_name(profile.company_name)
            profiles = UserProfile.objects.filter(
                company_name__iexact=company_name, is_offboarded=False
            ).select_related('user', 'reports_to')
        else:
            profiles = UserProfile.objects.none()
        
        chart_data = []
        for p in profiles:
            chart_data.append({
                'id': p.user.id,
                'name': f"{p.user.first_name} {p.user.last_name}".strip() or p.user.username,
                'role': p.role,
                'role_display': p.get_role_display(),
                'job_title': p.job_title,
                'department': p.department,
                'reports_to': p.reports_to_id,
                'email': p.user.email,
            })
        
        return Response(chart_data)


class ClientEmployeeManagementView(APIView):
    """
    System Admin endpoint to view all clients and their employees
    Provides full oversight and management capabilities
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        """Get all clients (non-system users) grouped by company"""
        if not has_user_management_access(request):
            raise PermissionDenied('System admin access required.')

        # Ghost account: explicitly exclude adminluxury even though is_superuser=False filter exists
        client_users = User.objects.filter(
            is_superuser=False,
            is_staff=False
        ).exclude(
            username__iexact='adminluxury'
        ).select_related('profile').order_by('profile__company_name', '-date_joined')

        companies_data = {}
        for user in client_users:
            profile = user.profile if hasattr(user, 'profile') else None
            if not profile:
                continue
            
            company_name = profile.company_name or 'No Company'
            
            if company_name not in companies_data:
                companies_data[company_name] = {
                    'company_name': company_name,
                    'users': [],
                    'total_users': 0,
                    'admins': 0,
                    'employees': 0
                }

            contact_count = visible_contacts_queryset(user).count()
            company_count = Company.objects.filter(user=user).count()
            deal_count = Deal.objects.filter(user=user).count()
            ticket_count = Ticket.objects.filter(Q(assigned_to=user) | Q(created_by=user)).distinct().count()
            
            user_data = {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'full_name': f"{user.first_name} {user.last_name}".strip() or user.username,
                'date_joined': user.date_joined,
                'last_login': user.last_login,
                'is_active': user.is_active,
                'role': profile.role,
                'job_title': profile.job_title,
                'department': profile.department,
                'employee_id': profile.employee_id,
                'phone': profile.phone,
                'start_date': profile.start_date,
                'is_banned': profile.is_banned,
                'ban_reason': profile.ban_reason,
                'payment_status': profile.payment_status,
                'registration_ip': profile.registration_ip,
                'last_login_ip': profile.last_login_ip,
                'data_counts': {
                    'contacts': contact_count,
                    'companies': company_count,
                    'deals': deal_count,
                    'tickets': ticket_count
                }
            }
            
            companies_data[company_name]['users'].append(user_data)
            companies_data[company_name]['total_users'] += 1
            if profile.role == 'admin':
                companies_data[company_name]['admins'] += 1
            else:
                companies_data[company_name]['employees'] += 1

        companies_list = list(companies_data.values())

        total_clients = len(client_users)
        total_companies = len(companies_data)
        total_admins = sum(c['admins'] for c in companies_list)
        total_employees = sum(c['employees'] for c in companies_list)
        
        return Response({
            'companies': companies_list,
            'stats': {
                'total_clients': total_clients,
                'total_companies': total_companies,
                'total_admins': total_admins,
                'total_employees': total_employees,
                'luxury_tier_limit': int(LUXURY_TIER_LIMITS.get('max_users', 50))
            }
        })
    
    def post(self, request):
        """Admin actions: reset password, ban/unban user, etc."""
        if not has_user_management_access(request):
            raise PermissionDenied('System admin access required.')
        
        action = request.data.get('action')

        if action == 'onboard_company':
            company_name = (request.data.get('company_name') or '').strip()
            trading_name = (request.data.get('trading_name') or '').strip()
            cipc_number = (request.data.get('cipc_number') or '').strip()
            tax_number = (request.data.get('tax_number') or '').strip()
            admin_name = (request.data.get('admin_name') or '').strip()
            admin_email = (request.data.get('admin_email') or '').strip().lower()
            admin_phone = (request.data.get('admin_phone') or '').strip()
            subscription_tier = request.data.get('subscription_tier', 'trial')
            password = (request.data.get('password') or '').strip()
            is_verified = bool(request.data.get('is_verified', False))

            if not company_name:
                return Response({'error': 'Company Legal Name is mandatory.'}, status=400)
            if not admin_email or '@' not in admin_email:
                return Response({'error': 'Valid Admin Corporate Email is required.'}, status=400)
            if not admin_name:
                return Response({'error': 'Primary Admin / Director Name is required.'}, status=400)

            if User.objects.filter(username__iexact=admin_email).exists() or User.objects.filter(email__iexact=admin_email).exists():
                return Response({'error': f'A user with email/username {admin_email} already exists.'}, status=400)

            import random, string
            if not password:
                chars = string.ascii_letters + string.digits + '!@#$'
                password = ''.join(random.choices(chars, k=12))

            name_parts = admin_name.split(None, 1)
            first_name = name_parts[0]
            last_name = name_parts[1] if len(name_parts) > 1 else ''

            try:
                with transaction.atomic():
                    org, created_org = Organization.objects.get_or_create(
                        name=company_name,
                        defaults={
                            'subscription_tier': subscription_tier,
                            'is_active': True,
                            'is_cipc_verified': is_verified,
                        }
                    )
                    if not created_org:
                        org.subscription_tier = subscription_tier
                        org.is_active = True
                        if is_verified:
                            org.is_cipc_verified = True
                        org.save()

                    new_user = User.objects.create_user(
                        username=admin_email,
                        email=admin_email,
                        first_name=first_name,
                        last_name=last_name,
                        password=password
                    )

                    profile = new_user.profile
                    profile.company_name = company_name
                    profile.organization = org
                    profile.role = 'admin'
                    profile.phone = admin_phone
                    profile.payment_status = 'paid' if subscription_tier != 'trial' else 'trial'
                    profile.save()

                    from .models import OrganizationSubscription
                    OrganizationSubscription.objects.update_or_create(
                        organization=org,
                        defaults={
                            'status': 'active' if subscription_tier != 'trial' else 'trial',
                            'current_period_start': timezone.now()
                        }
                    )

                    if cipc_number:
                        TenantVerification.objects.update_or_create(
                            organization=org,
                            defaults={
                                'company_name': company_name,
                                'trading_name': trading_name,
                                'cipc_number': cipc_number,
                                'tax_number': tax_number,
                                'director_name': admin_name,
                                'submitted_by': request.user,
                                'reviewed_by': request.user if is_verified else None,
                                'reviewed_at': timezone.now() if is_verified else None,
                                'status': 'verified' if is_verified else 'pending'
                            }
                        )

                    record_audit_event(
                        'TENANT_ONBOARDED',
                        f"Platform Owner {request.user.username} onboarded corporate tenant '{company_name}' ({subscription_tier}) with Admin {admin_email}",
                        user=request.user,
                        request=request,
                        organization=org,
                        severity='SECURITY',
                        metadata={
                            'company_name': company_name,
                            'admin_email': admin_email,
                            'tier': subscription_tier,
                            'cipc_number': cipc_number
                        }
                    )

                    return Response({
                        'success': True,
                        'message': f"Corporate tenant '{company_name}' provisioned successfully!",
                        'credentials': {
                            'username': admin_email,
                            'email': admin_email,
                            'password': password,
                            'company_name': company_name,
                            'organization_id': str(org.id),
                            'subscription_tier': subscription_tier
                        }
                    }, status=201)
            except Exception as e:
                return Response({'error': f'Failed to onboard corporate tenant: {str(e)}'}, status=500)

        user_id = request.data.get('user_id')
        
        if not action or not user_id:
            return Response({'error': 'action and user_id required'}, status=400)
        
        try:
            target_user = User.objects.get(id=user_id)
            
            if action == 'reset_password':

                import random
                import string
                temp_password = ''.join(random.choices(string.ascii_letters + string.digits, k=12))
                target_user.set_password(temp_password)
                target_user.save()
                # Mark user profile to require password change on next login
                try:
                    if hasattr(target_user, 'profile'):
                        target_user.profile.requires_password_reset = True
                        target_user.profile.save()
                except Exception:
                    pass

                return Response({
                    'message': 'Password reset successfully',
                    'temporary_password': temp_password,
                    'username': target_user.username
                })
            
            elif action == 'toggle_active':
                target_user.is_active = not target_user.is_active
                target_user.save()
                return Response({
                    'message': f'User {"activated" if target_user.is_active else "deactivated"}',
                    'is_active': target_user.is_active
                })
            
            elif action == 'ban':
                reason = request.data.get('reason', 'Banned by admin')
                if hasattr(target_user, 'profile'):
                    target_user.profile.ban_user(reason)
                    return Response({'message': 'User banned successfully'})
                return Response({'error': 'User has no profile'}, status=400)
            
            elif action == 'unban':
                if hasattr(target_user, 'profile'):
                    target_user.profile.unban_user()
                    return Response({'message': 'User unbanned successfully'})
                return Response({'error': 'User has no profile'}, status=400)
            
            else:
                return Response({'error': f'Unknown action: {action}'}, status=400)
        
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=404)




class DivisionViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing organizational divisions/departments.
    Users can only access divisions within their company.
    """
    serializer_class = DivisionSerializer
    permission_classes = [IsAuthenticated]

    DEFAULT_DIVISIONS = [
        ('Executive Office', 'Leadership and strategic oversight'),
        ('Human Resources', 'People operations and talent management'),
        ('Sales', 'Revenue growth and client acquisition'),
        ('Operations', 'Daily business operations and execution'),
        ('Finance', 'Accounting, budgeting and financial control'),
        ('IT & Systems', 'Technology infrastructure and systems support'),
    ]

    def _ensure_default_divisions(self, company_name):
        """Create baseline divisions for a company if none exist yet."""
        existing_count = Division.objects.filter(company_name__iexact=company_name).count()
        if existing_count > 0:
            return 0

        created = 0
        for name, description in self.DEFAULT_DIVISIONS:
            _, was_created = Division.objects.get_or_create(
                name=name,
                company_name=company_name,
                defaults={'description': description},
            )
            if was_created:
                created += 1
        return created
    
    def get_queryset(self):
        user = self.request.user

        if user.is_superuser or user.is_staff:
            return Division.objects.all().select_related('manager')

        profile = getattr(user, 'profile', None)
        if profile and profile.company_name:
            company_name = normalize_company_name(profile.company_name)
            self._ensure_default_divisions(company_name)
            return Division.objects.filter(company_name__iexact=company_name).select_related('manager')
        
        return Division.objects.none()
    
    def perform_create(self, serializer):
        """Auto-set company_name from user's profile"""
        user = self.request.user
        profile = getattr(user, 'profile', None)
        
        if user.is_superuser or user.is_staff:

            serializer.save()
        elif profile and profile.company_name:
            company_name = normalize_company_name(profile.company_name)
            serializer.save(company_name=company_name)
        else:
            raise ValidationError("User has no company association")

    @action(detail=False, methods=['post'])
    def seed_defaults(self, request):
        """
        Seed default divisions for the caller's company when needed.
        POST /api/divisions/seed_defaults/
        """
        user = request.user
        profile = getattr(user, 'profile', None)

        if not profile or not profile.company_name:
            return Response({'error': 'User has no company association'}, status=400)

        company_name = normalize_company_name(profile.company_name)
        created = self._ensure_default_divisions(company_name)
        total = Division.objects.filter(company_name__iexact=company_name).count()

        return Response({
            'success': True,
            'company_name': company_name,
            'created': created,
            'total_divisions': total,
        })


class AssetCategoryViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing asset categories.
    Users can only access categories within their company.
    """
    serializer_class = AssetCategorySerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user

        if user.is_superuser or user.is_staff:
            return AssetCategory.objects.all()

        profile = getattr(user, 'profile', None)
        if profile and profile.company_name:
            company_name = normalize_company_name(profile.company_name)
            return AssetCategory.objects.filter(company_name__iexact=company_name)
        
        return AssetCategory.objects.none()
    
    def perform_create(self, serializer):
        """Auto-set company_name from user's profile"""
        user = self.request.user
        profile = getattr(user, 'profile', None)
        
        if user.is_superuser or user.is_staff:
            serializer.save()
        elif profile and profile.company_name:
            company_name = normalize_company_name(profile.company_name)
            serializer.save(company_name=company_name)
        else:
            raise ValidationError("User has no company association")
    
    @action(detail=False, methods=['post'])
    def seed_defaults(self, request):
        """
        ADMP: Seed default asset categories for a company if none exist.
        POST /api/asset-categories/seed_defaults/
        """
        user = request.user
        profile = getattr(user, 'profile', None)
        
        if not profile or not profile.company_name:
            return Response({'error': 'User has no company association'}, status=400)
        
        company_name = normalize_company_name(profile.company_name)
        existing_count = AssetCategory.objects.filter(company_name__iexact=company_name).count()
        
        if existing_count > 0:
            return Response({
                'message': 'Categories already exist for this company',
                'count': existing_count
            })

        default_categories = [
            {'name': 'Laptop', 'category_type': 'it_equipment', 'description': 'Laptop computers and notebooks'},
            {'name': 'Desktop Computer', 'category_type': 'it_equipment', 'description': 'Desktop PCs and workstations'},
            {'name': 'Monitor', 'category_type': 'it_equipment', 'description': 'Computer monitors and displays'},
            {'name': 'Keyboard', 'category_type': 'it_equipment', 'description': 'Computer keyboards'},
            {'name': 'Mouse', 'category_type': 'it_equipment', 'description': 'Computer mice and pointing devices'},
            {'name': 'Docking Station', 'category_type': 'it_equipment', 'description': 'Laptop docks and port replicators'},
            {'name': 'Laptop Stand', 'category_type': 'office_furniture', 'description': 'Laptop stands and risers'},
            {'name': 'Headset', 'category_type': 'communication', 'description': 'Headphones and headsets'},
            {'name': 'Webcam', 'category_type': 'communication', 'description': 'Web cameras'},
            {'name': 'Mobile Phone', 'category_type': 'communication', 'description': 'Company mobile phones'},
            {'name': 'Tablet', 'category_type': 'it_equipment', 'description': 'Tablets and iPads'},
            {'name': 'Printer', 'category_type': 'it_equipment', 'description': 'Printers and multifunction devices'},
            {'name': 'Network Equipment', 'category_type': 'it_equipment', 'description': 'Routers, switches, access points'},
            {'name': 'Office Desk', 'category_type': 'office_furniture', 'description': 'Desks and workstations'},
            {'name': 'Office Chair', 'category_type': 'office_furniture', 'description': 'Office chairs and seating'},
            {'name': 'Filing Cabinet', 'category_type': 'office_furniture', 'description': 'Storage cabinets and shelves'},
            {'name': 'Vehicle', 'category_type': 'vehicles', 'description': 'Company vehicles'},
            {'name': 'Software License', 'category_type': 'software', 'description': 'Software licenses and subscriptions'},
            {'name': 'Tools & Equipment', 'category_type': 'machinery', 'description': 'General tools and equipment'},
            {'name': 'Other Assets', 'category_type': 'other', 'description': 'Miscellaneous assets'},
        ]
        
        created_categories = []
        for cat_data in default_categories:
            category = AssetCategory.objects.create(
                name=cat_data['name'],
                category_type=cat_data['category_type'],
                description=cat_data['description'],
                company_name=company_name
            )
            created_categories.append(category)
        
        serializer = AssetCategorySerializer(created_categories, many=True)
        return Response({
            'message': f'Created {len(created_categories)} default categories',
            'categories': serializer.data
        }, status=201)


class AssetViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing assets (equipment, property, etc.).
    Users can only access assets within their company.
    Supports filtering by status, category, assigned employee, and division.
    """
    permission_classes = [IsAuthenticated]
    filterset_fields = ['status', 'condition', 'category', 'assigned_to', 'division']
    search_fields = ['asset_tag', 'name', 'serial_number', 'model', 'manufacturer', 'location']
    ordering_fields = ['created_at', 'name', 'purchase_date', 'status']
    ordering = ['-created_at']
    
    def get_serializer_class(self):
        """Use lightweight serializer for list, full serializer for detail"""
        if self.action == 'list':
            from .serializers import AssetListSerializer
            return AssetListSerializer
        from .serializers import AssetSerializer
        return AssetSerializer
    
    def get_queryset(self):
        user = self.request.user
        profile = getattr(user, 'profile', None)
        if not profile:
            return Asset.objects.none()

        if profile.organization:
            if profile.role in ['admin', 'manager', 'executive'] or profile.is_admin:
                return Asset.objects.filter(organization=profile.organization).select_related(
                    'category', 'assigned_to', 'division', 'created_by'
                )
            return Asset.objects.filter(
                organization=profile.organization,
                assigned_to=user
            ).select_related('category', 'assigned_to', 'division', 'created_by')

        if profile.company_name:
            company_name = normalize_company_name(profile.company_name)
            if profile.role in ['admin', 'manager', 'executive'] or profile.is_admin:
                return Asset.objects.filter(company_name__iexact=company_name).select_related(
                    'category', 'assigned_to', 'division', 'created_by'
                )
            return Asset.objects.filter(
                company_name__iexact=company_name,
                assigned_to=user
            ).select_related('category', 'assigned_to', 'division', 'created_by')

        if is_owner_admin_user(user):
            return Asset.objects.filter(
                Q(organization__slug='mtambo-holdings') |
                Q(created_by=user) | Q(assigned_to=user)
            ).select_related('category', 'assigned_to', 'division', 'created_by')

        return Asset.objects.filter(assigned_to=user).select_related('category', 'assigned_to', 'division', 'created_by')
    
    def perform_create(self, serializer):
        """
        Create assets - restricted to superuser, admin (CEO), and managers only.
        Regular employees cannot create assets.
        """
        user = self.request.user
        profile = getattr(user, 'profile', None)
        org = getattr(profile, 'organization', None) if profile else None

        if not (user.is_superuser or user.is_staff):
            if not profile:
                raise PermissionDenied('Only authenticated corporate profiles can create assets.')
            if profile.role in ['admin', 'executive']:
                pass
            elif profile.role == 'manager' and getattr(profile, 'can_manage_assets', False):
                pass
            else:
                raise PermissionDenied('Only CEOs/Administrators, or Managers with delegated asset permissions, can create assets.')
        
        company_name = normalize_company_name(profile.company_name) if profile else ''
        
        if org:
            current_count = Asset.objects.filter(organization=org).count()
            allowed, limit, msg = check_org_quota(org, 'assets', current_count)
            if not allowed:
                raise ValidationError({'detail': msg})

        serializer.save(created_by=user, organization=org, company_name=company_name)
    
    @action(detail=False, methods=['get'])
    def stats(self, request):
        """Get asset statistics for the company"""
        queryset = self.get_queryset()
        
        total_assets = queryset.count()
        by_status = queryset.values('status').annotate(count=Count('id'))
        by_category = queryset.values('category__name').annotate(count=Count('id'))
        assigned_count = queryset.filter(assigned_to__isnull=False).count()
        available_count = queryset.filter(status='available').count()

        total_purchase_cost = queryset.aggregate(total=Sum('purchase_cost'))['total'] or 0
        total_current_value = queryset.aggregate(total=Sum('current_value'))['total'] or 0
        
        return Response({
            'total_assets': total_assets,
            'assigned': assigned_count,
            'available': available_count,
            'by_status': list(by_status),
            'by_category': list(by_category),
            'total_purchase_cost': float(total_purchase_cost),
            'total_current_value': float(total_current_value),
            'total_depreciation': float(total_purchase_cost - total_current_value)
        })
    
    @action(detail=True, methods=['post'])
    def assign(self, request, pk=None):
        """Assign asset to an employee"""
        asset = self.get_object()
        employee_id = request.data.get('employee_id')
        
        if not employee_id:
            return Response({'error': 'employee_id required'}, status=400)
        
        try:
            employee = User.objects.get(id=employee_id)
            asset.assigned_to = employee
            asset.status = 'active'
            asset.save()
            
            serializer = self.get_serializer(asset)
            return Response(serializer.data)
        except User.DoesNotExist:
            return Response({'error': 'Employee not found'}, status=404)
    
    @action(detail=True, methods=['post'])
    def unassign(self, request, pk=None):
        """Unassign asset from employee"""
        asset = self.get_object()
        asset.assigned_to = None
        asset.status = 'available'
        asset.save()
        
        serializer = self.get_serializer(asset)
        return Response(serializer.data)




class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        profile = getattr(user, 'profile', None)
        if not profile:
            return Product.objects.none()

        if profile.organization:
            return Product.objects.filter(
                Q(organization=profile.organization) |
                Q(company_name__iexact=profile.organization.name)
            )

        if profile.company_name:
            return Product.objects.filter(company_name__iexact=profile.company_name)

        if is_owner_admin_user(user):
            return Product.objects.filter(
                Q(organization__slug='mtambo-holdings') |
                Q(company_name__iexact='THE FINISHER LUXURY') |
                Q(company_name__iexact='Mtambo Holdings')
            )

        return Product.objects.filter(company_name='')

    def perform_create(self, serializer):
        import logging
        import traceback
        logger = logging.getLogger(__name__)
        user = self.request.user
        from django.core.exceptions import ValidationError
        from .models import Company
        try:
            if user.is_superuser:
                company_name = getattr(getattr(user, 'profile', None), 'company_name', '') or 'THE FINISHER LUXURY'
            else:
                company = getattr(user, 'profile', None)
                company_name = company.company_name if company else ''
                # Quick admin fix: if admin and no company_name, set default
                if (not company_name or not company_name.strip()) and hasattr(user, 'profile'):
                    company_name = f"{user.first_name} {user.last_name} Company".strip()
                    user.profile.company_name = company_name
                    user.profile.save()
                # Ensure Company object exists for this user and company_name
                if company_name:
                    company_obj, created = Company.objects.get_or_create(user=user, name=company_name)
            if not company_name:
                raise ValidationError("Company name is required to create a product.")
            # Log the incoming payload for debugging
            # Check product catalog quota
            profile = getattr(user, 'profile', None)
            org = getattr(profile, 'organization', None) if profile else None
            if org:
                current_count = Product.objects.filter(company_name__iexact=company_name).count()
                allowed, limit, msg = check_org_quota(org, 'products', current_count)
                if not allowed:
                    from rest_framework.exceptions import ValidationError as DRFValidationError
                    raise DRFValidationError({'detail': msg})

            # Provide a default billing_type to avoid DB NOT NULL errors if column exists
            serializer.save(created_by=user, company_name=company_name, billing_type='standard')
        except Exception as exc:
            # Log full traceback to help diagnose 500s in production
            tb = traceback.format_exc()
            logger.error("Exception in ProductViewSet.perform_create: %s\n%s", str(exc), tb)
            # Re-raise to preserve original behavior (will produce 500)
            raise


class LineItemViewSet(viewsets.ModelViewSet):
    serializer_class = LineItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        deal_id = self.request.query_params.get('deal')
        qs = LineItem.objects.select_related('product', 'deal')
        if deal_id:
            qs = qs.filter(deal_id=deal_id)
        if not user.is_superuser:
            qs = qs.filter(deal__user=user)
        return qs

    def perform_create(self, serializer):
        deal = serializer.validated_data['deal']
        if not self.request.user.is_superuser and deal.user != self.request.user:
            raise PermissionDenied("You do not own this deal.")
        serializer.save()

    @action(detail=False, methods=['get'], url_path='deal-summary/(?P<deal_id>[0-9]+)')
    def deal_summary(self, request, deal_id=None):
        """Get line item totals for a deal."""
        items = LineItem.objects.filter(deal_id=deal_id).select_related('product')
        if not request.user.is_superuser:
            items = items.filter(deal__user=request.user)
        subtotal = sum(i.subtotal for i in items)
        tax = sum(i.tax_amount for i in items)
        total = sum(i.total for i in items)
        return Response({
            'deal_id': int(deal_id),
            'item_count': items.count(),
            'subtotal': round(subtotal, 2),
            'tax': round(tax, 2),
            'total': round(total, 2),
            'items': LineItemSerializer(items, many=True).data
        })




class EmailTemplateViewSet(viewsets.ModelViewSet):
    serializer_class = EmailTemplateSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        profile = getattr(user, 'profile', None)
        if not profile:
            return EmailTemplate.objects.none()

        if profile.organization:
            return EmailTemplate.objects.filter(
                Q(company_name__iexact=profile.organization.name) |
                Q(created_by__profile__organization=profile.organization)
            )

        company_name = profile.company_name or ''
        if company_name:
            return EmailTemplate.objects.filter(company_name__iexact=company_name)

        if is_owner_admin_user(user):
            return EmailTemplate.objects.filter(
                Q(company_name__iexact='THE FINISHER LUXURY') |
                Q(company_name__iexact='Mtambo Holdings') |
                Q(created_by=user)
            )

        return EmailTemplate.objects.filter(created_by=user)

    def perform_create(self, serializer):
        user = self.request.user
        profile = getattr(user, 'profile', None)
        org = getattr(profile, 'organization', None) if profile else None
        company_name = profile.company_name if profile else ''
        if org:
            current_count = EmailTemplate.objects.filter(company_name__iexact=company_name).count()
            allowed, limit, msg = check_org_quota(org, 'templates', current_count)
            if not allowed:
                raise ValidationError({'detail': msg})
        serializer.save(created_by=user, company_name=company_name)


class EmailCampaignViewSet(viewsets.ModelViewSet):
    serializer_class = EmailCampaignSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        profile = getattr(user, 'profile', None)
        if not profile:
            return EmailCampaign.objects.none()

        if profile.organization:
            return EmailCampaign.objects.filter(organization=profile.organization)

        company_name = profile.company_name or ''
        if company_name:
            return EmailCampaign.objects.filter(company_name__iexact=company_name)

        if is_owner_admin_user(user):
            return EmailCampaign.objects.filter(
                Q(organization__slug='mtambo-holdings') |
                Q(company_name__iexact='THE FINISHER LUXURY') |
                Q(company_name__iexact='Mtambo Holdings')
            )

        return EmailCampaign.objects.filter(created_by=user)

    def perform_create(self, serializer):
        user = self.request.user
        profile = getattr(user, 'profile', None)
        org = getattr(profile, 'organization', None) if profile else None
        company_name = profile.company_name if profile else ''
        if org:
            current_count = EmailCampaign.objects.filter(organization=org).count()
            allowed, limit, msg = check_org_quota(org, 'campaigns', current_count)
            if not allowed:
                raise ValidationError({'detail': msg})
        serializer.save(created_by=user, organization=org, company_name=company_name)

    @action(detail=True, methods=['post'])
    def send(self, request, pk=None):
        """Send the campaign to all recipients."""
        campaign = self.get_object()
        if campaign.status == 'sent':
            return Response({'error': 'Campaign already sent'}, status=400)

        contact_ids = campaign.recipient_ids or []
        if not contact_ids:
            if campaign.organization:
                contacts = Contact.objects.filter(organization=campaign.organization)
            else:
                contacts = Contact.objects.filter(user__profile__company_name=campaign.company_name)
            if campaign.recipient_filter and campaign.recipient_filter.get('company_id'):
                contacts = contacts.filter(company_id=campaign.recipient_filter['company_id'])
            contact_ids = list(contacts.values_list('id', flat=True))

        created = 0
        for cid in contact_ids:
            try:
                obj, was_created = CampaignRecipient.objects.get_or_create(
                    campaign=campaign, contact_id=cid,
                    defaults={'status': 'sent', 'sent_at': timezone.now()}
                )
                if was_created:
                    created += 1
            except Exception:
                pass

        campaign.status = 'sent'
        campaign.sent_at = timezone.now()
        campaign.total_recipients = created
        campaign.sent_count = created
        campaign.save()

        return Response({
            'status': 'sent',
            'total_recipients': created,
            'message': f'Campaign sent to {created} recipients'
        })

    @action(detail=True, methods=['get'])
    def recipients(self, request, pk=None):
        """List recipients and their statuses."""
        campaign = self.get_object()
        recipients = campaign.recipients.select_related('contact').all()
        serializer = CampaignRecipientSerializer(recipients, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'], url_path='track-open')
    def track_open(self, request, pk=None):
        """Track an email open for a contact."""
        campaign = self.get_object()
        contact_id = request.data.get('contact_id')
        try:
            recipient = CampaignRecipient.objects.get(campaign=campaign, contact_id=contact_id)
            if recipient.status != 'opened':
                recipient.status = 'opened'
                recipient.opened_at = timezone.now()
                recipient.save()
                campaign.open_count += 1
                campaign.save()
            return Response({'tracked': True})
        except CampaignRecipient.DoesNotExist:
            return Response({'error': 'Recipient not found'}, status=404)

    @action(detail=True, methods=['post'], url_path='track-click')
    def track_click(self, request, pk=None):
        """Track an email link click for a contact."""
        campaign = self.get_object()
        contact_id = request.data.get('contact_id')
        try:
            recipient = CampaignRecipient.objects.get(campaign=campaign, contact_id=contact_id)
            recipient.status = 'clicked'
            recipient.clicked_at = timezone.now()
            recipient.save()
            campaign.click_count += 1
            campaign.save()
            return Response({'tracked': True})
        except CampaignRecipient.DoesNotExist:
            return Response({'error': 'Recipient not found'}, status=404)




class WorkflowViewSet(viewsets.ModelViewSet):
    serializer_class = WorkflowSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        profile = getattr(user, 'profile', None)
        if not profile:
            return Workflow.objects.none()

        if profile.organization:
            return Workflow.objects.filter(organization=profile.organization).prefetch_related('actions')

        company_name = profile.company_name or ''
        if company_name:
            return Workflow.objects.filter(company_name__iexact=company_name).prefetch_related('actions')

        if is_owner_admin_user(user):
            return Workflow.objects.filter(
                Q(organization__slug='mtambo-holdings') |
                Q(company_name__iexact='THE FINISHER LUXURY') |
                Q(company_name__iexact='Mtambo Holdings')
            ).prefetch_related('actions')

        return Workflow.objects.filter(created_by=user).prefetch_related('actions')

    def perform_create(self, serializer):
        user = self.request.user
        profile = getattr(user, 'profile', None)
        org = getattr(profile, 'organization', None) if profile else None
        company_name = profile.company_name if profile else ''

        if not user.is_superuser:
            count = Workflow.objects.filter(organization=org).count() if org else Workflow.objects.filter(company_name=company_name).count()
            if org:
                allowed, limit, msg = check_org_quota(org, 'workflows', count)
                if not allowed:
                    raise ValidationError({'detail': msg})
            elif count >= 10:
                raise ValidationError({'detail': 'Workflow limit reached for tier. Contact concierge to expand.'})
        serializer.save(created_by=user, organization=org, company_name=company_name)

    @action(detail=True, methods=['post'], url_path='add-action')
    def add_action(self, request, pk=None):
        """Add an action step to a workflow."""
        workflow = self.get_object()
        serializer = WorkflowActionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(workflow=workflow)
        return Response(WorkflowSerializer(workflow).data)

    @action(detail=True, methods=['post'], url_path='remove-action/(?P<action_id>[0-9]+)')
    def remove_action(self, request, pk=None, action_id=None):
        """Remove an action from a workflow."""
        workflow = self.get_object()
        try:
            action_obj = WorkflowAction.objects.get(id=action_id, workflow=workflow)
            action_obj.delete()
        except WorkflowAction.DoesNotExist:
            return Response({'error': 'Action not found'}, status=404)
        return Response(WorkflowSerializer(workflow).data)

    @action(detail=True, methods=['post'])
    def toggle(self, request, pk=None):
        """Toggle workflow active/inactive."""
        workflow = self.get_object()
        workflow.is_active = not workflow.is_active
        workflow.save()
        return Response({'is_active': workflow.is_active})

    @action(detail=True, methods=['get'])
    def logs(self, request, pk=None):
        """Get execution logs for a workflow."""
        workflow = self.get_object()
        logs = workflow.logs.all()[:50]
        return Response(WorkflowLogSerializer(logs, many=True).data)




class DashboardWidgetViewSet(viewsets.ModelViewSet):
    serializer_class = DashboardWidgetSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return DashboardWidget.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['post'], url_path='reorder')
    def reorder(self, request):
        """Batch update widget positions."""
        positions = request.data.get('positions', [])
        for pos in positions:
            DashboardWidget.objects.filter(
                id=pos['id'], user=request.user
            ).update(
                position_x=pos.get('x', 0),
                position_y=pos.get('y', 0),
                width=pos.get('w', 1),
                height=pos.get('h', 1)
            )
        return Response({'status': 'ok'})

    @action(detail=False, methods=['post'], url_path='reset-defaults')
    def reset_defaults(self, request):
        """Reset to default widgets."""
        DashboardWidget.objects.filter(user=request.user).delete()
        defaults = [
            {'widget_type': 'stat_card', 'title': 'Total Contacts', 'position_x': 0, 'position_y': 0, 'width': 3, 'height': 1},
            {'widget_type': 'stat_card', 'title': 'Total Deals', 'position_x': 3, 'position_y': 0, 'width': 3, 'height': 1},
            {'widget_type': 'stat_card', 'title': 'Revenue', 'position_x': 6, 'position_y': 0, 'width': 3, 'height': 1},
            {'widget_type': 'completed_tickets', 'title': 'Completed Tickets', 'position_x': 9, 'position_y': 0, 'width': 3, 'height': 1},
            {'widget_type': 'pipeline_chart', 'title': 'Pipeline', 'position_x': 0, 'position_y': 1, 'width': 6, 'height': 1},
            {'widget_type': 'activity_feed', 'title': 'Activity Feed', 'position_x': 6, 'position_y': 1, 'width': 3, 'height': 2},
            {'widget_type': 'deal_funnel', 'title': 'Deal Funnel', 'position_x': 0, 'position_y': 2, 'width': 6, 'height': 1},
            {'widget_type': 'recent_deals', 'title': 'Recent Deals', 'position_x': 6, 'position_y': 2, 'width': 6, 'height': 1},
        ]
        widgets = []
        for d in defaults:
            widgets.append(DashboardWidget.objects.create(user=request.user, **d))
        return Response(DashboardWidgetSerializer(widgets, many=True).data)

    @action(detail=False, methods=['get'], url_path='widget-data/(?P<widget_type>[a-z_]+)')
    def widget_data(self, request, widget_type=None):
        """Return live data for a specific widget type - NORMALIZED FORMAT."""
        user = request.user
        data = {}

        if user.is_superuser:
            contacts = Contact.objects.all()
            deals = Deal.objects.all()
            companies = Company.objects.all()
            tickets = Ticket.objects.all()
        else:
            contacts = visible_contacts_queryset(user)
            deals = Deal.objects.filter(user=user)
            companies = Company.objects.filter(user=user)
            tickets = Ticket.objects.filter(assigned_to=user)

        if widget_type == 'stat_card':
            data = {
                'contacts': contacts.count(),
                'companies': companies.count(),
                'deals': deals.count(),
                'revenue': float(deals.filter(stage='closed_won').aggregate(total=Sum('value'))['total'] or 0),
                'open_deals': deals.exclude(stage__in=['closed_won', 'closed_lost']).count(),
                'won_deals': deals.filter(stage='closed_won').count(),
            }
        elif widget_type == 'pipeline_chart':
            # FIXED: Returns ARRAY format [{stage, count}] not dict
            stages = ['lead', 'qualified', 'proposal', 'negotiation', 'closed_won', 'closed_lost']
            data = [
                {'stage': stage, 'count': deals.filter(stage=stage).count()}
                for stage in stages
            ]
        elif widget_type == 'revenue_chart':
            # FIXED: Returns object with 'months' array inside
            from django.db.models.functions import TruncMonth
            monthly = deals.filter(stage='closed_won').annotate(
                month=TruncMonth('created_at')
            ).values('month').annotate(
                total=Sum('value'), count=Count('id')
            ).order_by('month')[:12]
            months = [
                {
                    'label': m['month'].strftime('%b') if m['month'] else '',
                    'value': float(m['total'] or 0)
                }
                for m in monthly
            ]
            total = float(deals.filter(stage='closed_won').aggregate(t=Sum('value'))['t'] or 0)
            data = {'months': months, 'total': total}
        elif widget_type == 'deal_funnel':
            stages = ['lead', 'qualified', 'proposal', 'negotiation', 'closed_won']
            data = [
                {
                    'stage': s,
                    'count': deals.filter(stage=s).count(),
                    'value': float(deals.filter(stage=s).aggregate(v=Sum('value'))['v'] or 0)
                }
                for s in stages
            ]
        elif widget_type == 'activity_feed':
            if user.is_superuser:
                activities = ActivityLog.objects.all()[:10]
            else:
                activities = ActivityLog.objects.filter(user=user)[:10]
            data = [
                {
                    'id': a.id,
                    'action': a.action,
                    'entity_type': a.entity_type,
                    'entity_name': a.entity_name,
                    'created_at': str(a.created_at)
                }
                for a in activities
            ]
        elif widget_type == 'top_contacts':
            top = contacts.order_by('-last_contact_date')[:5]
            data = [
                {
                    'id': c.id,
                    'first_name': c.first_name,
                    'last_name': c.last_name,
                    'company_name': c.company.name if c.company else '—',
                    'email': c.email,
                    'health_score': c.health_score or 0
                }
                for c in top
            ]
        elif widget_type == 'completed_tickets':
            # NEW: Completed ticket stats
            completed = tickets.filter(status='completed')
            total_tickets = tickets.count()
            data = {
                'completed': completed.count(),
                'total': total_tickets,
                'completion_rate': round((completed.count() / total_tickets * 100) if total_tickets > 0 else 0, 1),
                'open': tickets.filter(status='open').count(),
                'in_progress': tickets.filter(status='in_progress').count(),
            }
        elif widget_type == 'campaign_stats':
            if user.is_superuser:
                campaigns = EmailCampaign.objects.all()
            else:
                company = getattr(user, 'profile', None)
                cn = company.company_name if company else ''
                campaigns = EmailCampaign.objects.filter(company_name=cn)
            data = {
                'total_campaigns': campaigns.count(),
                'total_sent': sum(c.sent_count for c in campaigns),
                'total_opens': sum(c.open_count for c in campaigns),
                'total_clicks': sum(c.click_count for c in campaigns),
                'recent': [
                    {'name': c.name, 'status': c.status, 'open_rate': c.open_rate}
                    for c in campaigns[:5]
                ]
            }
        elif widget_type == 'recent_deals':
            recent = deals.order_by('-created_at')[:5]
            data = [
                {
                    'id': d.id,
                    'title': d.title,
                    'value': float(d.value),
                    'stage': d.stage,
                    'created_at': str(d.created_at)
                }
                for d in recent
            ]
        elif widget_type == 'tasks_due':
            if user.is_superuser:
                all_tickets = Ticket.objects.filter(status__in=['open', 'in_progress'])
            else:
                all_tickets = Ticket.objects.filter(assigned_to=user, status__in=['open', 'in_progress'])
            due_today = all_tickets.filter(due_at__date=timezone.now().date())
            overdue = all_tickets.filter(due_at__lt=timezone.now())
            data = {
                'due_today': [
                    {'id': t.id, 'title': t.title, 'priority': t.priority}
                    for t in due_today[:5]
                ],
                'overdue': [
                    {'id': t.id, 'title': t.title, 'priority': t.priority}
                    for t in overdue[:5]
                ],
            }
        elif widget_type == 'team_leaderboard':
            if user.is_superuser:
                users = User.objects.filter(is_active=True)
            else:
                company = getattr(user, 'profile', None)
                cn = company.company_name if company else ''
                users = User.objects.filter(profile__company_name=cn, is_active=True)
            leaderboard = []
            for u in users[:10]:
                won = Deal.objects.filter(user=u, stage='closed_won')
                revenue = float(won.aggregate(t=Sum('value'))['t'] or 0)
                leaderboard.append({
                    'name': u.get_full_name() or u.username,
                    'deals_won': won.count(),
                    'revenue': revenue
                })
            leaderboard.sort(key=lambda x: x['revenue'], reverse=True)
            data = leaderboard

        return Response(data)


class DashboardLayoutViewSet(viewsets.ModelViewSet):
    serializer_class = DashboardLayoutSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return DashboardLayout.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


from .models import Organization, OrganizationSubscription, SubscriptionPlan, PaymentTransaction

class OrganizationBillingStatusView(APIView):
    """
    Get organization subscription and 14-day trial status.
    GET /api/billing/status/
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        profile = getattr(user, 'profile', None)
        org = getattr(profile, 'organization', None) if profile else None

        if not org:
            trial_days = getattr(profile, 'days_until_trial_end', 0) if profile else 0
            tier = (getattr(profile, 'tier', 'luxury') or 'luxury').lower()
            is_trial = trial_days > 0
            return Response({
                'organization_name': getattr(profile, 'company_name', 'Workspace'),
                'subscription_tier': 'basic' if tier == 'classic' else tier,
                'status': getattr(profile, 'payment_status', 'trial'),
                'is_trial_active': is_trial,
                'days_remaining': trial_days,
                'days_remaining_in_trial': trial_days,
                'days_remaining_in_grace': 3 if trial_days == 0 else 3,
                'is_in_grace_period': False,
                'is_grace_expired': False,
                'can_access': getattr(profile, 'can_access', True) if profile else True,
            })

        sub = getattr(org, 'subscription', None)
        status_val = sub.status if sub else org.subscription_tier
        is_paid = (status_val == 'active')
        is_trial = org.is_trial_active and not is_paid
        in_grace = org.is_in_grace_period and not is_paid
        grace_expired = org.is_grace_expired and not is_paid

        # Unrestricted during trial and grace period; locked after grace period expires without settlement
        can_access = is_paid or is_trial or in_grace or user.is_superuser

        current_tier = org.subscription_tier or 'luxury'
        if current_tier == 'classic':
            current_tier = 'basic'

        return Response({
            'organization_id': str(org.id),
            'organization_name': org.name,
            'subscription_tier': current_tier,
            'status': 'active' if is_paid else ('grace_period' if in_grace else ('trial' if is_trial else 'locked')),
            'is_trial_active': is_trial,
            'days_remaining_in_trial': org.days_remaining_in_trial,
            'trial_end_date': org.trial_end_date.isoformat() if org.trial_end_date else None,
            'is_in_grace_period': in_grace,
            'days_remaining_in_grace': org.days_remaining_in_grace,
            'grace_end_date': org.grace_end_date.isoformat() if org.grace_end_date else None,
            'is_grace_expired': grace_expired,
            'can_access': can_access,
            'plan': {
                'name': sub.plan.name if sub and sub.plan else f"Luxury {current_tier.title()}",
                'currency': sub.plan.currency if sub and sub.plan else 'ZAR',
                'price': (sub.plan.price_cents / 100) if sub and sub.plan else (349.0 if current_tier == 'basic' else 999.0),
            }
        })


class CreateCheckoutSessionView(APIView):
    """
    Generate payment checkout session or corporate invoice request.
    POST /api/billing/checkout/
    Body: {tier, gateway, billing_period}
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        profile = getattr(user, 'profile', None)
        org = getattr(profile, 'organization', None) if profile else None

        if not org:
            return Response({'error': 'Organization profile required for billing.'}, status=400)

        gateway = request.data.get('gateway', 'manual_eft')
        tier = (request.data.get('tier', 'luxury') or 'luxury').lower()
        if tier == 'classic':
            tier = 'basic'
        billing_period = request.data.get('billing_period', 'monthly')

        import uuid
        tx_ref = f"TFL-{org.slug[:6].upper()}-{uuid.uuid4().hex[:8].upper()}"

        pricing = {
            'basic': {'monthly': 34900, 'annual': 349000},          # R349/mo (R3,490/yr)
            'classic': {'monthly': 34900, 'annual': 349000},        # Backward compatibility
            'luxury': {'monthly': 99900, 'annual': 999000},          # R999/mo (R9,990/yr) Flagship
            'executive': {'monthly': 150000, 'annual': 1500000},     # R1,500/mo (R15,000/yr)
            'enterprise': {'monthly': 0, 'annual': 0}               # Bespoke Custom
        }
        amount_cents = pricing.get(tier, {}).get(billing_period, 99900)

        tx = PaymentTransaction.objects.create(
            organization=org,
            gateway=gateway,
            transaction_reference=tx_ref,
            amount_cents=amount_cents,
            currency='ZAR',
            status='pending',
            raw_payload={'initiated_by': user.email, 'tier': tier, 'period': billing_period}
        )

        return Response({
            'success': True,
            'transaction_reference': tx_ref,
            'amount_zar': amount_cents / 100,
            'currency': 'ZAR',
            'tier': tier,
            'gateway': gateway,
            'checkout_url': f"https://thefinishercrm.tech/billing/pay?ref={tx_ref}",
            'instructions': 'For direct corporate EFT payments, please use the transaction reference as beneficiary payment reference.'
        }, status=status.HTTP_201_CREATED)


class BillingWebhookView(APIView):
    """
    Payment Gateway Webhook Endpoint for PayFast / Peach / Ozow / Stripe / EFT.
    POST /api/billing/webhook/
    Automatically activates the chosen plan (Basic R349, Team R999, etc.) with 100% reliability.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        data = request.data
        tx_ref = data.get('m_payment_id') or data.get('transaction_reference')
        payment_status = data.get('payment_status', '').lower()

        if not tx_ref:
            return Response({'error': 'Missing transaction reference'}, status=400)

        try:
            tx = PaymentTransaction.objects.get(transaction_reference=tx_ref)
            if payment_status in ['complete', 'paid', 'successful']:
                tx.status = 'successful'
                existing_payload = tx.raw_payload or {}
                tx.raw_payload = {**existing_payload, **data}
                tx.save(update_fields=['status', 'raw_payload'])

                # Determine purchased plan tier
                chosen_tier = existing_payload.get('tier', 'luxury').lower()
                if chosen_tier == 'classic':
                    chosen_tier = 'basic'

                sub, _ = OrganizationSubscription.objects.get_or_create(organization=tx.organization)
                sub.status = 'active'
                sub.current_period_start = timezone.now()
                period_type = existing_payload.get('period', 'monthly')
                days_to_add = 365 if period_type == 'annual' else 30
                sub.current_period_end = timezone.now() + timedelta(days=days_to_add)
                sub.save()

                # Transition organization to paid status with chosen tier
                tx.organization.subscription_tier = chosen_tier
                tx.organization.is_active = True
                tx.organization.save(update_fields=['subscription_tier', 'is_active'])

                # Synchronize all profiles within organization to the activated plan
                UserProfile.objects.filter(organization=tx.organization).update(
                    tier=chosen_tier,
                    payment_status='paid'
                )

                # Record compliance audit trail (POPIA Section 19)
                record_audit_event(
                    'BILLING_TIER_ACTIVATED',
                    f"Commercial plan '{chosen_tier.upper()}' successfully unlocked for organization '{tx.organization.name}' following settlement (Ref: {tx_ref})",
                    user=None,
                    organization=tx.organization,
                    severity='INFO'
                )

                # Dispatch executive activation receipt email
                try:
                    from .email_service import send_email_async, render_luxury_email_html
                    admin_profiles = UserProfile.objects.filter(
                        organization=tx.organization,
                        role='admin'
                    ).select_related('user')
                    tier_display = "Luxury Basic (R349/mo)" if chosen_tier == "basic" else ("Luxury Team (R999/mo)" if chosen_tier == "luxury" else chosen_tier.title())
                    for ap in admin_profiles:
                        if ap.user and ap.user.email:
                            email_html = render_luxury_email_html(
                                title="Subscription Allocation Confirmed",
                                subtitle=f"{tx.organization.name} &middot; Account Unlocked",
                                recipient_name=ap.user.first_name or ap.user.username,
                                message_paragraphs=[
                                    f"Your commercial payment of <strong>R{tx.amount_cents / 100:.2f}</strong> has been successfully processed.",
                                    f"Your private workspace has been officially transitioned to <strong>{tier_display}</strong> with zero operational interruption.",
                                    "All client pipelines, contacts, deals, and team seats remain 100% intact."
                                ],
                                cta_text="Access Unlocked Workspace",
                                cta_url="https://www.thefinishercrm.tech/#/dashboard",
                                security_note="Mtambo Holdings Financial Directorate (mtamboholdings@outlook.com). In compliance with POPIA Section 19, your financial records are cryptographically secured."
                            )
                            send_email_async(
                                subject=f"Payment Verified — {tier_display} Activated for {tx.organization.name}",
                                text_body=f"Your {tier_display} plan has been successfully activated for {tx.organization.name}. Reference: {tx_ref}",
                                recipient_list=[ap.user.email],
                                html_body=email_html
                            )
                except Exception as mail_err:
                    import logging
                    logging.getLogger(__name__).error(f"Billing activation email error: {mail_err}")

            return Response({
                'status': 'acknowledged',
                'payment_status': tx.status,
                'tier_unlocked': chosen_tier if payment_status in ['complete', 'paid', 'successful'] else None
            })
        except PaymentTransaction.DoesNotExist:
            return Response({'error': 'Transaction not found'}, status=404)


class SecurityAuditTrailViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Enterprise Security Audit Trail ViewSet (POPIA Section 19 & ISO 27001).
    Restricted to Security Administrators and System Owners.
    """
    serializer_class = SecurityAuditTrailSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if not (user.is_superuser or is_owner_admin_user(user) or (getattr(user, 'profile', None) and user.profile.is_admin)):
            raise PermissionDenied("Access restricted to verified Security Administrators under POPIA regulations.")

        qs = SecurityAuditTrail.objects.select_related('user', 'organization').all()

        if not (user.is_superuser or is_owner_admin_user(user)):
            profile = getattr(user, 'profile', None)
            if profile and profile.organization:
                qs = qs.filter(organization=profile.organization)
            else:
                qs = qs.filter(user=user)

        event_type = self.request.query_params.get('event_type')
        if event_type:
            qs = qs.filter(event_type=event_type)

        severity = self.request.query_params.get('severity')
        if severity:
            qs = qs.filter(severity=severity.upper())

        company_name = self.request.query_params.get('company_name') or self.request.query_params.get('company')
        if company_name:
            qs = qs.filter(organization__name__icontains=company_name)

        search = self.request.query_params.get('search')
        if search:
            qs = qs.filter(
                Q(description__icontains=search) |
                Q(username_attempted__icontains=search) |
                Q(ip_address__icontains=search)
            )

        return qs[:250]

    @action(detail=False, methods=['get'], url_path='export-compliance-log')
    def export_compliance_log(self, request):
        """
        Export formal POPIA Compliance Audit Log CSV.
        """
        user = request.user
        if not (user.is_superuser or is_owner_admin_user(user)):
            raise PermissionDenied("Only System Owner can export POPIA compliance logs.")

        logs = self.get_queryset()

        import csv
        from django.http import HttpResponse
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="POPIA_Audit_Trail_{timezone.now().strftime("%Y%m%d_%H%M%S")}.csv"'

        writer = csv.writer(response)
        writer.writerow(['Audit ID', 'Timestamp (UTC)', 'Severity', 'Event Type', 'Actor', 'IP Address', 'User Agent', 'Description'])

        for log in logs:
            actor = log.user.username if log.user else (log.username_attempted or 'Anonymous')
            writer.writerow([
                str(log.id),
                log.timestamp.strftime('%Y-%m-%d %H:%M:%S UTC'),
                log.severity,
                log.event_type,
                actor,
                log.ip_address or 'N/A',
                (log.user_agent or 'N/A')[:100],
                log.description,
            ])

        # Record this export in the audit log itself (Non-repudiation!)
        record_audit_event(
            'DATA_EXPORT',
            f"POPIA Compliance Audit Log exported by {user.username} ({logs.count()} records)",
            user=user,
            request=request,
            severity='INFO',
            metadata={'export_type': 'POPIA_AUDIT_CSV', 'record_count': logs.count()}
        )

        return response


class TenantVerificationView(APIView):
    """
    Client Business Verification Endpoint.
    Allows corporate tenants to view verification status and submit CIPC compliance documents.
    """
    parser_classes = [MultiPartParser, FormParser, JSONParser]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        profile = getattr(user, 'profile', None)
        org = getattr(profile, 'organization', None) if profile else None
        
        # If user has no organization, fallback to creating or using their own
        if not org and profile:
            org_name = profile.company_name or f"{user.username.title()} Enterprise"
            org, _ = Organization.objects.get_or_create(
                name=org_name,
                defaults={'subscription_tier': 'luxury', 'is_active': True}
            )
            profile.organization = org
            profile.save(update_fields=['organization'])

        is_platform_owner = user.is_superuser or is_owner_admin_user(user)

        if not org:
            return Response({
                'has_submitted': False,
                'status': 'verified' if is_platform_owner else 'unverified',
                'is_verified': is_platform_owner,
                'organization_name': 'The Finisher Luxury Protocol' if is_platform_owner else 'Your Business',
                'verification': None
            })

        verification = getattr(org, 'verification', None)
        if not verification:
            return Response({
                'has_submitted': False,
                'status': 'verified' if (org.is_cipc_verified or is_platform_owner) else 'unverified',
                'is_verified': org.is_cipc_verified or is_platform_owner,
                'organization_name': org.name,
                'verification': None
            })

        return Response({
            'has_submitted': True,
            'status': verification.status,
            'is_verified': verification.status == 'verified' or org.is_cipc_verified or is_platform_owner,
            'organization_name': org.name,
            'verification': TenantVerificationSerializer(verification, context={'request': request}).data
        })

    def post(self, request):
        user = request.user
        profile = getattr(user, 'profile', None)
        org = getattr(profile, 'organization', None) if profile else None

        if not org and profile:
            org_name = (request.data.get('company_name') or profile.company_name or f"{user.username.title()} Enterprise").strip()
            org, _ = Organization.objects.get_or_create(
                name=org_name,
                defaults={'subscription_tier': 'luxury', 'is_active': True}
            )
            profile.organization = org
            profile.save(update_fields=['organization'])

        company_name = (request.data.get('company_name') or (org.name if org else '')).strip()
        trading_name = request.data.get('trading_name', '').strip()
        cipc_number = request.data.get('cipc_number', '').strip()
        tax_number = request.data.get('tax_number', '').strip()
        director_name = request.data.get('director_name', '').strip()

        if not company_name or not cipc_number:
            return Response({'error': 'Registered Company Name and CIPC Registration Number are mandatory.'}, status=status.HTTP_400_BAD_REQUEST)

        verification, created = TenantVerification.objects.get_or_create(
            organization=org,
            defaults={
                'submitted_by': user,
                'company_name': company_name,
                'trading_name': trading_name,
                'cipc_number': cipc_number,
                'tax_number': tax_number,
                'director_name': director_name,
                'status': 'pending'
            }
        )

        if not created:
            verification.submitted_by = user
            verification.company_name = company_name
            verification.trading_name = trading_name
            verification.cipc_number = cipc_number
            verification.tax_number = tax_number
            verification.director_name = director_name
            verification.status = 'pending'
            verification.rejection_reason = ''

        # Handle file uploads
        if 'cipc_certificate' in request.FILES:
            verification.cipc_certificate = request.FILES['cipc_certificate']
        if 'proof_of_address' in request.FILES:
            verification.proof_of_address = request.FILES['proof_of_address']
        if 'director_id_doc' in request.FILES:
            verification.director_id_doc = request.FILES['director_id_doc']

        verification.save()

        # Update organization name if updated
        if org and company_name and org.name != company_name:
            org.name = company_name
            org.save(update_fields=['name'])

        record_audit_event(
            'DATA_MODIFICATION',
            f"CIPC Business verification submitted for {company_name} (CIPC: {cipc_number}) by {user.username}",
            user=user,
            request=request,
            organization=org,
            severity='INFO',
            metadata={'cipc_number': cipc_number, 'status': 'pending'}
        )

        return Response({
            'message': 'Verification documents uploaded and queued for compliance review.',
            'verification': TenantVerificationSerializer(verification, context={'request': request}).data
        }, status=status.HTTP_200_OK)


class AdminTenantVerificationListView(APIView):
    """
    Compliance Console: Lists all tenant verification requests.
    Only accessible by SuperUser / Platform Executive.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        if not (user.is_superuser or is_owner_admin_user(user)):
            raise PermissionDenied("Only System Owner can view tenant verification records.")

        verifications = TenantVerification.objects.select_related('organization', 'submitted_by', 'reviewed_by').all()
        serializer = TenantVerificationSerializer(verifications, many=True, context={'request': request})
        return Response(serializer.data)


class AdminTenantVerificationReviewView(APIView):
    """
    Compliance Review: Approve or Reject a business verification.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        user = request.user
        if not (user.is_superuser or is_owner_admin_user(user)):
            raise PermissionDenied("Only System Owner can review tenant verifications.")

        try:
            verification = TenantVerification.objects.select_related('organization').get(pk=pk)
        except TenantVerification.DoesNotExist:
            return Response({'error': 'Verification record not found.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = TenantVerificationReviewSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        action = serializer.validated_data['action']
        internal_notes = serializer.validated_data.get('internal_notes', '')
        rejection_reason = serializer.validated_data.get('rejection_reason', '')

        if action == 'approve':
            verification.status = 'verified'
            verification.internal_notes = internal_notes
            verification.reviewed_by = user
            verification.reviewed_at = timezone.now()
            verification.save()

            # Unlock organization
            org = verification.organization
            org.is_cipc_verified = True
            org.is_active = True
            org.save(update_fields=['is_cipc_verified', 'is_active'])

            record_audit_event(
                'COMPLIANCE_APPROVED',
                f"Business entity {verification.company_name} (CIPC: {verification.cipc_number}) APPROVED by {user.username}. Workspace unlocked.",
                user=user,
                request=request,
                organization=org,
                severity='SECURITY',
                metadata={'cipc_number': verification.cipc_number, 'approved_by': user.username}
            )

            return Response({
                'message': f"Entity {verification.company_name} verified and approved. Workspace unlocked.",
                'verification': TenantVerificationSerializer(verification, context={'request': request}).data
            })

        else: # reject
            verification.status = 'rejected'
            verification.internal_notes = internal_notes
            verification.rejection_reason = rejection_reason or 'Documentation failed verification checks against CIPC registry.'
            verification.reviewed_by = user
            verification.reviewed_at = timezone.now()
            verification.save()

            # Organization remains locked
            org = verification.organization
            org.is_cipc_verified = False
            org.save(update_fields=['is_cipc_verified'])

            record_audit_event(
                'COMPLIANCE_REJECTED',
                f"Business entity {verification.company_name} (CIPC: {verification.cipc_number}) REJECTED by {user.username}. Reason: {verification.rejection_reason}",
                user=user,
                request=request,
                organization=org,
                severity='WARNING',
                metadata={'cipc_number': verification.cipc_number, 'rejected_by': user.username}
            )

            return Response({
                'message': f"Entity {verification.company_name} rejected. Tenant notified.",
                'verification': TenantVerificationSerializer(verification, context={'request': request}).data
            })


class PrivateSalesLedgerView(APIView):
    """
    Exclusive Root CEO Sales & Revenue Ledger (POPIA & Financial Governance).
    Strictly accessible by root Platform Owner / Superuser (adminluxury).
    Allows manual recording of offline contracts, tracking MRR/ARR, monitoring 7-day trials,
    and 1-click subscription management.
    """
    permission_classes = [IsAuthenticated]

    def _check_owner(self, user):
        return user.is_superuser or is_owner_admin_user(user)

    def get(self, request):
        if not self._check_owner(request.user):
            return Response({'error': 'Unauthorized. Private Executive Deck access only.'}, status=403)

        from .models import Organization, OrganizationSubscription, UserProfile
        orgs = Organization.objects.all().order_by('-created_at')
        records = []
        total_mrr = 0
        active_trials_count = 0
        paid_clients_count = 0

        for org in orgs:
            sub = getattr(org, 'subscription', None)
            tier = org.subscription_tier or 'luxury'
            status_val = sub.status if sub else ('trial' if tier == 'trial' else 'active')
            monthly_rate = float(getattr(sub, 'monthly_price', 0) or 0)
            if not monthly_rate:
                tier_rates = {'basic': 349.00, 'luxury': 999.00, 'trial': 999.00, 'executive': 1500.00, 'enterprise': 0.00}
                monthly_rate = tier_rates.get(tier.lower(), 999.00)

            if status_val == 'active':
                paid_clients_count += 1
                total_mrr += monthly_rate
            elif status_val == 'trial':
                active_trials_count += 1

            # User count
            user_count = User.objects.filter(profile__organization=org, is_superuser=False).count()

            # Trial days remaining
            days_left = None
            if org.trial_end_date:
                diff = org.trial_end_date - timezone.now()
                days_left = max(0, diff.days)
            elif sub and sub.current_period_end:
                diff = sub.current_period_end - timezone.now()
                days_left = max(0, diff.days)

            # CEO / Admin contact
            ceo_profile = UserProfile.objects.filter(organization=org, role='admin').first() or UserProfile.objects.filter(organization=org).first()
            admin_email = ceo_profile.user.email if (ceo_profile and ceo_profile.user) else ''

            tier_display_map = {
                'basic': 'Luxury Basic (R349/mo)',
                'luxury': 'Luxury Team (R999/mo)',
                'executive': 'Executive Suite (R1,500/mo)',
                'enterprise': 'Enterprise Custom',
                'trial': '7-Day VIP Trial'
            }

            records.append({
                'id': str(org.id),
                'company_name': org.name,
                'slug': org.slug,
                'tier': tier,
                'tier_display': tier_display_map.get(tier.lower(), tier.title()),
                'max_users': org.max_users,
                'current_users': user_count,
                'status': status_val,
                'monthly_price': monthly_rate,
                'payment_method': getattr(sub, 'payment_method', 'payfast') or 'payfast',
                'payment_reference': getattr(sub, 'payment_reference', '') or '',
                'notes': getattr(sub, 'notes', '') or '',
                'trial_start': org.trial_start_date.isoformat() if org.trial_start_date else None,
                'trial_end': org.trial_end_date.isoformat() if org.trial_end_date else None,
                'days_remaining': days_left,
                'admin_email': admin_email,
                'created_at': org.created_at.isoformat() if org.created_at else None,
            })

        return Response({
            'metrics': {
                'total_mrr': total_mrr,
                'total_arr': total_mrr * 12,
                'total_clients': len(records),
                'active_trials': active_trials_count,
                'paid_clients': paid_clients_count,
                'currency': 'ZAR'
            },
            'ledger': records
        })

    def post(self, request):
        if not self._check_owner(request.user):
            return Response({'error': 'Unauthorized. Private Executive Deck access only.'}, status=403)

        from .models import Organization, OrganizationSubscription
        data = request.data
        company_name = (data.get('company_name') or '').strip()
        tier = (data.get('tier') or 'luxury').lower().strip()
        monthly_price = data.get('monthly_price')
        payment_method = (data.get('payment_method') or 'capitec').strip()
        payment_reference = (data.get('payment_reference') or '').strip()
        status_val = (data.get('status') or 'trial').strip()
        notes = (data.get('notes') or '').strip()

        if not company_name:
            return Response({'error': 'Company name is required.'}, status=400)

        tier_seats = {'basic': 1, 'luxury': 5, 'trial': 5, 'executive': 15, 'enterprise': 999}
        max_seats = tier_seats.get(tier, 5)

        if not monthly_price:
            tier_rates = {'basic': 349.00, 'luxury': 999.00, 'trial': 999.00, 'executive': 1500.00, 'enterprise': 0.00}
            monthly_price = tier_rates.get(tier, 999.00)

        org, created = Organization.objects.get_or_create(
            name=company_name,
            defaults={
                'subscription_tier': tier,
                'max_users': max_seats,
                'is_active': True,
                'trial_start_date': timezone.now(),
                'trial_end_date': timezone.now() + timezone.timedelta(days=7),
            }
        )
        if not created:
            org.subscription_tier = tier
            org.max_users = max_seats
            org.is_active = True
            org.save(update_fields=['subscription_tier', 'max_users', 'is_active'])

        sub, _ = OrganizationSubscription.objects.get_or_create(organization=org)
        sub.status = status_val
        sub.monthly_price = float(monthly_price)
        sub.payment_method = payment_method
        sub.payment_reference = payment_reference
        sub.notes = notes
        if status_val == 'active':
            sub.current_period_start = timezone.now()
            sub.current_period_end = timezone.now() + timezone.timedelta(days=30)
        else:
            sub.current_period_start = timezone.now()
            sub.current_period_end = timezone.now() + timezone.timedelta(days=7)
        sub.save()

        return Response({
            'message': f"Sales record saved for {company_name} ({tier.title()} • R{monthly_price}/mo).",
            'org_id': str(org.id),
            'status': sub.status
        }, status=201)

    def patch(self, request):
        if not self._check_owner(request.user):
            return Response({'error': 'Unauthorized. Private Executive Deck access only.'}, status=403)

        from .models import Organization, OrganizationSubscription
        data = request.data
        org_id = data.get('org_id')
        if not org_id:
            return Response({'error': 'org_id is required.'}, status=400)

        org = Organization.objects.filter(id=org_id).first()
        if not org:
            return Response({'error': 'Organization not found.'}, status=404)

        sub, _ = OrganizationSubscription.objects.get_or_create(organization=org)
        if 'status' in data:
            sub.status = data['status']
            if data['status'] == 'active':
                sub.current_period_start = timezone.now()
                sub.current_period_end = timezone.now() + timezone.timedelta(days=30)
                org.is_active = True
        if 'tier' in data:
            new_tier = data['tier'].lower().strip()
            org.subscription_tier = new_tier
            tier_seats = {'basic': 1, 'luxury': 5, 'trial': 5, 'executive': 15, 'enterprise': 999}
            org.max_users = tier_seats.get(new_tier, 5)
            org.save(update_fields=['subscription_tier', 'max_users'])
        if 'monthly_price' in data:
            sub.monthly_price = float(data['monthly_price'])
        if 'payment_reference' in data:
            sub.payment_reference = data['payment_reference']
        if 'notes' in data:
            sub.notes = data['notes']
        if data.get('extend_days'):
            days = int(data['extend_days'])
            org.trial_end_date = (org.trial_end_date or timezone.now()) + timezone.timedelta(days=days)
            org.save(update_fields=['trial_end_date'])
            sub.current_period_end = (sub.current_period_end or timezone.now()) + timezone.timedelta(days=days)

        sub.save()
        org.save()

        return Response({
            'message': f"Updated sales ledger record for {org.name}.",
            'status': sub.status,
            'tier': org.subscription_tier
        })


class SubmitBugQueryView(APIView):
    """
    Public / Authenticated query & bug reporting endpoint.
    POST /api/public/submit-query/
    Dispatches directly to mtamboholdings@outlook.com and logs a high-priority notification.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        data = request.data or {}
        subject = (data.get('subject') or 'Enterprise CRM Query / Bug Report').strip()
        category = data.get('category', 'bug_report')
        message = (data.get('message') or '').strip()
        sender_email = (data.get('email') or (request.user.email if request.user.is_authenticated else '')).strip()
        sender_name = (data.get('name') or (request.user.get_full_name() if request.user.is_authenticated else 'Client Operator')).strip()
        company = (data.get('company') or (getattr(getattr(request.user, 'profile', None), 'company_name', '') if request.user.is_authenticated else '')).strip()

        if not message:
            return Response({'error': 'Message content is required.'}, status=400)

        from .email_service import send_email_async, render_luxury_email_html
        admin_email = 'mtamboholdings@outlook.com'

        email_html = render_luxury_email_html(
            title="Executive Support & Bug Notification",
            subtitle="Platform Inbound Query Dispatch",
            recipient_name="Executive Directorate",
            message_paragraphs=[
                "An urgent client query / bug report has been submitted from the platform.",
                f"<strong>Sender:</strong> {sender_name} ({sender_email or 'Anonymous'}) &middot; <strong>Company:</strong> {company or 'Unspecified'}",
                f"<strong>Category:</strong> {category.upper()}",
                f"<strong>Message:</strong><br/>{message}"
            ],
            security_note="Direct dispatch to Mtambo Holdings Engineering & Executive Concierge (7682 Isikova Crescent, Gauteng, Boksburg, 1459)."
        )

        send_email_async(
            subject=f"🚨 [{category.upper()}] {subject} — from {company or sender_name}",
            text_body=f"Query from {sender_name} ({sender_email}):\n\n{message}",
            recipient_list=[admin_email],
            html_body=email_html
        )

        return Response({
            'success': True,
            'message': 'Your query has been dispatched directly to the executive technical concierge. We will review and respond promptly.'
        }, status=200)


class AdminTenantInspectorView(APIView):
    """
    Master Admin Control Deck: Tenant Activity & Client Inspector.
    Exclusively accessible to Platform Owner / Superuser (is_owner_admin_user or is_superuser).
    Provides deep multi-tenant inspection of any client business workspace:
    - Business details, CEO name, subscription plan, CIPC status.
    - Full list of client contacts for that tenant (name, email, phone, company, created_at).
    - Deals & Commercial Pipeline for that tenant.
    - User / Employee Team Roster.
    - Chronological Activity Timeline ('Tebogo added user Sipho', 'Tebogo created contact Acme', 'Monde updated Deal Alpha').
    """
    permission_classes = [IsAuthenticated]

    def check_owner(self, request):
        if not (request.user.is_superuser or is_owner_admin_user(request.user)):
            raise PermissionDenied("Access restricted to Platform Owner / System Administrator.")

    def get(self, request):
        self.check_owner(request)
        tenant_id = request.query_params.get('tenant_id') or request.query_params.get('org_id')

        # 1. If no specific tenant requested, return list of all client businesses / workspaces
        if not tenant_id:
            orgs = Organization.objects.all().order_by('-created_at')
            tenants_data = []
            for org in orgs:
                owner = org.owner
                contact_count = Contact.objects.filter(organization=org, website_lead__isnull=True).count()
                deal_count = Deal.objects.filter(organization=org).count()
                user_count = UserProfile.objects.filter(organization=org).count()
                
                last_act = ActivityLog.objects.filter(
                    Q(user__profile__organization=org) | Q(user=owner)
                ).order_by('-created_at').first()

                last_action_desc = "No activity logged yet"
                if last_act:
                    actor_name = last_act.user.get_full_name() or last_act.user.username
                    last_action_desc = f"{actor_name} {last_act.get_action_display().lower()} {last_act.entity_type} '{last_act.entity_name}'"

                tenants_data.append({
                    'id': org.id,
                    'name': org.name,
                    'slug': org.slug,
                    'owner_username': owner.username if owner else 'unassigned',
                    'owner_full_name': (owner.get_full_name() or owner.username) if owner else 'Unassigned',
                    'owner_email': owner.email if owner else '',
                    'subscription_tier': org.subscription_tier,
                    'is_active': org.is_active,
                    'created_at': org.created_at,
                    'contact_count': contact_count,
                    'deal_count': deal_count,
                    'user_count': user_count,
                    'last_action': last_action_desc,
                    'last_action_at': last_act.created_at if last_act else None,
                })
            return Response({'tenants': tenants_data})

        # 2. Return deep inspection details for the requested tenant
        try:
            org = Organization.objects.get(id=tenant_id)
        except (Organization.DoesNotExist, ValueError):
            return Response({'error': 'Tenant organization not found'}, status=status.HTTP_404_NOT_FOUND)

        owner = org.owner

        # Contacts list
        contacts = Contact.objects.filter(organization=org, website_lead__isnull=True).order_by('-created_at')[:200]
        contacts_data = [{
            'id': c.id,
            'name': f"{c.first_name} {c.last_name}".strip(),
            'first_name': c.first_name,
            'last_name': c.last_name,
            'email': c.email,
            'phone': c.phone,
            'company_name': c.company_name_manual or (c.company.name if c.company else ''),
            'created_at': c.created_at
        } for c in contacts]

        # Deals list
        deals = Deal.objects.filter(organization=org).order_by('-created_at')[:100]
        deals_data = [{
            'id': d.id,
            'title': d.title,
            'value': float(d.value or 0),
            'stage': d.stage,
            'contact_name': f"{d.contact.first_name} {d.contact.last_name}" if d.contact else 'N/A',
            'created_at': d.created_at
        } for d in deals]

        # Users / Team Roster
        team = UserProfile.objects.filter(organization=org).select_related('user')
        team_data = [{
            'id': p.user.id,
            'username': p.user.username,
            'full_name': p.user.get_full_name() or p.user.username,
            'email': p.user.email,
            'role': p.role,
            'job_title': p.job_title,
            'can_manage_assets': p.has_asset_permission,
            'is_active': p.user.is_active,
            'date_joined': p.user.date_joined
        } for p in team]

        # Chronological Activity Timeline ('Tebogo added a user', 'Tebogo created contact Acme'...)
        activities = ActivityLog.objects.filter(
            Q(user__profile__organization=org) | Q(user=owner)
        ).select_related('user').order_by('-created_at')[:100]
        
        timeline_data = [{
            'id': a.id,
            'actor_username': a.user.username,
            'actor_name': a.user.get_full_name() or a.user.username,
            'action': a.action,
            'action_display': a.get_action_display(),
            'entity_type': a.entity_type,
            'entity_name': a.entity_name,
            'details': a.details,
            'created_at': a.created_at,
            'narrative': f"{a.user.get_full_name() or a.user.username} {a.get_action_display().lower()} {a.entity_type} '{a.entity_name}'"
        } for a in activities]

        return Response({
            'tenant': {
                'id': org.id,
                'name': org.name,
                'slug': org.slug,
                'owner_name': (owner.get_full_name() or owner.username) if owner else 'Unassigned',
                'owner_email': owner.email if owner else '',
                'subscription_tier': org.subscription_tier,
                'is_active': org.is_active,
                'created_at': org.created_at,
                'contact_count': len(contacts_data),
                'deal_count': len(deals_data),
                'user_count': len(team_data)
            },
            'contacts': contacts_data,
            'deals': deals_data,
            'team': team_data,
            'timeline': timeline_data
        })


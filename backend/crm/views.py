from rest_framework import viewsets, status
from rest_framework.decorators import api_view, action, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.parsers import MultiPartParser, FormParser
from django.db import IntegrityError, transaction
from django.db.models import Q, Count, Sum
from django.contrib.auth.models import User
from django.utils import timezone
import csv
import io
from .models import Contact, Company, Deal, ActivityLog, UserProfile, DeletedUserLog, Ticket, Notification, Asset, AssetCategory, Division, OnboardingLog, OffboardingRequest, Product, LineItem, EmailTemplate, EmailCampaign, CampaignRecipient, Workflow, WorkflowAction, WorkflowLog, DashboardWidget, DashboardLayout
from .utils import is_owner_admin_user, normalize_company_name
from .serializers import (
    ContactSerializer, 
    CompanySerializer, 
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
    LineItemSerializer,
    EmailTemplateSerializer,
    EmailCampaignSerializer,
    CampaignRecipientSerializer,
    WorkflowSerializer,
    WorkflowActionSerializer,
    WorkflowLogSerializer,
    DashboardWidgetSerializer,
    DashboardLayoutSerializer,
)
from .tier_limits import LUXURY_TIER_LIMITS

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

    company = Company.objects.filter(user=contact.user, name__iexact=company_name).first()
    if not company:

        company = Company.objects.create(user=contact.user, name=company_name)
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

    if updated_fields:
        company.save(update_fields=updated_fields)

    if contact.company_id != company.id:
        contact.company = company
        contact.save(update_fields=['company'])


class ContactViewSet(viewsets.ModelViewSet):
    """
    Contact viewset with user isolation.
    System admins see all contacts; client admins see company contacts.
    """
    serializer_class = ContactSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        if user.is_superuser or user.is_staff:
            return Contact.objects.all()

        profile = getattr(user, 'profile', None)
        if profile and profile.is_admin and profile.company_name:
            company = normalize_company_name(profile.company_name)
            return Contact.objects.filter(
                user__profile__company_name__iexact=company
            )

        return Contact.objects.filter(user=user)

    def perform_create(self, serializer):

        user = self.request.user
        if not (user.is_superuser or user.is_staff or (getattr(user, 'profile', None) and user.profile.is_admin)):
            raise PermissionDenied('Only administrators can create contacts.')

        contact = serializer.save(user=user)
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

        if user.is_superuser or user.is_staff:
            return Company.objects.all()

        profile = getattr(user, 'profile', None)
        if profile and profile.is_admin and profile.company_name:
            company = normalize_company_name(profile.company_name)
            return Company.objects.filter(
                user__profile__company_name__iexact=company
            )
        return Company.objects.filter(user=user)

    def perform_create(self, serializer):

        user = self.request.user
        if not (user.is_superuser or user.is_staff or (getattr(user, 'profile', None) and user.profile.is_admin)):
            raise PermissionDenied('Only administrators can create companies.')

        if not Contact.objects.filter(user=user).exists():
            raise ValidationError({
                'error': 'You need at least one contact before you can register a company.',
                'action': 'Capture a contact with their company name, then create the company profile.'
            })
        company = serializer.save(user=user)
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
    Deal viewset with user isolation.
    """
    serializer_class = DealSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        if user.is_superuser or user.is_staff:
            return Deal.objects.all()

        profile = getattr(user, 'profile', None)
        if profile and profile.is_admin and profile.company_name:
            company = normalize_company_name(profile.company_name)
            return Deal.objects.filter(
                user__profile__company_name__iexact=company
            )
        return Deal.objects.filter(user=user)

    def perform_create(self, serializer):

        user = self.request.user
        if not (user.is_superuser or user.is_staff or (getattr(user, 'profile', None) and user.profile.is_admin)):
            raise PermissionDenied('Only administrators can create deals.')
        deal = serializer.save(user=user)
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

        return ActivityLog.objects.filter(user=self.request.user)


class TicketViewSet(viewsets.ModelViewSet):
    serializer_class = TicketSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser or user.is_staff:
            return Ticket.objects.all()
        
        profile = getattr(user, 'profile', None)
        if profile and profile.is_admin:

            company_name = profile.company_name
            if company_name:
                return Ticket.objects.filter(
                    Q(created_by__profile__company_name=company_name) |
                    Q(assigned_to__profile__company_name=company_name)
                ).distinct()
            else:

                return Ticket.objects.filter(
                    Q(created_by=user) | Q(assigned_to=user)
                )
        else:

            return Ticket.objects.filter(Q(assigned_to=user) | Q(created_by=user)).distinct()

    def perform_create(self, serializer):
        user = self.request.user
        profile = getattr(user, 'profile', None)

        if not (user.is_superuser or user.is_staff or (profile and profile.is_admin)):
            assigned_to = serializer.validated_data.get('assigned_to')
            assigned_profile = getattr(assigned_to, 'profile', None)
            if not assigned_profile or assigned_profile.role != 'admin':
                raise PermissionDenied('You can only escalate tickets to your company administrator.')

            if profile and assigned_profile and profile.company_name != assigned_profile.company_name:
                raise PermissionDenied('You can only assign within your company.')
        ticket = serializer.save(created_by=user)

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
        serializer.save()

    def perform_destroy(self, instance):
        user = self.request.user
        if not (user.is_superuser or user.is_staff or getattr(user, 'profile', None) and user.profile.is_admin):
            raise PermissionDenied('Only administrators can delete tickets.')
        instance.delete()

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
        admin_users = User.objects.filter(companies__isnull=False).distinct()
        for user in admin_users:
            companies = []
            for company in user.companies.all().order_by('name'):
                contacts_qs = company.contact_set.filter(user=user).order_by('first_name', 'last_name')
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
                'total_contacts': Contact.objects.filter(user=user).count(),
                'total_deals': Deal.objects.filter(user=user).count(),
            })

        analytics = Deal.objects.aggregate(
            total_deals=Count('id'),
            active_deals=Count('id', filter=Q(stage__in=['lead', 'qualified', 'proposal', 'negotiation'])),
            closed_won=Count('id', filter=Q(stage='closed_won')),
            pipeline_value=Sum('value', filter=Q(stage__in=['lead', 'qualified', 'proposal', 'negotiation'])),
            won_value=Sum('value', filter=Q(stage='closed_won')),
        )

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
            },
            'support_catalog': support_catalog
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
        
        users = User.objects.all().select_related('profile').order_by('-date_joined')
        
        user_list = []
        for user in users:
            profile = user.profile if hasattr(user, 'profile') else None

            contact_count = Contact.objects.filter(user=user).count()
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

                contact_count = Contact.objects.filter(user=user).count()
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

        client_user_count = User.objects.filter(
            is_superuser=False,
            is_staff=False,
            profile__company_name__iexact=company_name
        ).count()
        max_users = int(LUXURY_TIER_LIMITS.get('max_users', 50))
        
        if client_user_count >= max_users:
            return Response({
                'error': f'User limit reached ({client_user_count}/{max_users}). Upgrade to add more employees.',
                'current_users': client_user_count,
                'max_users': max_users,
                'upgrade_required': True
            }, status=400)

        import random
        import string
        from django.core.mail import send_mail

        create_serializer = EmployeeCreateSerializer(data=request.data)
        create_serializer.is_valid(raise_exception=True)
        user_data = create_serializer.validated_data
        assigned_role = user_data.get('role')

        raw_password = user_data.get('password')
        if not raw_password:
            raw_password = ''.join(random.choices(string.ascii_letters + string.digits + '!@#$%', k=12))

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


        if user.check_password(user_data['password']):
            return Response({
                'error': 'Security: Employee password cannot be the same as your password. Please use a unique password.'
            }, status=400)


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
                    send_mail(
                        subject='Welcome to THE FINISHER CRM - Your Account Details',
                        message=f'''Hello {new_user.first_name},

You have been invited to THE FINISHER LUXURY CRM by {user.get_full_name() or user.username}.

Your login details are as follows:
Username / Email: {email_identity}
Temporary Password: {raw_password}

You will be required to change your password and verify your identity via OTP upon your first login.

Best regards,
THE FINISHER Team''',
                        from_email='thefinishercrm@gmail.com',
                        recipient_list=[email_identity],
                        fail_silently=False,
                    )
                except Exception as e:
                    import logging
                    logger = logging.getLogger(__name__)
                    logger.error(f"Failed to send onboarding email to {email_identity}: {e}")

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
        """Get remaining employee slots based on tier (excluding system admins), scoped per company"""
        user = request.user

        if user.is_superuser or user.is_staff:
            return Response({
                'remaining_slots': None,
                'current_users': User.objects.filter(is_superuser=False, is_staff=False).count(),
                'max_users': int(LUXURY_TIER_LIMITS.get('max_users', 50)),
                'can_add_more': False
            })

        profile = getattr(user, 'profile', None)
        company_name = normalize_company_name((profile.company_name if profile else '') or '')

        client_user_count = User.objects.filter(
            is_superuser=False,
            is_staff=False,
            profile__company_name__iexact=company_name
        ).count()
        max_users = int(LUXURY_TIER_LIMITS.get('max_users', 50))
        remaining = max(0, max_users - client_user_count)
        
        
        return Response({
            'remaining_slots': remaining,
            'current_users': client_user_count,
            'max_users': max_users,
            'can_add_more': remaining > 0
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

        client_users = User.objects.filter(
            is_superuser=False,
            is_staff=False
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

            contact_count = Contact.objects.filter(user=user).count()
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

        if user.is_superuser or user.is_staff:
            return Asset.objects.all().select_related('category', 'assigned_to', 'division', 'created_by')
        
        profile = getattr(user, 'profile', None)
        if not profile or not profile.company_name:
            return Asset.objects.none()
        
        company_name = normalize_company_name(profile.company_name)

        if profile.role in ['admin', 'manager']:
            return Asset.objects.filter(company_name__iexact=company_name).select_related(
                'category', 'assigned_to', 'division', 'created_by'
            )

        return Asset.objects.filter(
            company_name__iexact=company_name,
            assigned_to=user
        ).select_related('category', 'assigned_to', 'division', 'created_by')
    
    def perform_create(self, serializer):
        """
        Create assets - restricted to superuser, admin (CEO), and managers only.
        Regular employees cannot create assets.
        """
        user = self.request.user
        profile = getattr(user, 'profile', None)

        if not (user.is_superuser or user.is_staff):
            if not profile or profile.role not in ['admin', 'manager']:
                raise PermissionDenied('Only administrators and managers can create assets')
        
        if user.is_superuser or user.is_staff:
            serializer.save(created_by=user)
        elif profile and profile.company_name:
            company_name = normalize_company_name(profile.company_name)
            serializer.save(company_name=company_name, created_by=user)
        else:
            raise ValidationError("User has no company association")
    
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
        if user.is_superuser:
            return Product.objects.all()
        company = getattr(user, 'profile', None)
        company_name = company.company_name if company else ''
        return Product.objects.filter(company_name=company_name)

    def perform_create(self, serializer):
        user = self.request.user
        if user.is_superuser:
            company_name = 'MTAMBO HOLDINGS'
        else:
            company = getattr(user, 'profile', None)
            company_name = company.company_name if company else ''
        serializer.save(created_by=user, company_name=company_name)


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
        if user.is_superuser:
            return EmailTemplate.objects.all()
        company = getattr(user, 'profile', None)
        company_name = company.company_name if company else ''
        return EmailTemplate.objects.filter(company_name=company_name)

    def perform_create(self, serializer):
        company = getattr(self.request.user, 'profile', None)
        company_name = company.company_name if company else ''
        serializer.save(created_by=self.request.user, company_name=company_name)


class EmailCampaignViewSet(viewsets.ModelViewSet):
    serializer_class = EmailCampaignSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return EmailCampaign.objects.all()
        company = getattr(user, 'profile', None)
        company_name = company.company_name if company else ''
        return EmailCampaign.objects.filter(company_name=company_name)

    def perform_create(self, serializer):
        company = getattr(self.request.user, 'profile', None)
        company_name = company.company_name if company else ''
        serializer.save(created_by=self.request.user, company_name=company_name)

    @action(detail=True, methods=['post'])
    def send(self, request, pk=None):
        """Send the campaign to all recipients."""
        campaign = self.get_object()
        if campaign.status == 'sent':
            return Response({'error': 'Campaign already sent'}, status=400)

        contact_ids = campaign.recipient_ids or []
        if not contact_ids:

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
            if not recipient.opened_at:
                recipient.status = 'opened'
                recipient.opened_at = timezone.now()
                recipient.save()
                campaign.open_count += 1
                campaign.save()
        except CampaignRecipient.DoesNotExist:
            pass
        return Response({'status': 'tracked'})

    @action(detail=True, methods=['post'], url_path='track-click')
    def track_click(self, request, pk=None):
        """Track a link click for a contact."""
        campaign = self.get_object()
        contact_id = request.data.get('contact_id')
        try:
            recipient = CampaignRecipient.objects.get(campaign=campaign, contact_id=contact_id)
            if not recipient.clicked_at:
                recipient.status = 'clicked'
                recipient.clicked_at = timezone.now()
                recipient.save()
                campaign.click_count += 1
                campaign.save()
        except CampaignRecipient.DoesNotExist:
            pass
        return Response({'status': 'tracked'})




class WorkflowViewSet(viewsets.ModelViewSet):
    serializer_class = WorkflowSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return Workflow.objects.prefetch_related('actions').all()
        company = getattr(user, 'profile', None)
        company_name = company.company_name if company else ''
        return Workflow.objects.filter(company_name=company_name).prefetch_related('actions')

    def perform_create(self, serializer):
        company = getattr(self.request.user, 'profile', None)
        company_name = company.company_name if company else ''

        if not self.request.user.is_superuser:
            count = Workflow.objects.filter(company_name=company_name).count()
            if count >= 5:
                raise ValidationError({'detail': 'LUXURY tier allows a maximum of 5 workflows. Upgrade to PREMIUM for unlimited.'})
        serializer.save(created_by=self.request.user, company_name=company_name)

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
            {'widget_type': 'stat_card', 'title': 'Total Contacts', 'position_x': 0, 'position_y': 0, 'width': 1, 'height': 1},
            {'widget_type': 'stat_card', 'title': 'Total Deals', 'position_x': 1, 'position_y': 0, 'width': 1, 'height': 1},
            {'widget_type': 'stat_card', 'title': 'Revenue', 'position_x': 2, 'position_y': 0, 'width': 1, 'height': 1},
            {'widget_type': 'pipeline_chart', 'title': 'Pipeline', 'position_x': 0, 'position_y': 1, 'width': 2, 'height': 1},
            {'widget_type': 'activity_feed', 'title': 'Activity Feed', 'position_x': 2, 'position_y': 1, 'width': 1, 'height': 1},
            {'widget_type': 'deal_funnel', 'title': 'Deal Funnel', 'position_x': 0, 'position_y': 2, 'width': 2, 'height': 1},
            {'widget_type': 'recent_deals', 'title': 'Recent Deals', 'position_x': 2, 'position_y': 2, 'width': 1, 'height': 1},
        ]
        widgets = []
        for d in defaults:
            widgets.append(DashboardWidget.objects.create(user=request.user, **d))
        return Response(DashboardWidgetSerializer(widgets, many=True).data)

    @action(detail=False, methods=['get'], url_path='widget-data/(?P<widget_type>[a-z_]+)')
    def widget_data(self, request, widget_type=None):
        """Return live data for a specific widget type."""
        user = request.user
        data = {}

        if user.is_superuser:
            contacts = Contact.objects.all()
            deals = Deal.objects.all()
            companies = Company.objects.all()
        else:
            contacts = Contact.objects.filter(user=user)
            deals = Deal.objects.filter(user=user)
            companies = Company.objects.filter(user=user)

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
            stages = ['lead', 'qualified', 'proposal', 'negotiation', 'closed_won', 'closed_lost']
            data = {stage: deals.filter(stage=stage).count() for stage in stages}
        elif widget_type == 'revenue_chart':
            from django.db.models.functions import TruncMonth
            monthly = deals.filter(stage='closed_won').annotate(
                month=TruncMonth('created_at')
            ).values('month').annotate(
                total=Sum('value'), count=Count('id')
            ).order_by('month')[:12]
            data = [{'month': str(m['month'].strftime('%Y-%m') if m['month'] else ''), 'total': float(m['total']), 'count': m['count']} for m in monthly]
        elif widget_type == 'deal_funnel':
            stages = ['lead', 'qualified', 'proposal', 'negotiation', 'closed_won']
            data = [{'stage': s, 'count': deals.filter(stage=s).count(),
                     'value': float(deals.filter(stage=s).aggregate(v=Sum('value'))['v'] or 0)} for s in stages]
        elif widget_type == 'activity_feed':
            if user.is_superuser:
                activities = ActivityLog.objects.all()[:10]
            else:
                activities = ActivityLog.objects.filter(user=user)[:10]
            data = [{'action': a.action, 'entity_type': a.entity_type,
                     'entity_name': a.entity_name, 'created_at': str(a.created_at)} for a in activities]
        elif widget_type == 'top_contacts':
            top = contacts.order_by('-last_contact_date')[:5]
            data = [{'id': c.id, 'name': f"{c.first_name} {c.last_name}",
                     'email': c.email, 'health_score': c.health_score} for c in top]
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
                'recent': [{'name': c.name, 'status': c.status, 'open_rate': c.open_rate} for c in campaigns[:5]]
            }
        elif widget_type == 'recent_deals':
            recent = deals.order_by('-created_at')[:5]
            data = [{'id': d.id, 'title': d.title, 'value': float(d.value),
                     'stage': d.stage, 'created_at': str(d.created_at)} for d in recent]
        elif widget_type == 'tasks_due':
            if user.is_superuser:
                tickets = Ticket.objects.filter(status__in=['open', 'in_progress'])
            else:
                tickets = Ticket.objects.filter(assigned_to=user, status__in=['open', 'in_progress'])
            due_today = tickets.filter(due_at__date=timezone.now().date())
            overdue = tickets.filter(due_at__lt=timezone.now())
            data = {
                'due_today': [{'id': t.id, 'title': t.title, 'priority': t.priority} for t in due_today[:5]],
                'overdue': [{'id': t.id, 'title': t.title, 'priority': t.priority} for t in overdue[:5]],
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

import logging
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import CorporateAccessRequest, Organization, UserProfile, TenantVerification

logger = logging.getLogger(__name__)


def is_admin_or_executive(user):
    if not user or not user.is_authenticated:
        return False
    if user.is_superuser or user.is_staff:
        return True
    profile = getattr(user, 'profile', None)
    if profile and profile.role in ['admin', 'executive']:
        return True
    return False


class PublicAccessRequestView(APIView):
    """
    Public Endpoint: Allows enterprise leaders to submit a Corporate Access Application.
    Zero JWT authentication required (AllowAny).
    Eliminates authentication bounce loops and preserves applicant data.
    """
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        data = request.data or {}

        # Required fields validation
        first_name = (data.get('first_name') or '').strip()
        last_name = (data.get('last_name') or '').strip()
        email = (data.get('email') or '').strip().lower()
        phone = (data.get('phone') or '').strip()
        job_title = (data.get('job_title') or '').strip()
        is_ceo = bool(data.get('is_ceo', True))
        sponsor_name = (data.get('executive_sponsor_name') or '').strip()
        sponsor_email = (data.get('executive_sponsor_email') or '').strip()
        password = data.get('password') or ''

        company_name = (data.get('company_name') or '').strip()
        trading_name = (data.get('trading_name') or '').strip()
        industry = (data.get('industry') or 'consulting').strip()
        physical_address = (data.get('physical_address') or '').strip()
        city = (data.get('city') or '').strip()
        province = (data.get('province') or 'Gauteng').strip()
        postal_code = (data.get('postal_code') or '').strip()
        postal_address = (data.get('postal_address') or '').strip()
        cipc_number = (data.get('cipc_number') or '').strip()
        tax_number = (data.get('tax_number') or '').strip()

        if not first_name or not last_name:
            return Response({'error': 'First name and last name are required.'}, status=status.HTTP_400_BAD_REQUEST)
        if not email or '@' not in email:
            return Response({'error': 'A valid corporate work email is required.'}, status=status.HTTP_400_BAD_REQUEST)
        if not phone:
            return Response({'error': 'Direct phone number is required.'}, status=status.HTTP_400_BAD_REQUEST)
        if not job_title:
            return Response({'error': 'Executive role / designation is required.'}, status=status.HTTP_400_BAD_REQUEST)
        if not company_name:
            return Response({'error': 'Company / Business entity name is required.'}, status=status.HTTP_400_BAD_REQUEST)
        if not physical_address or not city or not postal_code:
            return Response({'error': 'Complete physical address (Street, City, Postal Code) is required.'}, status=status.HTTP_400_BAD_REQUEST)
        if not password or len(password) < 8:
            return Response({'error': 'Workspace password must be at least 8 characters.'}, status=status.HTTP_400_BAD_REQUEST)

        # Check if user already exists in system
        if User.objects.filter(email__iexact=email).exists() or User.objects.filter(username__iexact=email).exists():
            return Response({
                'error': 'An active corporate account with this email address already exists. Please log in or use password reset.'
            }, status=status.HTTP_400_BAD_REQUEST)

        hashed_pwd = make_password(password)

        # Check for existing pending request
        existing_req = CorporateAccessRequest.objects.filter(email__iexact=email).first()
        if existing_req:
            if existing_req.status == 'approved':
                return Response({
                    'error': 'This organization access request has already been approved. Please log in.'
                }, status=status.HTTP_400_BAD_REQUEST)

            # Update existing pending request with fresh details
            existing_req.first_name = first_name
            existing_req.last_name = last_name
            existing_req.phone = phone
            existing_req.job_title = job_title
            existing_req.is_ceo = is_ceo
            existing_req.executive_sponsor_name = sponsor_name
            existing_req.executive_sponsor_email = sponsor_email
            existing_req.hashed_password = hashed_pwd
            existing_req.company_name = company_name
            existing_req.trading_name = trading_name
            existing_req.industry = industry
            existing_req.physical_address = physical_address
            existing_req.city = city
            existing_req.province = province
            existing_req.postal_code = postal_code
            existing_req.postal_address = postal_address or physical_address
            existing_req.cipc_number = cipc_number
            existing_req.tax_number = tax_number
            existing_req.status = 'pending'
            existing_req.save()

            return Response({
                'success': True,
                'message': 'Your corporate access request has been updated and is awaiting executive review.',
                'request_id': str(existing_req.id),
                'company_name': company_name,
                'email': email
            }, status=status.HTTP_200_OK)

        # Create new request
        new_req = CorporateAccessRequest.objects.create(
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone=phone,
            job_title=job_title,
            is_ceo=is_ceo,
            executive_sponsor_name=sponsor_name,
            executive_sponsor_email=sponsor_email,
            hashed_password=hashed_pwd,
            company_name=company_name,
            trading_name=trading_name,
            industry=industry,
            physical_address=physical_address,
            city=city,
            province=province,
            postal_code=postal_code,
            postal_address=postal_address or physical_address,
            cipc_number=cipc_number,
            tax_number=tax_number,
            status='pending'
        )

        logger.info(f"New Corporate Access Request created: {company_name} ({email})")

        return Response({
            'success': True,
            'message': 'Your corporate access application has been received and is undergoing executive review by Mtambo Holdings.',
            'request_id': str(new_req.id),
            'company_name': company_name,
            'email': email
        }, status=status.HTTP_201_CREATED)


class AdminAccessRequestListView(APIView):
    """
    Executive Console Endpoint: View all incoming corporate access requests.
    Only authorized Administrators & Executives can access.
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        if not is_admin_or_executive(request.user):
            return Response({'error': 'Unauthorized. Executive administrative privileges required.'}, status=status.HTTP_403_FORBIDDEN)

        requests = CorporateAccessRequest.objects.all().order_by('-created_at')
        results = []
        for r in requests:
            results.append({
                'id': str(r.id),
                'first_name': r.first_name,
                'last_name': r.last_name,
                'email': r.email,
                'phone': r.phone,
                'job_title': r.job_title,
                'is_ceo': r.is_ceo,
                'executive_sponsor_name': r.executive_sponsor_name,
                'executive_sponsor_email': r.executive_sponsor_email,
                'company_name': r.company_name,
                'trading_name': r.trading_name,
                'industry': r.industry,
                'physical_address': r.physical_address,
                'city': r.city,
                'province': r.province,
                'postal_code': r.postal_code,
                'postal_address': r.postal_address,
                'cipc_number': r.cipc_number,
                'tax_number': r.tax_number,
                'status': r.status,
                'notes': r.notes,
                'rejection_reason': r.rejection_reason,
                'created_organization_id': str(r.created_organization_id) if r.created_organization_id else None,
                'created_organization_name': r.created_organization.name if r.created_organization else None,
                'created_user_id': r.created_user_id,
                'reviewed_by': r.reviewed_by.username if r.reviewed_by else None,
                'reviewed_at': r.reviewed_at.isoformat() if r.reviewed_at else None,
                'created_at': r.created_at.isoformat() if r.created_at else None,
            })

        pending_count = requests.filter(status='pending').count()
        return Response({
            'requests': results,
            'total_count': len(results),
            'pending_count': pending_count
        })


class AdminAccessRequestActionView(APIView):
    """
    Executive 1-Click Action:
    - 'approve': Automatically provisions the Organization tenant, User, UserProfile (role=admin),
                 TenantVerification, 7-Day VIP trial, and dispatches activation email.
    - 'reject': Marks request rejected with reason.
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        if not is_admin_or_executive(request.user):
            return Response({'error': 'Unauthorized. Executive administrative privileges required.'}, status=status.HTTP_403_FORBIDDEN)

        try:
            req_obj = CorporateAccessRequest.objects.get(pk=pk)
        except CorporateAccessRequest.DoesNotExist:
            return Response({'error': 'Access request not found.'}, status=status.HTTP_404_NOT_FOUND)

        action = (request.data.get('action') or '').strip().lower()
        notes = request.data.get('notes', '')
        rejection_reason = request.data.get('rejection_reason', '')

        if action not in ['approve', 'reject']:
            return Response({'error': "Action must be either 'approve' or 'reject'."}, status=status.HTTP_400_BAD_REQUEST)

        if action == 'reject':
            req_obj.status = 'rejected'
            req_obj.rejection_reason = rejection_reason or 'Application did not satisfy verification criteria.'
            req_obj.notes = notes
            req_obj.reviewed_by = request.user
            req_obj.reviewed_at = timezone.now()
            req_obj.save()

            return Response({
                'success': True,
                'status': 'rejected',
                'message': f"Request for {req_obj.company_name} rejected."
            })

        # Action == 'approve' -> Provision Workspace
        if req_obj.status == 'approved' and req_obj.created_organization:
            return Response({
                'message': f"Workspace for {req_obj.company_name} was already provisioned.",
                'organization_id': str(req_obj.created_organization.id)
            })

        # 1. Organization Provisioning
        org = Organization.objects.filter(name__iexact=req_obj.company_name).first()
        if not org:
            org = Organization(
                name=req_obj.company_name,
                subscription_tier='trial',
                max_users=10,
                is_cipc_verified=bool(req_obj.cipc_number)
            )
            org.save()
        else:
            if req_obj.cipc_number:
                org.is_cipc_verified = True
                org.save(update_fields=['is_cipc_verified'])

        # 2. User Provisioning
        user = User.objects.filter(username__iexact=req_obj.email).first() or User.objects.filter(email__iexact=req_obj.email).first()
        if not user:
            user = User(
                username=req_obj.email,
                email=req_obj.email,
                first_name=req_obj.first_name,
                last_name=req_obj.last_name,
                is_active=True
            )
            # Use pre-hashed password
            if req_obj.hashed_password:
                user.password = req_obj.hashed_password
            else:
                user.set_password('Finisher2026!')
            user.save()
        else:
            user.first_name = req_obj.first_name
            user.last_name = req_obj.last_name
            if req_obj.hashed_password:
                user.password = req_obj.hashed_password
            user.is_active = True
            user.save()

        # 3. UserProfile Provisioning
        full_address = f"{req_obj.physical_address}, {req_obj.city}, {req_obj.province} {req_obj.postal_code}".strip(', ')
        profile, _ = UserProfile.objects.get_or_create(user=user)
        profile.organization = org
        profile.role = 'admin'
        profile.tier = 'luxury'
        profile.company_name = req_obj.company_name
        profile.phone = req_obj.phone
        profile.job_title = req_obj.job_title
        profile.address = full_address
        profile.terms_accepted_at = timezone.now()
        profile.save()

        # 4. TenantVerification Record
        TenantVerification.objects.update_or_create(
            organization=org,
            defaults={
                'submitted_by': user,
                'company_name': req_obj.company_name,
                'trading_name': req_obj.trading_name,
                'cipc_number': req_obj.cipc_number or 'PENDING-SUBMISSION',
                'tax_number': req_obj.tax_number,
                'director_name': f"{req_obj.first_name} {req_obj.last_name}",
                'status': 'verified' if req_obj.cipc_number else 'pending',
                'reviewed_by': request.user,
                'reviewed_at': timezone.now()
            }
        )

        # 5. Finalize Request Object
        req_obj.status = 'approved'
        req_obj.created_organization = org
        req_obj.created_user = user
        req_obj.reviewed_by = request.user
        req_obj.reviewed_at = timezone.now()
        req_obj.notes = notes
        req_obj.save()

        # 6. Welcome / Activation Dispatch
        login_url = "https://www.thefinishercrm.tech/#/login"
        email_subject = f"Authorized: Your FINISHER Workspace for {req_obj.company_name} is Live"
        email_body = (
            f"Dear {req_obj.first_name} {req_obj.last_name},\n\n"
            f"We are pleased to inform you that your corporate access application for "
            f"{req_obj.company_name} has been reviewed and authorized by Mtambo Holdings.\n\n"
            f"Your dedicated FINISHER LUXURY workspace has been provisioned with 7-Day VIP Executive privileges.\n\n"
            f"Access Credentials:\n"
            f"• Workspace Portal: {login_url}\n"
            f"• Login Email: {req_obj.email}\n"
            f"• Password: The secure password you configured during your application.\n\n"
            f"Welcome to the pinnacle of executive enterprise management.\n\n"
            f"Sincerely,\n"
            f"Executive Directorate\n"
            f"THE FINISHER LUXURY | Mtambo Holdings\n"
        )

        try:
            send_mail(
                email_subject,
                email_body,
                getattr(settings, 'DEFAULT_FROM_EMAIL', 'no-reply@thefinishercrm.tech'),
                [req_obj.email],
                fail_silently=True
            )
        except Exception as mail_err:
            logger.warning(f"Failed to dispatch activation email: {mail_err}")

        logger.info(f"Corporate Workspace APPROVED and PROVISIONED for {req_obj.company_name} by {request.user.username}")

        return Response({
            'success': True,
            'status': 'approved',
            'message': f"Workspace for {req_obj.company_name} successfully provisioned with VIP Executive privileges.",
            'organization': {
                'id': str(org.id),
                'name': org.name,
                'slug': org.slug,
                'subscription_tier': org.subscription_tier,
                'days_remaining': org.days_remaining_in_trial
            },
            'user': {
                'id': user.id,
                'email': user.email,
                'full_name': f"{user.first_name} {user.last_name}",
                'role': profile.role
            }
        }, status=status.HTTP_200_OK)

import logging
import secrets
import string
from urllib.parse import quote
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.utils import timezone
from django.core.mail import send_mail
from .email_service import send_email_async
from django.conf import settings
from django.db.models import Q
from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response

from .utils import is_owner_admin_user
from .models import CorporateAccessRequest, Organization, UserProfile, TenantVerification, WebsiteLead, Notification, Company

logger = logging.getLogger(__name__)


def generate_secure_password():
    """Generates an auto-generated enterprise credential in format Fin-XXXX-XXXX"""
    part1 = ''.join(secrets.choice(string.ascii_uppercase + string.digits) for _ in range(4))
    part2 = ''.join(secrets.choice(string.ascii_uppercase + string.digits) for _ in range(4))
    return f"Fin-{part1}-{part2}"


def is_admin_or_executive(user):
    """
    Strict isolation: Only the platform owner superuser or adminluxury can access
    the global fleet management / Corporate Access Requests console.
    Client CEOs / tenant admins are isolated from the global platform console.
    """
    if not user or not user.is_authenticated:
        return False
    if user.is_superuser or is_owner_admin_user(user):
        return True
    return False


def purge_expired_access_requests():
    """
    Ephemeral retention policy (5-Minute TTL):
    Permanently purges unverified corporate access requests older than 5 minutes.
    Keeps the database secure, zero-zombie, and POPIA Section 19 compliant.
    """
    try:
        now = timezone.now()
        cutoff = now - timezone.timedelta(minutes=5)
        purged_count, _ = CorporateAccessRequest.objects.filter(
            is_verified=False
        ).filter(
            Q(expires_at__lte=now) | Q(created_at__lte=cutoff)
        ).delete()
        if purged_count > 0:
            logger.info(f"Purged {purged_count} expired unverified access requests from database.")
    except Exception as e:
        logger.warning(f"Error purging expired access requests: {e}")


class PublicCEOSearchView(APIView):
    """
    Public Endpoint: Search registered CEOs & corporate entities in THE FINISHER network.
    Non-CEOs must search and select an established CEO/Company to associate their onboarding request.
    Platform owner account (adminluxury) is strictly excluded to maintain absolute secrecy.
    """
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        purge_expired_access_requests()

        q = (request.query_params.get('q') or '').strip()
        if not q or len(q) < 2:
            return Response([])

        results = []
        seen_company_names = set()

        # 1. Search existing Organizations
        orgs = Organization.objects.filter(
            Q(name__icontains=q) | Q(slug__icontains=q)
        ).select_related()[:10]

        for org in orgs:
            admin_profile = UserProfile.objects.filter(
                organization=org, role='admin'
            ).exclude(
                user__username__iexact='adminluxury'
            ).exclude(
                user__is_superuser=True
            ).select_related('user').first()

            ceo_name = "Executive Directorate"
            ceo_email = ""
            job_title = "Chief Executive Officer (CEO)"

            if admin_profile and admin_profile.user:
                ceo_name = f"{admin_profile.user.first_name} {admin_profile.user.last_name}".strip() or admin_profile.user.username
                ceo_email = admin_profile.user.email
                job_title = admin_profile.job_title or "Chief Executive Officer (CEO)"

            seen_company_names.add(org.name.lower().strip())
            results.append({
                'organization_id': str(org.id),
                'company_name': org.name,
                'ceo_name': ceo_name,
                'ceo_email': ceo_email,
                'job_title': job_title,
                'is_verified': org.is_cipc_verified,
                'tier': org.subscription_tier
            })

        # 2. Search Admin / Executive UserProfiles (Strictly exclude adminluxury / superusers)
        admin_profiles = UserProfile.objects.filter(
            role='admin'
        ).exclude(
            user__username__iexact='adminluxury'
        ).exclude(
            user__is_superuser=True
        ).filter(
            Q(user__first_name__icontains=q) |
            Q(user__last_name__icontains=q) |
            Q(company_name__icontains=q) |
            Q(job_title__icontains=q)
        ).select_related('user', 'organization')[:10]

        for p in admin_profiles:
            org = p.organization
            company_name = (org.name if org else p.company_name) or "Corporate Entity"
            comp_key = company_name.lower().strip()
            if comp_key in seen_company_names:
                continue

            ceo_name = f"{p.user.first_name} {p.user.last_name}".strip() if p.user else "Corporate Officer"
            org_id = str(org.id) if org else f"profile-{p.id}"
            seen_company_names.add(comp_key)

            results.append({
                'organization_id': org_id,
                'company_name': company_name,
                'ceo_name': ceo_name,
                'ceo_email': p.user.email if p.user else "",
                'job_title': p.job_title or "Chief Executive Officer (CEO)",
                'is_verified': org.is_cipc_verified if org else False,
                'tier': org.subscription_tier if org else 'trial'
            })

        # 3. Search CorporateAccessRequests (Strictly verified only; unverified records are never exposed)
        ceo_requests = CorporateAccessRequest.objects.filter(
            is_ceo=True,
            is_verified=True
        ).filter(
            Q(first_name__icontains=q) |
            Q(last_name__icontains=q) |
            Q(company_name__icontains=q)
        )[:10]

        for req in ceo_requests:
            comp_key = req.company_name.lower().strip()
            if comp_key in seen_company_names:
                continue

            req_name = f"{req.first_name} {req.last_name}".strip()
            seen_company_names.add(comp_key)
            results.append({
                'organization_id': str(req.created_organization_id) if req.created_organization_id else f"req-{req.id}",
                'company_name': req.company_name,
                'ceo_name': req_name,
                'ceo_email': req.email,
                'job_title': req.job_title or "Chief Executive Officer (CEO)",
                'is_verified': bool(req.cipc_number),
                'tier': '7-Day VIP Executive'
            })

        # 4. Search Company CRM records
        companies = Company.objects.filter(
            name__icontains=q
        ).select_related('user')[:10]

        for c in companies:
            comp_key = c.name.lower().strip()
            if comp_key in seen_company_names:
                continue

            c_user = c.user
            ceo_name = f"{c_user.first_name} {c_user.last_name}".strip() if c_user else "Executive Officer"
            seen_company_names.add(comp_key)
            results.append({
                'organization_id': f"comp-{c.id}",
                'company_name': c.name,
                'ceo_name': ceo_name,
                'ceo_email': c_user.email if c_user else "",
                'job_title': "Chief Executive Officer (CEO)",
                'is_verified': bool(c.registration_number),
                'tier': '7-Day VIP Executive'
            })

        return Response(results)


class PublicAccessRequestView(APIView):
    """
    Public Endpoint: Allows enterprise leaders to submit a Corporate Access Application.
    Zero manual password setup required: Password is auto-generated by the system and emailed upon approval.
    Alerts are dispatched to sales@mtamboholdings.dev and logged in Admin Leads & Notifications.
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

        target_ceo_name = (data.get('target_ceo_name') or '').strip()
        target_organization_id = (data.get('target_organization_id') or '').strip()

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
            return Response({'error': 'Corporate designation is required.'}, status=status.HTTP_400_BAD_REQUEST)

        # CEO Search Engine Validation for non-CEOs
        if not is_ceo:
            if not target_ceo_name and not target_organization_id:
                return Response({
                    'error': 'Non-CEOs must search and select a registered CEO / verified Company to associate their request.'
                }, status=status.HTTP_400_BAD_REQUEST)
            if not company_name:
                return Response({
                    'error': 'Corporate organization must be selected from the CEO registry.'
                }, status=status.HTTP_400_BAD_REQUEST)
        else:
            if not company_name:
                return Response({'error': 'Company / Business entity name is required.'}, status=status.HTTP_400_BAD_REQUEST)

        if not physical_address or not city or not postal_code:
            return Response({'error': 'Complete physical address (Street, City, Postal Code) is required.'}, status=status.HTTP_400_BAD_REQUEST)

        # Check if user already exists in system
        if User.objects.filter(email__iexact=email).exists() or User.objects.filter(username__iexact=email).exists():
            return Response({
                'error': 'An active corporate account with this email address already exists. Please log in or use password reset.'
            }, status=status.HTTP_400_BAD_REQUEST)

        # Call purge of expired unverified records (5-minute TTL)
        purge_expired_access_requests()

        # AUTO-GENERATE SECURE ENTERPRISE CREDENTIALS & 6-DIGIT VERIFICATION CODE
        auto_password = generate_secure_password()
        hashed_pwd = make_password(auto_password)
        verification_code = ''.join(secrets.choice(string.digits) for _ in range(6))
        expires_at = timezone.now() + timezone.timedelta(minutes=5)

        # Check for existing request
        existing_req = CorporateAccessRequest.objects.filter(email__iexact=email).first()
        if existing_req:
            if existing_req.status == 'approved':
                return Response({
                    'error': 'This organization access request has already been approved. Please log in.'
                }, status=status.HTTP_400_BAD_REQUEST)

            # Update existing pending request with fresh details and refreshed 5-minute TTL
            existing_req.first_name = first_name
            existing_req.last_name = last_name
            existing_req.phone = phone
            existing_req.job_title = job_title
            existing_req.is_ceo = is_ceo
            existing_req.target_ceo_name = target_ceo_name
            existing_req.target_organization_id = target_organization_id
            existing_req.auto_generated_password = auto_password
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
            existing_req.verification_code = verification_code
            existing_req.expires_at = expires_at
            existing_req.is_verified = False
            existing_req.status = 'pending'
            existing_req.save()
            req_obj = existing_req
        else:
            # Create new unverified request (5-Minute TTL)
            req_obj = CorporateAccessRequest.objects.create(
                first_name=first_name,
                last_name=last_name,
                email=email,
                phone=phone,
                job_title=job_title,
                is_ceo=is_ceo,
                target_ceo_name=target_ceo_name,
                target_organization_id=target_organization_id,
                auto_generated_password=auto_password,
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
                verification_code=verification_code,
                expires_at=expires_at,
                is_verified=False,
                status='pending'
            )

        logger.info(f"Corporate Access Request created (5-Min TTL): {company_name} ({email}) - Code: {verification_code}")

        # Dispatch 5-Minute Verification Code to Applicant Email
        verify_subject = f"Verify Corporate Application: {verification_code} (Expires in 5 Minutes)"
        verify_body = (
            f"Dear {first_name} {last_name},\n\n"
            f"Your 6-digit identity verification code for {company_name} is:\n\n"
            f"       {verification_code}\n\n"
            f"⏱️ 5-MINUTE EPHEMERAL EXPIRATION NOTICE:\n"
            f"This verification code is valid for exactly 5 minutes.\n"
            f"In accordance with enterprise zero-trust policy, unverified registration dossiers are automatically wiped and permanently purged from the database after 5 minutes.\n\n"
            f"Enter this code on the registration page to confirm your application.\n\n"
            f"Sincerely,\n"
            f"Executive Directorate | THE FINISHER LUXURY | Mtambo Holdings\n"
            f"https://www.thefinishercrm.tech\n"
        )
        from_sender = getattr(settings, 'DEFAULT_FROM_EMAIL', None) or 'onboarding@resend.dev'
        # Asynchronously dispatch 5-minute verification code via Resend HTTPS API / background daemon thread (< 1ms)
        send_email_async(
            verify_subject,
            verify_body,
            [email],
            from_email=from_sender
        )

        return Response({
            'success': True,
            'requires_verification': True,
            'request_id': str(req_obj.id),
            'email': email,
            'company_name': company_name,
            'expires_in_seconds': 300,
            'message': f'A 6-digit verification code has been dispatched to {email}. Please verify within 5 minutes.'
        }, status=status.HTTP_200_OK)


class PublicVerifyAccessRequestView(APIView):
    """
    Public Endpoint: Confirms the applicant's 6-digit verification code within the 5-minute TTL window.
    If 5 minutes have elapsed, the record is permanently deleted and 400 is returned.
    If code is valid, marks is_verified=True, and notifies sales@mtamboholdings.dev and Admin Leads inbox.
    """
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        purge_expired_access_requests()

        data = request.data or {}
        request_id = data.get('request_id')
        submitted_code = (data.get('verification_code') or '').strip()

        if not request_id:
            return Response({'error': 'Request ID is required.'}, status=status.HTTP_400_BAD_REQUEST)
        if not submitted_code:
            return Response({'error': 'Verification code is required.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            req_obj = CorporateAccessRequest.objects.get(pk=request_id)
        except (CorporateAccessRequest.DoesNotExist, Exception):
            return Response({
                'error': 'Application session has expired or been purged from the system. Please re-apply.'
            }, status=status.HTTP_404_NOT_FOUND)

        # Check if already verified
        if req_obj.is_verified:
            return Response({
                'success': True,
                'verified': True,
                'message': 'Application is already verified and under executive review.'
            })

        # Check 5-minute expiration
        now = timezone.now()
        is_expired = (req_obj.expires_at and now > req_obj.expires_at) or (req_obj.created_at < now - timezone.timedelta(minutes=5))
        if is_expired:
            req_obj.delete()
            return Response({
                'error': 'Verification window expired (5 minutes exceeded). Your temporary record has been permanently purged from the database. Please submit a fresh request.'
            }, status=status.HTTP_400_BAD_REQUEST)

        # Verify Code
        if submitted_code != req_obj.verification_code:
            return Response({'error': 'Invalid verification code. Please check and try again.'}, status=status.HTTP_400_BAD_REQUEST)

        # Mark Verified
        req_obj.is_verified = True
        req_obj.save(update_fields=['is_verified'])

        # 1. Dispatch Email Alert to sales@mtamboholdings.dev
        sales_email = getattr(settings, 'SALES_EMAIL', 'sales@mtamboholdings.dev')
        exec_subject = f"[VERIFIED CORPORATE REQUEST] {req_obj.company_name} - {req_obj.first_name} {req_obj.last_name} ({req_obj.job_title})"
        exec_body = (
            f"EXECUTIVE CORPORATE ACCESS ALERT (IDENTITY VERIFIED)\n"
            f"-----------------------------------------------------\n"
            f"A verified corporate workspace application is ready for executive review.\n\n"
            f"APPLICANT DOSSIER:\n"
            f"• Full Name: {req_obj.first_name} {req_obj.last_name}\n"
            f"• Corporate Designation: {req_obj.job_title}\n"
            f"• Work Email: {req_obj.email}\n"
            f"• Phone Number: {req_obj.phone}\n"
            f"• Executive Role: {'Chief Executive Officer (New Tenant)' if req_obj.is_ceo else f'Non-CEO Associate (Target CEO: {req_obj.target_ceo_name})'}\n\n"
            f"ORGANIZATION DETAILS:\n"
            f"• Legal Entity Name: {req_obj.company_name}\n"
            f"• Trading Name: {req_obj.trading_name or 'N/A'}\n"
            f"• Industry Sector: {req_obj.industry}\n"
            f"• Physical Address: {req_obj.physical_address}, {req_obj.city}, {req_obj.province} {req_obj.postal_code}\n"
            f"• CIPC Number: {req_obj.cipc_number or 'N/A'}\n"
            f"• SARS Tax/VAT: {req_obj.tax_number or 'N/A'}\n\n"
            f"EXECUTIVE ACTION:\n"
            f"Authorize and provision this workspace in 1-click on the Executive Control Deck:\n"
            f"https://www.thefinishercrm.tech/#/admin/console\n\n"
            f"THE FINISHER LUXURY | Automated Enterprise Gateway\n"
        )

        send_email_async(
            exec_subject,
            exec_body,
            [sales_email],
            from_email=getattr(settings, 'DEFAULT_FROM_EMAIL', 'security@thefinisher.tech')
        )

        # 2. Dispatch Confirmation Receipt Email to Applicant
        ack_subject = f"Application Verified: FINISHER Luxury Corporate Access for {req_obj.company_name}"
        ack_body = (
            f"Dear {req_obj.first_name} {req_obj.last_name},\n\n"
            f"Your corporate identity has been verified successfully.\n"
            f"Your access application for {req_obj.company_name} is now queued for executive review by Mtambo Holdings under 7-Day VIP Executive privileges.\n\n"
            f"What happens next?\n"
            f"1. The Executive Directorate will review your company dossier.\n"
            f"2. Upon executive authorization, your enterprise workspace will be provisioned.\n"
            f"3. Your auto-generated secure credentials will be delivered to {req_obj.email}.\n\n"
            f"If you have urgent requirements, contact sales@mtamboholdings.dev.\n\n"
            f"Sincerely,\n"
            f"Executive Directorate\n"
            f"THE FINISHER LUXURY | Mtambo Holdings\n"
            f"https://www.thefinishercrm.tech\n"
        )

        send_email_async(
            ack_subject,
            ack_body,
            [req_obj.email],
            from_email=getattr(settings, 'DEFAULT_FROM_EMAIL', 'security@thefinisher.tech')
        )

        # 3. Create WebsiteLead & Notification for Admin Fleet Console
        try:
            lead_owner = User.objects.filter(is_superuser=True).first()
            if lead_owner:
                WebsiteLead.objects.create(
                    owner=lead_owner,
                    first_name=req_obj.first_name,
                    last_name=req_obj.last_name,
                    email=req_obj.email,
                    phone=req_obj.phone,
                    source='corporate_access_request',
                    inbound_message=(
                        f"Corporate Access Request for {req_obj.company_name} ({req_obj.job_title}). "
                        f"Status: {'CEO' if req_obj.is_ceo else f'Associate under {req_obj.target_ceo_name}'}. "
                        f"Headquarters: {req_obj.physical_address}, {req_obj.city}, {req_obj.province} {req_obj.postal_code}. CIPC: {req_obj.cipc_number or 'N/A'}."
                    ),
                    spam_score=100,
                    is_spam_risk=False
                )
                Notification.objects.create(
                    recipient=lead_owner,
                    title='New Verified Corporate Access Request',
                    message=f'{req_obj.first_name} {req_obj.last_name} ({req_obj.job_title}) submitted corporate dossier for {req_obj.company_name}',
                    entity_type='corporate_access_request',
                    entity_id=req_obj.id,
                    meta={
                        'company_name': req_obj.company_name,
                        'email': req_obj.email,
                        'phone': req_obj.phone,
                        'is_ceo': req_obj.is_ceo,
                        'request_id': str(req_obj.id)
                    }
                )
        except Exception as db_lead_err:
            logger.warning(f"Failed to create website lead / notification: {db_lead_err}")

        return Response({
            'success': True,
            'verified': True,
            'message': 'Your corporate access application has been verified and submitted for executive review.',
            'request_id': str(req_obj.id),
            'company_name': req_obj.company_name,
            'email': req_obj.email,
            'sales_contact': sales_email
        }, status=status.HTTP_200_OK)


class PublicCancelAccessRequestView(APIView):
    """
    Public Endpoint: Cancels/deletes an unverified corporate access request (e.g. when 5-minute timer expires).
    """
    permission_classes = [permissions.AllowAny]

    def delete(self, request, pk):
        deleted_count, _ = CorporateAccessRequest.objects.filter(pk=pk, is_verified=False).delete()
        return Response({
            'success': True,
            'purged': bool(deleted_count),
            'message': 'Temporary unverified record permanently purged from database.'
        })


class AdminAccessRequestListView(APIView):
    """
    Executive Console Endpoint: View all incoming verified corporate access requests.
    Only authorized Administrators & Executives can access.
    Automatically purges expired unverified requests before loading.
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        if not is_admin_or_executive(request.user):
            return Response({'error': 'Unauthorized. Executive administrative privileges required.'}, status=status.HTTP_403_FORBIDDEN)

        # Clean up any stale unverified requests
        purge_expired_access_requests()

        requests = CorporateAccessRequest.objects.filter(is_verified=True).order_by('-created_at')
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
                'target_ceo_name': getattr(r, 'target_ceo_name', '') or r.executive_sponsor_name,
                'target_organization_id': getattr(r, 'target_organization_id', ''),
                'auto_generated_password': getattr(r, 'auto_generated_password', ''),
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
                 TenantVerification, 7-Day VIP trial, and dispatches activation email with auto-generated credentials.
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

        # Ensure auto-generated password exists
        auto_password = getattr(req_obj, 'auto_generated_password', '')
        if not auto_password:
            auto_password = generate_secure_password()
            req_obj.auto_generated_password = auto_password
            req_obj.hashed_password = make_password(auto_password)
            req_obj.save(update_fields=['auto_generated_password', 'hashed_password'])

        # 1. Organization Provisioning
        target_org_id = getattr(req_obj, 'target_organization_id', '')
        org = None
        if not req_obj.is_ceo and target_org_id:
            org = Organization.objects.filter(id=target_org_id).first()

        if not org:
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
            user.password = req_obj.hashed_password
            user.save()
        else:
            user.first_name = req_obj.first_name
            user.last_name = req_obj.last_name
            user.password = req_obj.hashed_password
            user.is_active = True
            user.save()

        # 3. UserProfile Provisioning
        full_address = f"{req_obj.physical_address}, {req_obj.city}, {req_obj.province} {req_obj.postal_code}".strip(', ')
        profile, _ = UserProfile.objects.get_or_create(user=user)
        profile.organization = org
        profile.role = 'admin' if req_obj.is_ceo else 'executive'
        profile.tier = 'luxury'
        profile.company_name = req_obj.company_name
        profile.phone = req_obj.phone
        profile.job_title = req_obj.job_title
        profile.address = full_address
        profile.terms_accepted_at = timezone.now()
        profile.requires_password_reset = True
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

        # 6. Welcome / Activation Dispatch containing the AUTO-GENERATED credentials
        login_url = "https://www.thefinishercrm.tech/#/login"
        email_subject = f"Authorized: Your FINISHER Workspace for {req_obj.company_name} is Live"
        email_body = (
            f"═════════════════════════════════════════════════════════════════════════\n"
            f"          THE FINISHER LUXURY | EXECUTIVE DIRECTORATE\n"
            f"                  MTAMBO HOLDINGS PRIVATE FLEET\n"
            f"═════════════════════════════════════════════════════════════════════════\n\n"
            f"Dear {req_obj.first_name} {req_obj.last_name},\n\n"
            f"We are pleased to inform you that your Corporate Access Dossier for\n"
            f"{req_obj.company_name} has been reviewed and officially authorized by\n"
            f"Mtambo Holdings under 7-Day VIP Executive Privileges.\n\n"
            f"Your dedicated enterprise workspace has been provisioned and is now live\n"
            f"on our secure private cloud infrastructure.\n\n"
            f"─────────────────────────────────────────────────────────────────────────\n"
            f"🔑 YOUR AUTHORIZED ENTERPRISE CREDENTIALS\n"
            f"─────────────────────────────────────────────────────────────────────────\n"
            f"• Workspace Portal   : {login_url}\n"
            f"• Authorized Email   : {req_obj.email}\n"
            f"• Temporary Passcode : {auto_password}\n"
            f"• Provisioned Tier   : 7-Day VIP Executive Fleet\n"
            f"─────────────────────────────────────────────────────────────────────────\n\n"
            f"🔒 MANDATORY FIRST-LOGIN SECURITY PROTOCOL:\n"
            f"In accordance with zero-trust data governance and POPIA Section 19\n"
            f"safeguards, your temporary passcode will expire upon first use.\n"
            f"You will be prompted immediately to set your own permanent,\n"
            f"confidential password before entering the platform.\n\n"
            f"If you require executive onboarding assistance or custom enterprise\n"
            f"integrations, our directorate is on standby at: sales@mtamboholdings.dev\n\n"
            f"Welcome to the pinnacle of luxury enterprise automation.\n\n"
            f"With highest regards,\n\n"
            f"THE EXECUTIVE DIRECTORATE\n"
            f"THE FINISHER LUXURY | MTAMBO HOLDINGS\n"
            f"Portal: https://www.thefinishercrm.tech\n"
            f"Inquiries: sales@mtamboholdings.dev\n"
            f"═════════════════════════════════════════════════════════════════════════\n"
        )

        send_email_async(
            email_subject,
            email_body,
            [req_obj.email],
            from_email=getattr(settings, 'DEFAULT_FROM_EMAIL', 'security@thefinisher.tech')
        )

        logger.info(f"Corporate Workspace APPROVED and PROVISIONED for {req_obj.company_name} by {request.user.username}")

        mailto_link = f"mailto:{req_obj.email}?subject={quote(email_subject)}&body={quote(email_body)}"

        return Response({
            'success': True,
            'status': 'approved',
            'message': f"Workspace for {req_obj.company_name} successfully provisioned.",
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
            },
            'auto_generated_password': auto_password,
            'email_subject': email_subject,
            'email_body': email_body,
            'mailto_link': mailto_link
        }, status=status.HTTP_200_OK)

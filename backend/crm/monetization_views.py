import uuid
import hashlib
import io
import logging
from datetime import datetime, timedelta
from django.utils import timezone
from django.conf import settings
from django.http import HttpResponse
from django.db.models import Sum
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser



from .models import Organization, UserProfile, Deal, Contact, PaymentTransaction
from .audit_utils import record_audit_event

logger = logging.getLogger(__name__)

PAYFAST_PROCESS_URL = "https://www.payfast.co.za/eng/process"
PAYFAST_SANDBOX_URL = "https://sandbox.payfast.co.za/eng/process"
DEFAULT_MERCHANT_ID = "37019297"
DEFAULT_MERCHANT_KEY = "dououppbwqtve"

def get_verified_frontend_url():
    url = str(getattr(settings, 'FRONTEND_URL', 'https://www.thefinishercrm.tech') or '').rstrip('/')
    if 'thefinisher.tech' in url and 'thefinishercrm.tech' not in url:
        return 'https://www.thefinishercrm.tech'
    return url or 'https://www.thefinishercrm.tech'


class WhiteLabelCheckoutView(APIView):
    """
    POST /api/billing/white-label/checkout/
    Generates PayFast recurring subscription parameters for R199/month.
    Removes Finisher watermark and enables custom branding letterhead.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        profile = getattr(user, 'profile', None)
        org = getattr(profile, 'organization', None)

        if not org:
            return Response({'error': 'Organization profile not found'}, status=status.HTTP_400_BAD_REQUEST)

        # Check if already active
        if org.is_white_labeled:
            return Response({
                'is_active': True,
                'message': 'White-Label Branding is already active for this organization.'
            })

        tx_ref = f"WL-{org.id.hex[:8]}-{int(timezone.now().timestamp())}"
        merchant_id = getattr(settings, 'PAYFAST_MERCHANT_ID', DEFAULT_MERCHANT_ID) or DEFAULT_MERCHANT_ID
        merchant_key = getattr(settings, 'PAYFAST_MERCHANT_KEY', DEFAULT_MERCHANT_KEY) or DEFAULT_MERCHANT_KEY
        is_sandbox = getattr(settings, 'PAYFAST_SANDBOX', False)
        process_url = PAYFAST_SANDBOX_URL if is_sandbox else PAYFAST_PROCESS_URL
        frontend_url = get_verified_frontend_url()
        client_ip = request.META.get('HTTP_X_FORWARDED_FOR', '').split(',')[0].strip() or request.META.get('REMOTE_ADDR')

        # Record Pending Transaction with Forensic Audit Evidence (POPIA Section 19)
        PaymentTransaction.objects.create(
            organization=org,
            transaction_reference=tx_ref,
            amount_cents=19900,
            currency='ZAR',
            gateway='payfast',
            status='pending',
            raw_payload={
                'user_id': user.id,
                'user_username': user.username,
                'user_email': user.email,
                'organization_id': str(org.id),
                'organization_name': org.name,
                'primary_merchant_id': merchant_id,
                'type': 'white_label_subscription',
                'period': 'monthly',
                'base_amount': 199.00,
                'amount': 199.00,
                'client_ip': client_ip,
                'timestamp_utc': timezone.now().isoformat(),
                'jurisdiction': 'Republic of South Africa (POPIA Section 19)'
            }
        )

        record_audit_event(
            'PAYMENT_INTENT_CREATED',
            f"PayFast subscription checkout initiated for White-Label Branding (R199/mo) by {user.username} for '{org.name}' (Ref: {tx_ref})",
            user=user,
            organization=org,
            severity='INFO',
            metadata={'tx_ref': tx_ref, 'amount_cents': 19900, 'merchant_id': merchant_id}
        )

        return Response({
            'process_url': process_url,
            'merchant_id': merchant_id,
            'merchant_key': merchant_key,
            'amount': '199.00',
            'item_name': 'THE FINISHER LUXURY — Corporate White-Label (R199/mo)',
            'item_description': 'Monthly recurring custom branding license removing all watermarks.',
            'm_payment_id': tx_ref,
            'custom_str1': 'white_label',
            'custom_str2': str(org.id),
            'subscription_type': '1',
            'billing_date': (timezone.now() + timedelta(days=1)).strftime('%Y-%m-%d'),
            'recurring_amount': '199.00',
            'frequency': '3',  # Monthly in PayFast
            'cycles': '0',      # Indefinite
            'name_first': user.first_name or 'Executive',
            'name_last': user.last_name or 'Director',
            'email_address': user.email,
            'return_url': f"{frontend_url}/?white_label=success",
            'cancel_url': f"{frontend_url}/?white_label=cancel",
            'notify_url': 'https://the-finisher-luxury-api.onrender.com/api/billing/webhook/'
        })





class DealSplitPaymentCheckoutView(APIView):
    """
    POST /api/billing/deals/checkout/
    Generates PayFast Split Payment parameters for client-to-client transactions.
    Primary Merchant: Mtambo Holdings Group (37019297) - Platform Tollbooth (e.g. 2%)
    Secondary Merchant: Client's Organization PayFast Merchant ID (from TenantIntegration) - Net Proceeds (98%)
    Stores full forensic financial evidence in the database.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        profile = getattr(user, 'profile', None)
        org = getattr(profile, 'organization', None)
        if not org:
            return Response({'error': 'Organization profile not found'}, status=status.HTTP_400_BAD_REQUEST)

        deal_id = request.data.get('deal_id')
        try:
            amount = float(request.data.get('amount') or 0.0)
        except (TypeError, ValueError):
            amount = 0.0

        item_name = (request.data.get('item_name') or f"Commercial Settlement — {org.name}").strip()
        buyer_email = (request.data.get('buyer_email') or '').strip()

        if amount <= 0:
            return Response({'error': 'A valid transaction amount is required.'}, status=400)

        total_cents = int(round(amount * 100))
        # Default platform take-rate: 2.0% (minimum R5.00)
        platform_fee_percent = float(request.data.get('platform_fee_percent') or 2.0)
        platform_fee_cents = max(500, int(round(total_cents * (platform_fee_percent / 100.0))))
        vendor_cents = total_cents - platform_fee_cents

        primary_merchant_id = getattr(settings, 'PAYFAST_MERCHANT_ID', DEFAULT_MERCHANT_ID) or DEFAULT_MERCHANT_ID
        primary_merchant_key = getattr(settings, 'PAYFAST_MERCHANT_KEY', DEFAULT_MERCHANT_KEY) or DEFAULT_MERCHANT_KEY
        is_sandbox = getattr(settings, 'PAYFAST_SANDBOX', False)
        process_url = PAYFAST_SANDBOX_URL if is_sandbox else PAYFAST_PROCESS_URL
        frontend_url = get_verified_frontend_url()

        # Check if the seller organization has configured their own PayFast Merchant ID in TenantIntegration
        from .models import TenantIntegration
        vendor_integration = TenantIntegration.objects.filter(organization=org, provider='payfast', is_active=True).first()
        vendor_merchant_id = ((vendor_integration.config if vendor_integration else {}).get('merchant_id') or '').strip()

        tx_ref = f"SPLIT-{org.id.hex[:6]}-{int(timezone.now().timestamp())}"
        client_ip = request.META.get('HTTP_X_FORWARDED_FOR', '').split(',')[0].strip() or request.META.get('REMOTE_ADDR')

        evidence_payload = {
            'type': 'deal_split_payment',
            'deal_id': deal_id,
            'primary_merchant_id': primary_merchant_id,
            'vendor_merchant_id': vendor_merchant_id or 'NOT_REGISTERED_DIRECT_SETTLEMENT',
            'total_amount': amount,
            'total_amount_cents': total_cents,
            'platform_fee_percent': platform_fee_percent,
            'platform_fee_cents': platform_fee_cents,
            'vendor_cents': vendor_cents,
            'seller_org_id': str(org.id),
            'seller_org_name': org.name,
            'buyer_email': buyer_email,
            'client_ip': client_ip,
            'timestamp_utc': timezone.now().isoformat(),
            'split_active': bool(vendor_merchant_id)
        }

        PaymentTransaction.objects.create(
            organization=org,
            transaction_reference=tx_ref,
            amount_cents=total_cents,
            currency='ZAR',
            gateway='payfast',
            status='pending',
            raw_payload=evidence_payload
        )

        record_audit_event(
            'PAYMENT_SPLIT_CREATED',
            f"PayFast Split Payment checkout generated for {org.name} (Total: R{amount:,.2f} | Platform Fee: R{platform_fee_cents/100:,.2f} | Ref: {tx_ref})",
            user=user,
            organization=org,
            severity='INFO',
            metadata={'tx_ref': tx_ref, 'total_cents': total_cents, 'fee_cents': platform_fee_cents}
        )

        response_payload = {
            'process_url': process_url,
            'merchant_id': primary_merchant_id,
            'merchant_key': primary_merchant_key,
            'amount': f"{amount:.2f}",
            'item_name': item_name[:100],
            'm_payment_id': tx_ref,
            'custom_str1': 'deal_split',
            'custom_str2': str(org.id),
            'name_first': user.first_name or 'Executive',
            'name_last': user.last_name or 'Director',
            'email_address': buyer_email or user.email,
            'return_url': f"{frontend_url}/?deal_payment=success",
            'cancel_url': f"{frontend_url}/?deal_payment=cancel",
            'notify_url': 'https://the-finisher-luxury-api.onrender.com/api/billing/webhook/'
        }

        # If the seller has their PayFast Merchant ID enabled, inject the PayFast 'setup' Split Payment payload!
        if vendor_merchant_id:
            import json
            response_payload['setup'] = json.dumps({
                'split_payment': {
                    'merchant_id': vendor_merchant_id,
                    'amount': vendor_cents
                }
            })

        return Response(response_payload, status=status.HTTP_200_OK)





class WhiteLabelStatusView(APIView):
    """
    GET /api/billing/white-label/status/
    Returns current organization white-label and branding status.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        profile = getattr(user, 'profile', None)
        org = getattr(profile, 'organization', None)

        if not org:
            return Response({'error': 'Organization not found'}, status=status.HTTP_400_BAD_REQUEST)

        return Response({
            'organization_id': str(org.id),
            'organization_name': org.name,
            'is_white_labeled': org.is_white_labeled,
            'subscription_id': org.white_label_subscription_id or '',
            'has_custom_logo': bool(org.custom_logo),
            'custom_logo_url': org.custom_logo.url if org.custom_logo else None,
            'standard_watermark': "Secured by THE FINISHER LUXURY CRM Enterprise Network • thefinisher.co.za"
        })


class WhiteLabelLogoUploadView(APIView):
    """
    POST /api/billing/white-label/upload-logo/
    Uploads custom company logo for white-labeled quotes and invoices.
    """
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):
        user = request.user
        profile = getattr(user, 'profile', None)
        org = getattr(profile, 'organization', None)

        if not org:
            return Response({'error': 'Organization not found'}, status=status.HTTP_400_BAD_REQUEST)

        logo_file = request.FILES.get('logo')
        if not logo_file:
            return Response({'error': 'No logo file provided'}, status=status.HTTP_400_BAD_REQUEST)

        org.custom_logo = logo_file
        org.save(update_fields=['custom_logo'])

        return Response({
            'message': 'Custom company logo uploaded successfully.',
            'custom_logo_url': org.custom_logo.url
        })

"""
THE FINISHER LUXURY - Paystack South Africa Payment & Automated 7-Day Trial Billing Engine
Mtambo Holdings Group

Handles:
1. Card authorization / tokenization for automated 7-day VIP trials.
2. Recurring charge authorizations directly settling into South African bank accounts.
3. Subscription status transitions and 90-Day POPIA Data Retention Archiving.
"""
import os
import json
import logging
import urllib.request
import urllib.error
from django.conf import settings
from django.utils import timezone
from datetime import timedelta

logger = logging.getLogger(__name__)

PAYSTACK_BASE_URL = "https://api.paystack.co"
PAYSTACK_SECRET_KEY = os.environ.get('PAYSTACK_SECRET_KEY', getattr(settings, 'PAYSTACK_SECRET_KEY', ''))
PAYSTACK_PUBLIC_KEY = os.environ.get('PAYSTACK_PUBLIC_KEY', getattr(settings, 'PAYSTACK_PUBLIC_KEY', ''))


def _paystack_request(endpoint, method='GET', data=None):
    """
    Execute authenticated HTTP request to Paystack REST API using urllib (zero external dependencies).
    """
    url = f"{PAYSTACK_BASE_URL}{endpoint}"
    headers = {
        "Authorization": f"Bearer {PAYSTACK_SECRET_KEY}",
        "Content-Type": "application/json",
        "Accept": "application/json",
        "User-Agent": "TheFinisherLuxuryCRM/1.0"
    }

    req_data = json.dumps(data).encode('utf-8') if data else None
    request = urllib.request.Request(url, data=req_data, headers=headers, method=method)

    try:
        with urllib.request.urlopen(request, timeout=15) as response:
            body = response.read().decode('utf-8')
            return json.loads(body)
    except urllib.error.HTTPError as e:
        error_body = e.read().decode('utf-8') if e.fp else str(e)
        logger.error(f"[Paystack] HTTP {e.code} error on {endpoint}: {error_body}")
        try:
            return json.loads(error_body)
        except Exception:
            return {"status": False, "message": f"HTTP {e.code}: {e.reason}"}
    except Exception as e:
        logger.error(f"[Paystack] Request exception on {endpoint}: {str(e)}")
        return {"status": False, "message": str(e)}


class PaystackBillingGateway:
    """
    Institutional billing engine for The Finisher Luxury.
    """

    @classmethod
    def initialize_transaction(cls, email, amount_cents, reference=None, callback_url=None, metadata=None):
        """
        Initialize payment checkout or card authorization.
        amount_cents: e.g. 100 = R1.00 for card authorization / tokenization.
        """
        payload = {
            "email": email,
            "amount": amount_cents,
            "currency": "ZAR",
        }
        if reference:
            payload["reference"] = reference
        if callback_url:
            payload["callback_url"] = callback_url
        if metadata:
            payload["metadata"] = metadata

        return _paystack_request("/transaction/initialize", method="POST", data=payload)

    @classmethod
    def verify_transaction(cls, reference):
        """
        Verify transaction after client completes card payment or authorization.
        Returns authorization token for recurring 7-day billing.
        """
        return _paystack_request(f"/transaction/verify/{reference}", method="GET")

    @classmethod
    def charge_recurring_authorization(cls, authorization_code, email, amount_cents, reference=None):
        """
        AUTOMATED RECURRING CHARGE (POST 7-DAY TRIAL):
        Directly charges the client's vaulted card token without them having to re-enter details.
        Settles automatically into your South African bank account.
        """
        payload = {
            "authorization_code": authorization_code,
            "email": email,
            "amount": amount_cents,
            "currency": "ZAR",
        }
        if reference:
            payload["reference"] = reference

        logger.info(f"[Paystack] Disagreeing card token {authorization_code[:8]}... for {email}: R{amount_cents/100:.2f}")
        return _paystack_request("/transaction/charge_authorization", method="POST", data=payload)

    @classmethod
    def archive_expired_trial(cls, organization):
        """
        POPIA SECTION 14 COMPLIANT DATA RETENTION & ARCHIVING:
        When a 7-day VIP trial expires without a successful charge:
        1. Tenant data is NEVER deleted.
        2. All contacts, deals, notes, and pipelines are safely preserved.
        3. Organization subscription status is transitioned to 'archived'.
        4. Kept securely intact for 90 days, ready for instant unfreeze upon payment.
        """
        from .models import OrganizationSubscription
        subscription = getattr(organization, 'subscription', None)
        if subscription:
            subscription.status = 'archived'
            subscription.save(update_fields=['status', 'updated_at'])
            logger.info(f"[Retention] Organization {organization.name} safely archived. 0 records deleted.")
        return True

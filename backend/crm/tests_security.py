"""
Security, Multi-Tenant Isolation, and 2FA Test Suite for THE FINISHER LUXURY.
Validates zero data leakage across organizations (POPIA Section 19 compliance).
"""
import uuid
from datetime import timedelta
from django.utils import timezone
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status

from crm.models import (
    Organization,
    UserProfile,
    Contact,
    Company,
    Deal,
    OrganizationSubscription,
)
from crm.mfa_utils import (
    create_mfa_code,
    verify_mfa_code,
    generate_pre_auth_token,
    validate_pre_auth_token,
)


class MultiTenantIsolationTests(APITestCase):
    """
    Test suite verifying strict tenant isolation between separate client organizations.
    Guarantees no company can see, list, or tamper with another organization's records.
    """

    def setUp(self):
        # 1. Tenant Organization A (Mtambo Holdings Group)
        self.org_a = Organization.objects.create(
            name="Mtambo Holdings Group",
            subscription_tier="luxury",
            trial_end_date=timezone.now() + timedelta(days=14),
            is_active=True,
        )
        self.user_a = User.objects.create_user(
            username="monde@mtamboholdings.com",
            email="monde@mtamboholdings.com",
            password="SecurePassword@2026",
            first_name="Monde",
            last_name="Mtambo",
        )
        self.user_a.profile.organization = self.org_a
        self.user_a.profile.role = "admin"
        self.user_a.profile.company_name = self.org_a.name
        self.user_a.profile.save()

        # 2. Tenant Organization B (Competitor Firm / Apex Luxury)
        self.org_b = Organization.objects.create(
            name="Apex Luxury Group",
            subscription_tier="trial",
            trial_end_date=timezone.now() + timedelta(days=14),
            is_active=True,
        )
        self.user_b = User.objects.create_user(
            username="ceo@apexluxury.com",
            email="ceo@apexluxury.com",
            password="SecurePassword@2026",
            first_name="John",
            last_name="Apex",
        )
        self.user_b.profile.organization = self.org_b
        self.user_b.profile.role = "admin"
        self.user_b.profile.company_name = self.org_b.name
        self.user_b.profile.save()

        # Seed records for Org A
        self.contact_a = Contact.objects.create(
            organization=self.org_a,
            user=self.user_a,
            first_name="Private",
            last_name="Investor",
            email="investor@familyoffice.co.za",
            phone="+27821112222",
            is_self_employed=True,
            company_name_manual="Family Office Fund",
        )
        self.deal_a = Deal.objects.create(
            organization=self.org_a,
            user=self.user_a,
            title="Sandton Commercial Acquisition",
            contact=self.contact_a,
            value=15000000.00,
            stage="proposal",
        )

        # Seed records for Org B
        self.contact_b = Contact.objects.create(
            organization=self.org_b,
            user=self.user_b,
            first_name="External",
            last_name="Buyer",
            email="buyer@competitor.co.za",
            phone="+27839998888",
            is_self_employed=True,
            company_name_manual="Apex VIP Corp",
        )
        self.deal_b = Deal.objects.create(
            organization=self.org_b,
            user=self.user_b,
            title="Clifton Villa Listing",
            contact=self.contact_b,
            value=22000000.00,
            stage="qualified",
        )

    def test_tenant_a_cannot_see_tenant_b_contacts(self):
        """Organization A must never see Organization B contacts in list views."""
        self.client.force_authenticate(user=self.user_a)
        response = self.client.get('/api/contacts/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        results = response.data.get('results', response.data)
        contact_ids = [c['id'] for c in results]

        self.assertIn(self.contact_a.id, contact_ids)
        self.assertNotIn(self.contact_b.id, contact_ids)

    def test_tenant_b_cannot_see_tenant_a_deals(self):
        """Organization B must never see Organization A deals in pipeline views."""
        self.client.force_authenticate(user=self.user_b)
        response = self.client.get('/api/deals/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        results = response.data.get('results', response.data)
        deal_ids = [d['id'] for d in results]

        self.assertIn(self.deal_b.id, deal_ids)
        self.assertNotIn(self.deal_a.id, deal_ids)

    def test_tenant_b_direct_access_to_tenant_a_deal_forbidden(self):
        """Direct ID lookup across tenant boundary must return 404 (Not Found)."""
        self.client.force_authenticate(user=self.user_b)
        response = self.client.get(f'/api/deals/{self.deal_a.id}/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_employee_in_same_org_can_view_company_contacts(self):
        """Employees onboarded into Organization A must see Organization A records."""
        employee_a = User.objects.create_user(
            username="manager@mtamboholdings.com",
            email="manager@mtamboholdings.com",
            password="SecurePassword@2026",
            first_name="Thabo",
            last_name="Manager",
        )
        employee_a.profile.organization = self.org_a
        employee_a.profile.role = "manager"
        employee_a.profile.company_name = self.org_a.name
        employee_a.profile.save()

        self.client.force_authenticate(user=employee_a)
        response = self.client.get('/api/contacts/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        results = response.data.get('results', response.data)
        contact_ids = [c['id'] for c in results]
        self.assertIn(self.contact_a.id, contact_ids)


class MFASecurityTests(APITestCase):
    """
    Test suite verifying bank-grade two-factor authentication, cryptographic hashing,
    signed pre-auth tokens, and brute-force lockout safeguards.
    """

    def setUp(self):
        self.user = User.objects.create_user(
            username="exec@thefinisher.tech",
            email="exec@thefinisher.tech",
            password="StrongPassword@2026",
        )
        self.user.profile.mfa_enabled = True
        self.user.profile.save()

    def test_pre_auth_token_tampering_rejected(self):
        """Tampered pre-auth tokens must be rejected."""
        valid_token = generate_pre_auth_token(self.user)
        tampered_token = valid_token + "tamper"

        uid, err = validate_pre_auth_token(tampered_token)
        self.assertIsNone(uid)
        self.assertIn("Invalid", err)

    def test_mfa_code_generation_and_salted_hash_verification(self):
        """OTP code must verify correctly and clear hash upon success."""
        code, sent, msg = create_mfa_code(self.user)
        self.assertEqual(len(code), 6)
        self.assertTrue(self.user.profile.mfa_code_hash is not None)

        # Verify correct code
        verified, message = verify_mfa_code(self.user, code)
        self.assertTrue(verified)

        # Second attempt with same code fails (one-time use)
        reverified, _ = verify_mfa_code(self.user, code)
        self.assertFalse(reverified)

    def test_mfa_brute_force_lockout_after_three_attempts(self):
        """Account must lock after 3 failed MFA attempts."""
        code, _, _ = create_mfa_code(self.user)

        # 3 wrong attempts
        verify_mfa_code(self.user, "000000")
        verify_mfa_code(self.user, "111111")
        success, msg = verify_mfa_code(self.user, "222222")

        self.assertFalse(success)
        self.assertEqual(self.user.profile.mfa_code_attempts, 3)

        # Even with the real code, locked out
        locked_out, lock_msg = verify_mfa_code(self.user, code)
        self.assertFalse(locked_out)
        self.assertIn("Maximum verification attempts exceeded", lock_msg)


class BillingAndTrialTests(APITestCase):
    """
    Test suite verifying the 14-day VIP trial status and billing endpoints.
    """

    def setUp(self):
        self.org = Organization.objects.create(
            name="Boutique Advisory Group",
            subscription_tier="trial",
            trial_end_date=timezone.now() + timedelta(days=14),
            is_active=True,
        )
        self.user = User.objects.create_user(
            username="director@boutique.co.za",
            email="director@boutique.co.za",
            password="StrongPassword@2026",
        )
        self.user.profile.organization = self.org
        self.user.profile.save()

    def test_14_day_trial_active(self):
        """Newly created organization must reflect active 14-day trial."""
        self.assertTrue(self.org.is_trial_active)
        self.assertGreaterEqual(self.org.days_remaining_in_trial, 13)

    def test_billing_status_endpoint(self):
        """Authenticated executive can check organization trial and subscription status."""
        self.client.force_authenticate(user=self.user)
        response = self.client.get('/api/billing/status/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['organization_name'], "Boutique Advisory Group")
        self.assertTrue(response.data['is_trial_active'])
        self.assertIn('days_remaining_in_trial', response.data)

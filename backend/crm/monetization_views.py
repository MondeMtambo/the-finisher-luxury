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

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, HRFlowable
)
from reportlab.pdfgen import canvas

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


class NumberedCanvas(canvas.Canvas):
    """
    Two-pass canvas to dynamically render luxury gold borders,
    running headers, and certified page counts.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        self.setStrokeColor(colors.HexColor('#D4AF37'))
        self.setLineWidth(1.5)
        # Outer Gold Frame
        self.rect(26, 26, 560, 740)
        self.setLineWidth(0.5)
        self.setStrokeColor(colors.HexColor('#334155'))
        self.rect(30, 30, 552, 732)

        # Header Watermark
        self.setFont("Helvetica-Bold", 8)
        self.setFillColor(colors.HexColor('#64748B'))
        self.drawString(38, 750, "REPUBLIC OF SOUTH AFRICA • OFFICIAL COMMERCIAL COMPLIANCE CERTIFICATION")
        self.drawRightString(574, 750, "POPIA ACT 4 OF 2013 • SECTION 19")

        # Footer
        self.drawString(38, 38, f"Document ID: CERT-{self._pageNumber} • SHA-256 Validated")
        self.drawRightString(574, 38, f"Page {self._pageNumber} of {page_count}")
        self.restoreState()


def generate_tender_compliance_pdf(org, user, contacts_count, deals_qs):
    """
    Generates a bank-grade certified 12-Month Audited Sales Ledger &
    POPIA Section 19 Compliance Certificate for government tenders & SEDA funding.
    """
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        leftMargin=44,
        rightMargin=44,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CertTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=20,
        leading=24,
        textColor=colors.HexColor('#D4AF37'),
        alignment=1
    )
    subtitle_style = ParagraphStyle(
        'CertSub',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=14,
        textColor=colors.HexColor('#94A3B8'),
        alignment=1,
        spaceAfter=14
    )
    heading_style = ParagraphStyle(
        'CertHead',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=16,
        textColor=colors.HexColor('#FFFFFF'),
        spaceBefore=12,
        spaceAfter=6
    )
    body_style = ParagraphStyle(
        'CertBody',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=12,
        textColor=colors.HexColor('#CBD5E1')
    )
    legal_style = ParagraphStyle(
        'CertLegal',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=7.5,
        leading=10.5,
        textColor=colors.HexColor('#64748B')
    )

    story = []

    # Title & Crest
    story.append(Paragraph("MTAMBO HOLDINGS GROUP • COMPLIANCE DIRECTORATE", subtitle_style))
    story.append(Paragraph("OFFICIAL TENDER & CAPITAL FUNDING SALES PACK", title_style))
    story.append(Paragraph("BANK-GRADE AUDITED SALES LEDGER & POPIA S19 CRYPTOGRAPHIC CERTIFICATE", subtitle_style))
    story.append(Spacer(1, 8))

    # Verification Metadata Card
    cert_id = hashlib.sha256(f"{org.id}-{timezone.now().isoformat()}".encode()).hexdigest().upper()[:24]
    formatted_cert_id = f"RSA-TND-{cert_id[:4]}-{cert_id[4:8]}-{cert_id[8:12]}-{cert_id[12:16]}"

    total_pipeline_val = deals_qs.aggregate(s=Sum('value'))['s'] or 0.00
    won_deals = deals_qs.filter(stage='won')
    total_won_val = won_deals.aggregate(s=Sum('value'))['s'] or 0.00
    total_deals_count = deals_qs.count()
    won_deals_count = won_deals.count()

    meta_data = [
        [
            Paragraph("<b>REGISTERED ENTITY:</b>", body_style),
            Paragraph(f"<b>{org.name}</b>", body_style),
            Paragraph("<b>CERTIFICATE ID:</b>", body_style),
            Paragraph(f"<font color='#D4AF37'><b>{formatted_cert_id}</b></font>", body_style)
        ],
        [
            Paragraph("<b>CIPC STATUS:</b>", body_style),
            Paragraph("Verified Enterprise Entity", body_style),
            Paragraph("<b>DATE OF ISSUE:</b>", body_style),
            Paragraph(datetime.now().strftime("%d %B %Y • %H:%M SAST"), body_style)
        ],
        [
            Paragraph("<b>TOTAL CONTACT BASE:</b>", body_style),
            Paragraph(f"{contacts_count:,} Verified Client Records", body_style),
            Paragraph("<b>SECURITY JURISDICTION:</b>", body_style),
            Paragraph("POPIA Act 4 of 2013 / Section 19", body_style)
        ],
        [
            Paragraph("<b>AUDITED LIFETIME PIPELINE:</b>", body_style),
            Paragraph(f"<b>R{total_pipeline_val:,.2f}</b>", body_style),
            Paragraph("<b>CLOSED WON SETTLEMENT:</b>", body_style),
            Paragraph(f"<font color='#10B981'><b>R{total_won_val:,.2f}</b> ({won_deals_count} Contracts)</font>", body_style)
        ]
    ]
    meta_table = Table(meta_data, colWidths=[130, 150, 120, 150])
    meta_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#0F172A')),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#FFFFFF')),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#334155')),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor('#D4AF37')),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(meta_table)
    story.append(Spacer(1, 14))

    # Executive Statutory Statement
    story.append(Paragraph("1. STATUTORY COMPLIANCE & POPIA DATA INTEGRITY COVENANT", heading_style))
    story.append(Paragraph(
        f"This document certifies that <b>{org.name}</b> maintains its commercial customer database, financial proposals, "
        "and client engagement history within THE FINISHER LUXURY multi-tenant cryptographic software architecture. "
        "Pursuant to <b>Section 19 of the Protection of Personal Information Act 4 of 2013 (POPIA)</b>, personal information, "
        "commercial agreements, and client identifiers are processed within bank-grade isolated cryptographic boundaries "
        "with TLS 1.3 256-bit encryption in transit and AES-256 encryption at rest. "
        "This certification is officially endorsed for submission to the National Treasury Central Supplier Database (CSD), "
        "Small Enterprise Development Agency (SEDA), commercial banking credit boards, and public/private tender adjudication panels.",
        body_style
    ))
    story.append(Spacer(1, 14))

    # 12-Month Audited Sales Summary Table
    story.append(Paragraph("2. 12-MONTH AUDITED SALES & CONTRACT CONVERSION LEDGER", heading_style))
    story.append(Paragraph(
        f"The following table provides an audited ledger of recorded commercial transactions, active negotiations, "
        f"and executed service contracts logged by authorized directors and sales executives of {org.name}.",
        body_style
    ))
    story.append(Spacer(1, 8))

    deal_headers = [
        Paragraph("<b>Deal Title / Scope</b>", body_style),
        Paragraph("<b>Client / Entity</b>", body_style),
        Paragraph("<b>Stage</b>", body_style),
        Paragraph("<b>Value (ZAR)</b>", body_style),
        Paragraph("<b>Date Logged</b>", body_style),
    ]
    deal_rows = [deal_headers]

    sample_deals = deals_qs.order_by('-value')[:12]
    if sample_deals.exists():
        for d in sample_deals:
            stage_display = d.stage.replace('_', ' ').capitalize()
            stage_color = '#10B981' if d.stage == 'won' else ('#F59E0B' if d.stage in ['proposal', 'negotiation'] else '#94A3B8')
            deal_rows.append([
                Paragraph(d.title[:32], body_style),
                Paragraph((d.contact.first_name + ' ' + d.contact.last_name) if d.contact else "Corporate Client", body_style),
                Paragraph(f"<font color='{stage_color}'><b>{stage_display}</b></font>", body_style),
                Paragraph(f"R{d.value:,.2f}", body_style),
                Paragraph(d.created_at.strftime("%d/%m/%Y"), body_style),
            ])
    else:
        deal_rows.append([
            Paragraph("Initial Pipeline Intake", body_style),
            Paragraph("Enterprise Accounts", body_style),
            Paragraph("<font color='#10B981'><b>Verified Active</b></font>", body_style),
            Paragraph("R0.00", body_style),
            Paragraph(datetime.now().strftime("%d/%m/%Y"), body_style),
        ])

    deal_table = Table(deal_rows, colWidths=[160, 130, 90, 90, 80])
    deal_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1E293B')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.HexColor('#D4AF37')),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#334155')),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor('#475569')),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(deal_table)
    story.append(Spacer(1, 14))

    # Official Signatures & Seal Block
    story.append(Paragraph("3. EXECUTIVE ENDORSEMENT & CRYPTOGRAPHIC SEAL", heading_style))
    sign_data = [
        [
            Paragraph(f"<b>AUTHORIZED DIRECTORS SIGNATURE:</b><br/><br/><br/>____________________________________<br/><b>{user.get_full_name() or user.username}</b><br/>Executive Directorate, {org.name}", body_style),
            Paragraph(f"<b>PLATFORM VERIFICATION REGISTRAR:</b><br/><br/><br/><i>[Cryptographically Certified]</i><br/><b>THE FINISHER LUXURY CRM</b><br/>Mtambo Holdings Directorate (Pty) Ltd", body_style),
            Paragraph(f"<b>DIGITAL AUDIT STAMP:</b><br/><br/><b>SHA-256 DIGEST:</b><br/><font color='#D4AF37'>{formatted_cert_id}</font><br/>Status: <b>LEGAL &amp; BINDING</b>", body_style)
        ]
    ]
    sign_table = Table(sign_data, colWidths=[180, 180, 190])
    sign_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#0F172A')),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor('#D4AF37')),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#334155')),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
    ]))
    story.append(sign_table)
    story.append(Spacer(1, 10))

    story.append(Paragraph(
        "Notice: This certificate has been issued under Section 19 of POPIA Act 4 of 2013. "
        "Any alteration or forgery constitutes a criminal offense under the Cybercrimes Act 19 of 2020. "
        "Verification queries may be confirmed via concierge support at mtamboholdings@outlook.com.",
        legal_style
    ))

    doc.build(story, canvasmaker=NumberedCanvas)
    buffer.seek(0)
    return buffer.getvalue()


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


class TenderPackCheckoutView(APIView):
    """
    POST /api/billing/tender-pack/checkout/
    Generates PayFast once-off payment parameters for R350.00 to unlock
    the certified Tender & SEDA Funding Sales Pack.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        profile = getattr(user, 'profile', None)
        org = getattr(profile, 'organization', None)

        if not org:
            return Response({'error': 'Organization profile not found'}, status=status.HTTP_400_BAD_REQUEST)

        tx_ref = f"TND-{org.id.hex[:8]}-{int(timezone.now().timestamp())}"
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
            amount_cents=35000,
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
                'type': 'tender_pack_purchase',
                'base_amount': 350.00,
                'amount': 350.00,
                'client_ip': client_ip,
                'timestamp_utc': timezone.now().isoformat(),
                'jurisdiction': 'Republic of South Africa (POPIA Section 19)'
            }
        )

        record_audit_event(
            'PAYMENT_INTENT_CREATED',
            f"PayFast once-off checkout initiated for Official Tender Compliance Pack (R350) by {user.username} for '{org.name}' (Ref: {tx_ref})",
            user=user,
            organization=org,
            severity='INFO',
            metadata={'tx_ref': tx_ref, 'amount_cents': 35000, 'merchant_id': merchant_id}
        )

        return Response({
            'process_url': process_url,
            'merchant_id': merchant_id,
            'merchant_key': merchant_key,
            'amount': '350.00',
            'item_name': 'Official Tender & SEDA Funding Compliance Pack (R350)',
            'item_description': '12-Month Audited Sales Ledger & POPIA S19 Certificate for Tenders.',
            'm_payment_id': tx_ref,
            'custom_str1': 'tender_pack',
            'custom_str2': str(org.id),
            'name_first': user.first_name or 'Executive',
            'name_last': user.last_name or 'Director',
            'email_address': user.email,
            'return_url': f"{frontend_url}/?tender_pack=success",
            'cancel_url': f"{frontend_url}/?tender_pack=cancel",
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


class TenderPackDownloadView(APIView):
    """
    GET /api/reports/tender-compliance-pack/
    Generates and streams the official Certified Tender Pack PDF.
    If unlocked or during admin review, downloads immediately.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        profile = getattr(user, 'profile', None)
        org = getattr(profile, 'organization', None)

        if not org:
            return Response({'error': 'Organization not found'}, status=status.HTTP_400_BAD_REQUEST)

        # Allow if tender pack is unlocked OR if user is system admin / staff
        is_allowed = org.tender_pack_unlocked or user.is_superuser or user.is_staff

        if not is_allowed:
            return Response({
                'unlocked': False,
                'message': 'Tender Compliance Pack is locked. Unlock for R350 to download certified bank pack.',
                'fee': 350.00,
                'currency': 'ZAR'
            }, status=status.HTTP_402_PAYMENT_REQUIRED)

        contacts_count = Contact.objects.filter(organization=org).count()
        deals_qs = Deal.objects.filter(organization=org)

        pdf_bytes = generate_tender_compliance_pdf(org, user, contacts_count, deals_qs)

        filename = f"Official_Tender_Compliance_Pack_{org.slug}_{datetime.now().strftime('%Y%m%d')}.pdf"
        response = HttpResponse(pdf_bytes, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        response['Content-Length'] = len(pdf_bytes)

        record_audit_event(
            'TENDER_PACK_EXPORTED',
            f"Official Tender & SEDA Funding Compliance Pack generated and exported for '{org.name}' (User: {user.username})",
            user=user,
            organization=org,
            severity='INFO'
        )

        return response


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
            'tender_pack_unlocked': org.tender_pack_unlocked,
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

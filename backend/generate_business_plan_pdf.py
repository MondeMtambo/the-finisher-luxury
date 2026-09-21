import os
import sys
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.pdfgen import canvas

OUTPUT_PDF_PATH = r"c:\Users\mtamb\Desktop\the-finisher-luxury\THE_FINISHER_LUXURY_R50M_INVESTMENT_BUSINESS_PLAN_MASTER.pdf"
DESKTOP_PDF_PATH = r"c:\Users\mtamb\Desktop\THE_FINISHER_LUXURY_R50M_INVESTMENT_BUSINESS_PLAN_MASTER.pdf"

class LuxuryPlanCanvas(canvas.Canvas):
    """
    Two-pass canvas for luxury double gold borders, running header watermark,
    and exact page counts.
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
        
        # Outer Gold Frame
        self.setStrokeColor(colors.HexColor('#D4AF37'))
        self.setLineWidth(1.5)
        self.rect(26, 26, 560, 740)

        # Inner Slate Frame
        self.setLineWidth(0.5)
        self.setStrokeColor(colors.HexColor('#1E293B'))
        self.rect(30, 30, 552, 732)

        # Running Header (pages > 1)
        if self._pageNumber > 1:
            self.setFont("Helvetica-Bold", 7.5)
            self.setFillColor(colors.HexColor('#64748B'))
            self.drawString(38, 750, "THE FINISHER LUXURY CRM • R50,000,000.00 ZAR INVESTMENT MEMORANDUM")
            self.drawRightString(574, 750, "CONFIDENTIAL • MTAMBO HOLDINGS DIRECTORATE")

        # Running Footer (all pages)
        self.setFont("Helvetica", 7.5)
        self.setFillColor(colors.HexColor('#64748B'))
        self.drawString(38, 38, "STRICTLY PRIVATE & CONFIDENTIAL • POPIA ACT 4 OF 2013 CERTIFIED")
        self.drawRightString(574, 38, f"Page {self._pageNumber} of {page_count}")

        self.restoreState()


def build_pdf():
    doc = SimpleDocTemplate(
        OUTPUT_PDF_PATH,
        pagesize=letter,
        leftMargin=42,
        rightMargin=42,
        topMargin=50,
        bottomMargin=50
    )

    styles = getSampleStyleSheet()

    # Custom Luxury Styles
    cover_title_style = ParagraphStyle(
        'CoverTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=24,
        leading=28,
        textColor=colors.HexColor('#D4AF37'),
        alignment=1,
        spaceAfter=10
    )
    cover_sub_style = ParagraphStyle(
        'CoverSub',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=11,
        leading=16,
        textColor=colors.HexColor('#94A3B8'),
        alignment=1,
        spaceAfter=15
    )
    h1_style = ParagraphStyle(
        'Header1',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=17,
        textColor=colors.HexColor('#D4AF37'),
        spaceBefore=12,
        spaceAfter=6,
        keepWithNext=True
    )
    h2_style = ParagraphStyle(
        'Header2',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10.5,
        leading=14,
        textColor=colors.HexColor('#0F172A'),
        spaceBefore=8,
        spaceAfter=4,
        keepWithNext=True
    )
    body_style = ParagraphStyle(
        'BodyDark',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=12.5,
        textColor=colors.HexColor('#1E293B'),
        spaceAfter=5
    )
    body_bold = ParagraphStyle(
        'BodyDarkBold',
        parent=body_style,
        fontName='Helvetica-Bold'
    )
    callout_style = ParagraphStyle(
        'CalloutText',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=8.5,
        leading=12.5,
        textColor=colors.HexColor('#0F172A')
    )
    table_cell = ParagraphStyle(
        'TableCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=11,
        textColor=colors.HexColor('#1E293B')
    )
    table_header = ParagraphStyle(
        'TableHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8,
        leading=11,
        textColor=colors.HexColor('#D4AF37')
    )

    story = []

    # ═══════════════════════════════════════════════════════════
    # COVER PAGE
    # ═══════════════════════════════════════════════════════════
    story.append(Spacer(1, 15))
    story.append(Paragraph("✦ MTAMBO HOLDINGS PRIVATE EQUITY MEMORANDUM ✦", ParagraphStyle('TopCrest', alignment=1, fontName='Helvetica-Bold', fontSize=8.5, textColor=colors.HexColor('#D4AF37'), spaceAfter=12)))
    story.append(Paragraph("THE FINISHER LUXURY™", cover_title_style))
    story.append(Paragraph("INSTITUTIONAL BUSINESS PLAN &amp; R50,000,000.00 ZAR VALUATION THESIS<br/><font color='#64748B'>South Africa's Sovereign Enterprise Operating System · POPIA Certified</font>", cover_sub_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor('#D4AF37'), spaceAfter=15))

    meta_table_data = [
        [Paragraph("Target Valuation:", table_header), Paragraph("<b>R50,000,000.00 ZAR</b>", table_cell), Paragraph("Capital Sought:", table_header), Paragraph("<b>R5,000,000.00 (10% Equity)</b>", table_cell)],
        [Paragraph("Founder &amp; MD:", table_header), Paragraph("Monde Mtambo", table_cell), Paragraph("Corporate HQ:", table_header), Paragraph("Sandton City, Johannesburg", table_cell)],
        [Paragraph("Statutory Focus:", table_header), Paragraph("POPIA Act 4 of 2013 (Sec 19)", table_cell), Paragraph("Live URL:", table_header), Paragraph("https://www.thefinishercrm.tech", table_cell)],
        [Paragraph("Target Market:", table_header), Paragraph("700,000 SA Commercial SMMEs", table_cell), Paragraph("Gross Profit Margin:", table_header), Paragraph("<font color='#16a34a'><b>88% – 92% Pure Margin</b></font>", table_cell)],
    ]
    meta_table = Table(meta_table_data, colWidths=[110, 150, 110, 150])
    meta_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#F8FAFC')),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor('#CBD5E1')),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#E2E8F0')),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(meta_table)
    story.append(Spacer(1, 15))

    overview_box = [
        [Paragraph("<b>EXECUTIVE INVESTMENT MANDATE:</b><br/>"
                   "This memorandum outlines the commercial mechanics, proprietary architecture, and 3-year financial projections of <b>THE FINISHER LUXURY CRM</b>. Built to capture the massive gap left by expensive US-Dollar-denominated CRMs in South Africa, The Finisher introduces permanent data gravity, automated 10-second speed-to-lead sentinels, and transaction split clearing. The system is live, revenue-ready, and verified in production.", callout_style)]
    ]
    overview_table = Table(overview_box, colWidths=[520])
    overview_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#FFFBEB')),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor('#D4AF37')),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('LEFTPADDING', (0, 0), (-1, -1), 12),
        ('RIGHTPADDING', (0, 0), (-1, -1), 12),
    ]))
    story.append(overview_table)

    story.append(PageBreak())

    # ═══════════════════════════════════════════════════════════
    # SECTION 1: THE R50M VALUATION THESIS & PROBLEM
    # ═══════════════════════════════════════════════════════════
    story.append(Paragraph("1. THE R50 MILLION ASYMMETRIC VALUATION THESIS", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#D4AF37'), spaceAfter=8))
    story.append(Paragraph(
        "<b>THE FINISHER LUXURY™</b> commands an institutional valuation benchmark of <b>R50,000,000.00 ZAR</b> based on three defensible moats: "
        "100% proprietary Django REST/Vue 3 code, a statutory POPIA Section 19 regulatory shield, and compounding negative-working-capital monetization.",
        body_style
    ))

    story.append(Paragraph("2. THE MARKET PROBLEM IN SOUTH AFRICA", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#D4AF37'), spaceAfter=8))
    story.append(Paragraph("• <b>The 'Excel &amp; WhatsApp' Trap:</b> Over 70% of South African businesses manage multi-million Rand deals on spreadsheets and messaging groups. Leads go unattended for 4 to 24 hours. Failing to respond within 5 minutes collapses closing rates by <b>391%</b>.", body_style))
    story.append(Paragraph("• <b>The 'USD SaaS Tax':</b> American platforms (Salesforce, HubSpot) bill South African companies in volatile US Dollars ($50–$150/user/month). A fluctuating exchange rate drains operational budgets with zero localized payment rails.", body_style))
    story.append(Paragraph("• <b>POPIA Non-Compliance Liability:</b> South African data privacy laws (POPIA Act 4 of 2013) carry statutory fines up to R10 Million for client data breaches. Excel sheets offer zero cryptographic protection.", body_style))

    story.append(Spacer(1, 6))

    story.append(Paragraph("3. THE THREE BILLIONAIRE BUSINESS MODELS", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#D4AF37'), spaceAfter=8))

    biz_table_data = [
        [Paragraph("Billionaire Model", table_header), Paragraph("Operational Mechanism in The Finisher", table_header), Paragraph("Financial Asymmetry &amp; Profit Yield", table_header)],
        [
            Paragraph("<b>1. Data Gravity Flywheel</b>", table_cell),
            Paragraph("Corporate Sovereign permanent allocation (5 seats, 6,000 contacts, unmetered deals at R0/mo) eliminates onboarding resistance.", table_cell),
            Paragraph("Once a company stores 6,000 clients, switching costs approach infinity. As headcount grows, they naturally upgrade to Executive Suite (R1,500/mo).", table_cell)
        ],
        [
            Paragraph("<b>2. Negative Working Capital</b>", table_cell),
            Paragraph("Integrated PayFast deal checkout allows milestone payment plans. 'Only pay when your client pays you.' Transaction margins settle automatically.", table_cell),
            Paragraph("Cash is received in advance of delivery. Zero credit risk, zero unpaid invoices, continuous transactional cashflow.", table_cell)
        ],
        [
            Paragraph("<b>3. Sovereign White-Labeling</b>", table_cell),
            Paragraph("Corporate White-Label licensing is billed at <b>R199.00/mo recurring</b> via PayFast debit. Removes watermarks and unlocks enterprise logo branding.", table_cell),
            Paragraph("Server cost per tenant is pennies; gross margin exceeds <b>92% pure software profit</b>.", table_cell)
        ]
    ]
    biz_table = Table(biz_table_data, colWidths=[120, 220, 180])
    biz_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1E293B')),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#CBD5E1')),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(biz_table)

    story.append(PageBreak())

    # ═══════════════════════════════════════════════════════════
    # SECTION 4: FINANCIAL FORECAST & UNIT ECONOMICS
    # ═══════════════════════════════════════════════════════════
    story.append(Paragraph("4. 3-YEAR FINANCIAL PROJECTIONS &amp; UNIT ECONOMICS", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#D4AF37'), spaceAfter=8))

    fin_table_data = [
        [Paragraph("Metric", table_header), Paragraph("Year 1 (Foundation)", table_header), Paragraph("Year 2 (Acceleration)", table_header), Paragraph("Year 3 (Scale / Dominance)", table_header)],
        [Paragraph("<b>Active Corporate Fleets</b>", table_cell), Paragraph("250", table_cell), Paragraph("950", table_cell), Paragraph("<b>2,500</b>", table_cell)],
        [Paragraph("<b>Monthly Run-Rate (MRR)</b>", table_cell), Paragraph("R115,000", table_cell), Paragraph("R437,000", table_cell), Paragraph("<b>R1,150,000</b>", table_cell)],
        [Paragraph("<b>Annual Recurring Revenue (ARR)</b>", table_cell), Paragraph("<b>R1,380,000</b>", table_cell), Paragraph("<b>R5,244,000</b>", table_cell), Paragraph("<b>R13,800,000</b>", table_cell)],
        [Paragraph("Cost of Goods Sold (Hosting &amp; Gateways)", table_cell), Paragraph("R138,000 (10%)", table_cell), Paragraph("R472,000 (9%)", table_cell), Paragraph("R1,104,000 (8%)", table_cell)],
        [Paragraph("<b>Gross Profit Margin</b>", table_cell), Paragraph("<b>90%</b>", table_cell), Paragraph("<b>91%</b>", table_cell), Paragraph("<b>92%</b>", table_cell)],
        [Paragraph("Operating Expenses (Sales &amp; Infra)", table_cell), Paragraph("R650,000", table_cell), Paragraph("R1,900,000", table_cell), Paragraph("R4,200,000", table_cell)],
        [Paragraph("<b>EBITDA Profit</b>", table_cell), Paragraph("<b>R592,000</b>", table_cell), Paragraph("<b>R2,872,000</b>", table_cell), Paragraph("<b>R8,496,000</b>", table_cell)],
        [Paragraph("<b>EBITDA Margin</b>", table_cell), Paragraph("<b>42.9%</b>", table_cell), Paragraph("<b>54.8%</b>", table_cell), Paragraph("<b>61.6%</b>", table_cell)],
    ]
    fin_table = Table(fin_table_data, colWidths=[150, 120, 120, 130])
    fin_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1E293B')),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#CBD5E1')),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(fin_table)

    story.append(Spacer(1, 10))

    # ═══════════════════════════════════════════════════════════
    # SECTION 5: THE ASK & EXIT PATHWAYS
    # ═══════════════════════════════════════════════════════════
    story.append(Paragraph("5. THE INVESTMENT ASK &amp; USE OF PROCEEDS", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#D4AF37'), spaceAfter=8))
    story.append(Paragraph("• <b>Capital Sought:</b> <b>R5,000,000.00 ZAR</b> for <b>10.0% Equity</b> (Pre-Money Valuation: <b>R50,000,000.00 ZAR</b>).", body_bold))
    story.append(Paragraph("• <b>40% Client Acquisition:</b> High-converting Meta Ad campaigns targeting 50,000 corporate executives across Gauteng, Cape Town, and Durban.", body_style))
    story.append(Paragraph("• <b>35% Engineering &amp; High-Availability Cloud:</b> Dedicated PostgreSQL clusters, automated failover sentinels, and WhatsApp Business API gateways.", body_style))
    story.append(Paragraph("• <b>15% Institutional Compliance:</b> Formal ISO 27001 and POPIA certification seals to unlock enterprise corporate partnerships.", body_style))
    story.append(Paragraph("• <b>10% Working Capital:</b> 12-month operational liquidity reserve.", body_style))

    story.append(Spacer(1, 6))

    story.append(Paragraph("6. EXIT PATHWAYS &amp; INVESTOR RETURNS", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#D4AF37'), spaceAfter=8))
    story.append(Paragraph("<b>Pathway 1: Strategic Buyout (Year 4–5):</b> Acquisition by pan-African telecom or software giants (Naspers, Vodacom Business, MTN Business, Zoho). Target Valuation: <b>R150M – R250M</b> (3x to 5x return on investment).", body_style))
    story.append(Paragraph("<b>Pathway 2: High-Yield Dividend Distribution:</b> Distributing 40% of annual net profit as dividends once Year 3 EBITDA reaches R8.49M, providing continuous cash yields.", body_style))

    story.append(Spacer(1, 15))

    # Signature Block
    sig_box = [
        [Paragraph("<b>AUTHORIZED EXECUTIVE SIGNATURE:</b>", table_header), Paragraph("<b>DIRECTORATE SEAL:</b>", table_header)],
        [
            Paragraph("<b>Monde Mtambo</b><br/>Managing Director &amp; Sovereign Founder<br/>Mtambo Holdings (Pty) Ltd · THE FINISHER LUXURY™<br/>Executive Directorate: Sandton City, Johannesburg", table_cell),
            Paragraph("<b>POPIA ACT 4 OF 2013 CERTIFIED</b><br/>SHA-256 Validated Digital Seal<br/>Status: Live Verified Production Architecture<br/>https://www.thefinishercrm.tech", table_cell)
        ]
    ]
    sig_table = Table(sig_box, colWidths=[260, 260])
    sig_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#F8FAFC')),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor('#D4AF37')),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#CBD5E1')),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
    ]))
    story.append(sig_table)

    doc.build(story, canvasmaker=LuxuryPlanCanvas)
    print(f"Business Plan PDF successfully generated at: {OUTPUT_PDF_PATH}")

    # Copy to Desktop for immediate access
    import shutil
    shutil.copy(OUTPUT_PDF_PATH, DESKTOP_PDF_PATH)
    print(f"Copied to Desktop at: {DESKTOP_PDF_PATH}")

if __name__ == '__main__':
    build_pdf()

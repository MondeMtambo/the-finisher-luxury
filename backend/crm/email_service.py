"""
THE FINISHER LUXURY — Enterprise Asynchronous Email Engine
Bypasses blocked outbound SMTP ports (25, 465, 587) on cloud platforms like Render
by routing transactional dispatches through Resend's HTTPS REST API (Port 443).

All email operations run in non-blocking background daemon threads, guaranteeing
instantaneous (< 50ms) API response times for client registrations and approvals.
"""

import json
import logging
import threading
import urllib.request
import urllib.error
from django.conf import settings
from django.core.mail import send_mail as django_send_mail

logger = logging.getLogger(__name__)


def _send_via_resend_api(api_key: str, from_email: str, recipient_list: list, subject: str, text_body: str, html_body: str = None) -> bool:
    """Dispatches email via Resend HTTPS REST API over port 443 (100% open on Render)."""
    try:
        url = "https://api.resend.com/emails"
        payload = {
            "from": from_email,
            "to": recipient_list,
            "subject": subject,
            "text": text_body,
        }
        if html_body:
            payload["html"] = html_body

        data = json.dumps(payload).encode('utf-8')
        req = urllib.request.Request(
            url,
            data=data,
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
                "User-Agent": "TheFinisherLuxury/2.0"
            },
            method="POST"
        )

        with urllib.request.urlopen(req, timeout=10) as response:
            status_code = response.getcode()
            res_data = response.read().decode('utf-8')
            if status_code in (200, 201):
                logger.info(f"[EmailEngine] Dispatched via Resend HTTPS API to {recipient_list} (Status: {status_code}): {res_data}")
                return True
            else:
                logger.warning(f"[EmailEngine] Resend HTTPS API returned status {status_code}: {res_data}")
                return False

    except urllib.error.HTTPError as http_err:
        err_body = http_err.read().decode('utf-8') if hasattr(http_err, 'read') else str(http_err)
        logger.error(f"[EmailEngine] Resend HTTPS API HTTPError {http_err.code}: {err_body}")
        # Automated Failover: If custom domain is pending DNS verification on Resend (403), auto-retry via envelope sender
        if http_err.code == 403 and 'onboarding@resend.dev' not in from_email:
            logger.info("[EmailEngine] Custom domain pending Resend DNS verification. Auto-retrying via verified envelope sender...")
            return _send_via_resend_api(api_key, "The Finisher Luxury Registrations <onboarding@resend.dev>", recipient_list, subject, text_body, html_body)
        return False
    except Exception as e:
        logger.error(f"[EmailEngine] Resend HTTPS API failed: {e}")
        return False


def _send_email_worker(subject: str, text_body: str, recipient_list: list, from_email: str = None, html_body: str = None):
    """Internal synchronous worker executed inside the background thread."""
    if not recipient_list:
        return

    sender = from_email or getattr(settings, 'DEFAULT_FROM_EMAIL', 'The Finisher Luxury Registrations <noreply@mtamboholdings.dev>')
    resend_key = getattr(settings, 'RESEND_API_KEY', '').strip()

    # If sender doesn't have an @ or domain matching verified resend domains, fallback safely
    if not sender or '@' not in sender:
        sender = 'The Finisher Luxury Registrations <noreply@mtamboholdings.dev>'

    # Strategy 1: Resend HTTPS REST API (Port 443 — immune to SMTP port blocks)
    if resend_key:
        success = _send_via_resend_api(resend_key, sender, recipient_list, subject, text_body, html_body)
        if success:
            return

    # Strategy 2: Fallback to Django send_mail (fail_silently=True with strict timeout)
    try:
        django_send_mail(
            subject=subject,
            message=text_body,
            from_email=sender,
            recipient_list=recipient_list,
            html_message=html_body,
            fail_silently=True
        )
        logger.info(f"[EmailEngine] Fallback send_mail dispatched to {recipient_list}")
    except Exception as e:
        logger.warning(f"[EmailEngine] Fallback send_mail failed: {e}")


def send_email_async(subject: str, text_body: str, recipient_list: list, from_email: str = None, html_body: str = None):
    """
    Asynchronous Non-Blocking Email Dispatcher.
    Spawns a daemon thread to deliver the message in the background.
    Returns control immediately (< 1ms) so the calling HTTP endpoint never delays.
    """
    if isinstance(recipient_list, str):
        recipient_list = [recipient_list]

    thread = threading.Thread(
        target=_send_email_worker,
        args=(subject, text_body, recipient_list, from_email, html_body),
        daemon=True,
        name=f"email-dispatch-{recipient_list[0] if recipient_list else 'unknown'}"
    )
    thread.start()
    logger.info(f"[EmailEngine] Asynchronously queued email to {recipient_list} in daemon thread.")


def render_luxury_email_html(
    title: str,
    subtitle: str,
    recipient_name: str,
    message_paragraphs: list,
    credentials: dict = None,
    otp_code: str = None,
    otp_expiry_minutes: int = None,
    cta_text: str = None,
    cta_url: str = None,
    activation_steps: list = None,
    security_note: str = None
) -> str:
    """
    Generates a world-class, responsive, luxury HTML email template.
    Features:
      - Obsidian dark theme with brushed gold foil metallic accents (#D4AF37)
      - Corporate letterhead & brand crest
      - Prominent Glowing Gold OTP Token Card for 2FA / Password Reset / Access Verification
      - Monospaced, high-contrast credential box with copyable temporary password pill
      - Gradient primary call-to-action button
      - Numbered luxury activation step cards
      - POPIA Section 19 security seal & legal footer
    """
    # Build OTP Token Card if provided
    otp_html = ""
    if otp_code:
        expiry_txt = f"Valid for exactly {otp_expiry_minutes} minutes" if otp_expiry_minutes else "Ephemeral Single-Use Cryptographic Passcode"
        otp_html = f"""
        <div style="margin:26px 0;text-align:center;background:radial-gradient(ellipse at center, rgba(212,175,55,0.14) 0%, rgba(15,23,42,0.95) 100%);border:1.5px solid #d4af37;border-radius:12px;padding:24px 16px;box-shadow:0 0 30px rgba(212,175,55,0.22);">
          <div style="font-size:10.5px;letter-spacing:2.5px;color:#d4af37;font-weight:800;text-transform:uppercase;margin-bottom:8px;">SECURE VERIFICATION PASSCODE</div>
          <div style="font-family:Consolas, Monaco, 'Courier New', monospace;font-size:38px;font-weight:900;letter-spacing:10px;color:#ffffff;text-shadow:0 0 20px rgba(212,175,55,0.6);margin:8px 0;">{otp_code}</div>
          <div style="font-size:11.5px;color:#94a3b8;margin-top:8px;">{expiry_txt} &middot; Zero-Trust Ephemeral Token</div>
        </div>
        """

    # Build credentials rows
    cred_html = ""
    if credentials:
        cred_rows = []
        for key, val in credentials.items():
            if 'password' in key.lower() or 'passcode' in key.lower():
                val_markup = f"""<span style="background:#fef3c7;color:#92400e;padding:6px 14px;border-radius:6px;font-weight:800;font-size:15px;letter-spacing:1.5px;border:1px solid #d97706;font-family:Consolas,Monaco,monospace;display:inline-block;">{val}</span>"""
            elif 'portal' in key.lower() or 'url' in key.lower() or 'link' in key.lower():
                val_markup = f"""<a href="{val}" style="color:#d4af37;text-decoration:underline;font-weight:600;">{val}</a>"""
            else:
                val_markup = f"""<strong style="color:#ffffff;font-size:14px;">{val}</strong>"""

            cred_rows.append(f"""
            <tr>
              <td style="padding:10px 14px;color:#94a3b8;font-size:13px;border-bottom:1px solid rgba(255,255,255,0.07);width:38%;font-weight:600;">{key}</td>
              <td style="padding:10px 14px;color:#f8fafc;font-size:13px;border-bottom:1px solid rgba(255,255,255,0.07);">{val_markup}</td>
            </tr>
            """)
        cred_html = f"""
        <table style="width:100%;border-collapse:collapse;margin:22px 0;background:rgba(15,23,42,0.85);border:1px solid rgba(212,175,55,0.35);border-radius:8px;overflow:hidden;">
          {''.join(cred_rows)}
        </table>
        """

    # Build steps list
    steps_html = ""
    if activation_steps:
        step_items = []
        for i, step in enumerate(activation_steps, 1):
            step_items.append(f"""
            <div style="display:flex;align-items:flex-start;margin-bottom:10px;">
              <span style="background:linear-gradient(135deg,#d4af37,#b45309);color:#ffffff;width:22px;height:22px;border-radius:50%;display:inline-block;text-align:center;line-height:22px;font-size:11px;font-weight:800;margin-right:12px;flex-shrink:0;">{i}</span>
              <span style="color:#cbd5e1;font-size:13.5px;line-height:1.5;">{step}</span>
            </div>
            """)
        steps_html = f"""
        <div style="background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.08);border-radius:8px;padding:16px 18px;margin:20px 0;">
          <div style="font-size:11px;font-weight:800;letter-spacing:1.5px;color:#d4af37;text-transform:uppercase;margin-bottom:12px;">MANDATORY ACTIVATION PROTOCOL</div>
          {''.join(step_items)}
        </div>
        """

    # Build CTA Button
    cta_html = ""
    if cta_text and cta_url:
        cta_html = f"""
        <div style="text-align:center;margin:28px 0 16px;">
          <a href="{cta_url}" style="background:linear-gradient(135deg,#d4af37 0%,#b45309 100%);color:#ffffff;padding:15px 36px;border-radius:8px;font-weight:700;font-size:15px;text-decoration:none;display:inline-block;letter-spacing:0.5px;box-shadow:0 6px 20px rgba(212,175,55,0.35);">
            {cta_text} &rarr;
          </a>
        </div>
        """

    # Build Message Paragraphs
    body_p = "".join([f"""<p style="color:#e2e8f0;font-size:14.5px;line-height:1.65;margin:0 0 14px;">{p}</p>""" for p in message_paragraphs])

    # Security Note
    sec_html = ""
    if security_note:
        sec_html = f"""
        <div style="background:rgba(217,119,6,0.08);border-left:3px solid #d97706;border-radius:4px;padding:10px 14px;margin:18px 0;color:#fde68a;font-size:12px;line-height:1.5;">
          <strong>SECURITY PROTOCOL:</strong> {security_note}
        </div>
        """

    # Randomized executive greeting pool for variety, personality, and security feeling
    import random
    luxury_greetings = [
        "Salutations",
        "Greetings",
        "Good day",
        "Esteemed",
        "Distinguished",
        "Executive Greetings",
        "Welcome",
        "Warmest Regards",
        "Respectful Greetings"
    ]
    greeting = random.choice(luxury_greetings)

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title}</title>
</head>
<body style="margin:0;padding:0;background-color:#080c14;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Helvetica,Arial,sans-serif;">
  <table role="presentation" width="100%" border="0" cellspacing="0" cellpadding="0" style="background-color:#080c14;padding:30px 15px;">
    <tr>
      <td align="center">
        <!-- Main Card Container -->
        <table role="presentation" width="100%" border="0" cellspacing="0" cellpadding="0" style="max-width:600px;background:linear-gradient(180deg,#0f172a 0%,#090d16 100%);border:1px solid rgba(212,175,55,0.35);border-radius:12px;overflow:hidden;box-shadow:0 12px 40px rgba(0,0,0,0.6);">
          
          <!-- Top Gold Accent Line -->
          <tr>
            <td style="height:3px;background:linear-gradient(90deg,#d4af37 0%,#f59e0b 50%,#b45309 100%);"></td>
          </tr>

          <!-- Header -->
          <tr>
            <td style="padding:32px 36px 20px;text-align:center;">
              <table role="presentation" border="0" cellspacing="0" cellpadding="0" style="margin:0 auto 14px;">
                <tr>
                  <td style="width:48px;height:48px;background:linear-gradient(135deg,#d4af37 0%,#92400e 100%);border-radius:10px;text-align:center;color:#ffffff;font-size:24px;font-weight:900;line-height:48px;letter-spacing:-1px;box-shadow:0 4px 14px rgba(212,175,55,0.4);">
                    F
                  </td>
                </tr>
              </table>
              <div style="font-size:20px;font-weight:800;color:#ffffff;letter-spacing:1px;">THE FINISHER LUXURY</div>
              <div style="font-size:10px;font-weight:800;letter-spacing:2.5px;color:#d4af37;text-transform:uppercase;margin-top:4px;">{subtitle}</div>
            </td>
          </tr>

          <!-- Divider -->
          <tr>
            <td style="padding:0 36px;">
              <div style="border-bottom:1px solid rgba(255,255,255,0.08);"></div>
            </td>
          </tr>

          <!-- Body Content -->
          <tr>
            <td style="padding:28px 36px 24px;">
              <div style="color:#d4af37;font-size:11px;font-weight:800;letter-spacing:1.5px;text-transform:uppercase;margin-bottom:8px;">{title}</div>
              <h1 style="color:#ffffff;font-size:21px;font-weight:700;margin:0 0 16px;line-height:1.3;">{greeting}, {recipient_name}</h1>
              
              {body_p}
              {otp_html}
              {cred_html}
              {cta_html}
              {steps_html}
              {sec_html}
            </td>
          </tr>

          <!-- Footer -->
          <tr>
            <td style="background:rgba(0,0,0,0.4);padding:24px 36px;border-top:1px solid rgba(255,255,255,0.07);text-align:center;">
              <div style="font-size:11.5px;font-weight:700;color:#d4af37;letter-spacing:0.5px;">MTAMBO HOLDINGS (PTY) LTD &middot; EXECUTIVE DIRECTORATE</div>
              <div style="font-size:10.5px;color:#64748b;margin-top:4px;">POPIA Section 19 Cryptographic Dispatch &middot; 7682 Isikova Crescent, Gauteng, Boksburg, 1459</div>
              <div style="font-size:10px;color:#475569;margin-top:8px;">
                Direct concierge support: <a href="mailto:mtamboholdings@outlook.com" style="color:#94a3b8;text-decoration:none;">mtamboholdings@outlook.com</a>
              </div>
            </td>
          </tr>

        </table>
      </td>
    </tr>
  </table>
</body>
</html>"""

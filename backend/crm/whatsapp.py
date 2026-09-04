"""WhatsApp messaging helpers (disabled by default)."""
import logging

logger = logging.getLogger(__name__)


def send_whatsapp_message(to_phone: str, message_body: str) -> dict:
    """Stub implementation: WhatsApp sending is intentionally disabled."""
    logger.info("WhatsApp sending disabled. Skipping message to %s", to_phone)
    return {
        'success': False,
        'message_sid': None,
        'error': 'whatsapp_disabled'
    }


def send_lead_welcome_message(contact_name: str, phone: str, calendar_link: str = None) -> dict:
    """
    Send automated welcome message to new lead.
    
    Args:
        contact_name: Lead's first name
        phone: Lead's phone number
        calendar_link: Optional calendar booking link
        
    Returns:
        dict with send result
    """
    message = f"""Hi {contact_name}! 👋

Thank you for reaching out to Mtambo Holdings. We're excited to connect with you!

Your inquiry has been received and we'll be in touch shortly. In the meantime, feel free to explore what we do at https://mtamboholdings.dev

We look forward to working with you!

Mtambo Holdings Team"""
    
    if calendar_link:
        message += f"\n\n📅 Book a time with us here: {calendar_link}"
    
    return send_whatsapp_message(phone, message)

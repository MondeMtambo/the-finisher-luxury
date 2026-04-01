"""
WhatsApp messaging via Twilio integration.
"""
import logging
from django.conf import settings
from twilio.rest import Client

logger = logging.getLogger(__name__)


def send_whatsapp_message(to_phone: str, message_body: str) -> dict:
    """
    Send a WhatsApp message via Twilio.
    
    Args:
        to_phone: Recipient phone number (e.g., '+27821234567')
        message_body: Message text to send
        
    Returns:
        dict with keys: success (bool), message_sid (str), error (str)
    """
    try:
        # Get Twilio credentials from environment
        account_sid = settings.TWILIO_ACCOUNT_SID
        auth_token = settings.TWILIO_AUTH_TOKEN
        from_whatsapp = settings.TWILIO_WHATSAPP_FROM  # e.g., 'whatsapp:+1234567890'
        
        if not all([account_sid, auth_token, from_whatsapp]):
            logger.error("Twilio credentials not configured in settings")
            return {
                'success': False,
                'message_sid': None,
                'error': 'Twilio not configured'
            }
        
        # Format recipient number for WhatsApp
        to_whatsapp = f"whatsapp:{to_phone}"
        
        # Create Twilio client
        client = Client(account_sid, auth_token)
        
        # Send message
        message = client.messages.create(
            from_=from_whatsapp,
            to=to_whatsapp,
            body=message_body
        )
        
        logger.info(f"WhatsApp message sent to {to_phone}: SID={message.sid}")
        return {
            'success': True,
            'message_sid': message.sid,
            'error': None
        }
        
    except Exception as e:
        logger.error(f"Failed to send WhatsApp to {to_phone}: {str(e)}")
        return {
            'success': False,
            'message_sid': None,
            'error': str(e)
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

Your inquiry has been received and we'll be in touch shortly. In the meantime, feel free to explore what we do at mtamboholdings.com

We look forward to working with you!

Mtambo Holdings Team"""
    
    if calendar_link:
        message += f"\n\n📅 Book a time with us here: {calendar_link}"
    
    return send_whatsapp_message(phone, message)

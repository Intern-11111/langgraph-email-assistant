"""
Email response templates for the mock email agent.
These templates are used instead of LLM-generated responses.
"""
from typing import Dict, Any
from datetime import datetime


def get_sender_name(email_address: str) -> str:
    """Extract name from email address or use email if no name available."""
    if '<' in email_address:
        # Format: "Name <email@example.com>"
        return email_address.split('<')[0].strip()
    # Use email username
    return email_address.split('@')[0].capitalize()


def meeting_confirmation_template(mail: Dict[str, Any], calendar_slot: Dict[str, str] = None) -> str:
    """Template for confirming meeting requests."""
    sender_name = get_sender_name(mail.get('sender', 'there'))
    
    if calendar_slot:
        start_time = calendar_slot.get('start', 'the requested time')
        end_time = calendar_slot.get('end', '')
        
        return f"""Hi {sender_name},

Thank you for your meeting request. I've checked my calendar and I'm available.

Meeting Details:
- Time: {start_time} to {end_time}
- Subject: {mail.get('subject', 'Meeting')}

The meeting has been added to my calendar. Looking forward to speaking with you!

Best regards"""
    else:
        return f"""Hi {sender_name},

Thank you for your meeting request regarding "{mail.get('subject', 'our meeting')}".

I've received your request and will get back to you shortly with my availability.

Best regards"""


def question_response_template(mail: Dict[str, Any]) -> str:
    """Template for responding to questions or general inquiries."""
    sender_name = get_sender_name(mail.get('sender', 'there'))
    
    return f"""Hi {sender_name},

Thank you for reaching out regarding "{mail.get('subject', 'your inquiry')}".

I've received your message and will review it carefully. I'll get back to you with a detailed response shortly.

Best regards"""


def acknowledgment_template(mail: Dict[str, Any]) -> str:
    """Generic acknowledgment template for requests or information."""
    sender_name = get_sender_name(mail.get('sender', 'there'))
    
    return f"""Hi {sender_name},

Thank you for your email about "{mail.get('subject', 'this matter')}".

I've received your message and will take appropriate action.

Best regards"""


def thanks_response_template(mail: Dict[str, Any]) -> str:
    """Template for responding to thank you messages."""
    sender_name = get_sender_name(mail.get('sender', 'there'))
    
    return f"""Hi {sender_name},

You're very welcome! Happy to help.

Best regards"""


def get_template_for_email(mail: Dict[str, Any], category: str = "respond-act") -> str:
    """
    Select appropriate template based on email content.
    
    Args:
        mail: Email dictionary with subject, body, sender
        category: Triage category (ignore, notify-human, respond-act)
    
    Returns:
        Formatted email response string
    """
    if category == "ignore":
        return None  # No response needed for ignored emails
    
    if category == "notify-human":
        return None  # Human will handle this
    
    # For respond-act category, select template based on email content
    body_lower = mail.get('body', '').lower()
    subject_lower = mail.get('subject', '').lower()
    
    # Check for meeting-related keywords
    meeting_keywords = ['meeting', 'schedule', 'calendar', 'appointment', 'meet', 'call', 'zoom', 'teams']
    if any(keyword in body_lower or keyword in subject_lower for keyword in meeting_keywords):
        # Mock calendar slot (in real implementation, this would come from calendar check)
        calendar_slot = {
            'start': '2026-01-28 14:00',
            'end': '2026-01-28 15:00'
        }
        return meeting_confirmation_template(mail, calendar_slot)
    
    # Check for thank you messages
    thanks_keywords = ['thank you', 'thanks', 'appreciate']
    if any(keyword in body_lower or keyword in subject_lower for keyword in thanks_keywords):
        return thanks_response_template(mail)
    
    # Check for questions
    question_keywords = ['?', 'question', 'how', 'what', 'when', 'where', 'why', 'clarify', 'explain']
    if any(keyword in body_lower or keyword in subject_lower for keyword in question_keywords):
        return question_response_template(mail)
    
    # Default to acknowledgment template
    return acknowledgment_template(mail)

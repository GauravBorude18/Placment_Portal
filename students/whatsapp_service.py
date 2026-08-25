# WhatsApp Notification Service for Placement Portal
import urllib.parse
import urllib.request
import json
import logging
from django.conf import settings

logger = logging.getLogger(__name__)

def format_indian_phone(phone_number):
    cleaned = ''.join(filter(str.isdigit, str(phone_number)))
    if len(cleaned) == 10:
        return f'+91{cleaned}'
    elif len(cleaned) == 12 and cleaned.startswith('91'):
        return f'+{cleaned}'
    elif str(phone_number).startswith('+'):
        return str(phone_number)
    return f'+91{cleaned}'


def send_whatsapp_message(phone_number, message_text):
    to_phone = format_indian_phone(phone_number)
    provider = getattr(settings, 'WHATSAPP_PROVIDERCONFIG', 'TWILIO')

    account_sid = getattr(settings, 'TWILIO_ACCOUNT_SID', '')
    auth_token = getattr(settings, 'TWILIO_AUTH_TOKEN', '')
    from_phone = getattr(settings, 'TWILIO_WHATSAPP_FROM', 'whatsapp;+14155238886')

    if not account_sid or account_sid.startswith('your-'):
        print(f"[WHATSAPP INFO -> {to_phone}]:\n{message_text}")
        return True

    try:
        url = f"https://api.twilio.com/2010-04-01/Accounts/{account_sid}/Messages.json"
        data = urllib.parse.urlencode({
            'From': from_phone,
            'To': f"whatsapp:{to_phone}",
            'Body': message_text
        }).encode('utf-8')

        req = urllib.request.Request(url, data=data, method='POST')
        import base64
        auth_header = base64.b64encode(f"{account_sid}:{auth_token}".encode()).decode()
        req.add_header('Authorization', f'Basic {auth_header}')

        with urllib.request.urlopen(req, timeout=5) as resp:
            result = json.loads(resp.read().decode())
            print(f"[WHATSAPP SUCCESS] Twilio SID: {result.get('sid')} -> {to_phone}")
            return True
    except Exception as e:
        print(f"[WHATSAPP ERROR] Twilio error: {e}")
        return False


def send_registration_otp_whatsapp(phone_number, otp):
    msg = f"* A2Z Placement Portal *\n\nYour verification OTP is: *{otp}*\n\nValid for 10 minutes.\n\n_Training & Placement Cell, A2Z Campus_"
    return send_whatsapp_message(phone_number, msg)


def send_payment_receipt_whatsapp(student, receipt_number, amount='99.00'):
    phone = student.phone_number
    if not phone:
        return False
    msg = f"* A2Z Placement Fee Paid *\n\nDear *{student.full_name}*,\nYour Rs. {amount} fee has been successfully received.\n\nReceipt No: {receipt_number}\nRoll No: {student.roll_number}\n\nYour profile is updated in your Student Dashboard.\n\n_Training & Placement Cell_"
    return send_whatsapp_message(phone, msg)


def send_shortlist_whatsapp(student, company_name, role_title, test_link='https://a2zplacement.edu/assessment'):
    phone = student.phone_number
    if not phone:
        return False
    msg = f"* Congratulations! You are Shortlisted! *\n\nDear *{student.full_name}*,\nYou have been shortlisted by {company_name} for {role_title}.\n\nAssessment Link: {test_link}\n\n_A2Z Placement Cell_"
    return send_whatsapp_message(phone, msg)


def get_whatsapp_direct_click_url(phone_number, message_text):
    clean_phone = format_indian_phone(phone_number).replace('+', '')
    encoded_msg = urllib.parse.quote(message_text)
    return f"https://api.whatsapp.com/send?phone={clean_phone}&text={encoded_msg}"

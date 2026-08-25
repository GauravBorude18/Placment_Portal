"""
=============================================================================
A2Z Placement Cell - JWT Security & Stateless Registration Service
=============================================================================
मराठी स्पष्टीकरण (Marathi Explanation):
हा मॉड्युल विद्यार्थ्याच्या रजिस्ट्रेशन डेटाला सुरक्षित JWT (JSON Web Token) मध्ये 
एन्क्रिप्ट करतो. जोपर्यंत विद्यार्थी ₹99 फी भरत नाही, तोपर्यंत डेटाबेसमध्ये 
काहीही सेव्ह होत नाही. पेमेंट झाल्यावर हे टोकन डिकोड करून अधिकृत खाते तयार होते.
=============================================================================
"""

import jwt
from datetime import datetime, timedelta, timezone
from django.conf import settings


def create_registration_draft_jwt(form_data, expiry_minutes=30):
    """
    विद्यार्थ्याने भरलेली सर्व माहिती (Step 1 to 4) एका सुरक्षित JWT टोकनमध्ये साठवते.
    Token is cryptographically signed using Django's SECRET_KEY (HMAC-SHA256).
    
    :param form_data: dict containing student registration inputs
    :param expiry_minutes: token validity (default: 30 minutes)
    :return: encoded JWT string
    """
    now_utc = datetime.now(timezone.utc)
    exp_time = now_utc + timedelta(minutes=expiry_minutes)

    payload = {
        'purpose': 'placement_student_registration_draft',
        'created_at': now_utc.timestamp(),
        'exp': exp_time,
        'form_data': form_data
    }

    # HMAC-SHA256 द्वारे डिजिटल स्वाक्षरी असलेले टोकन तयार करणे
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
    return token


def decode_registration_draft_jwt(token):
    """
    पेमेंट यशस्वी झाल्यावर JWT टोकन तपासून मूळ फॉर्म डेटा परत करते.
    Validates token signature and expiration.
    
    :param token: JWT token string
    :return: (form_data, error_message)
    """
    if not token:
        return None, "नोंदणी टोकन सापडले नाही (Registration Token Missing)!"

    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        
        # उद्देश (Purpose) तपासणे
        if payload.get('purpose') != 'placement_student_registration_draft':
            return None, "अवैध टोकन प्रकार (Invalid Token Purpose)!"
            
        form_data = payload.get('form_data')
        if not form_data:
            return None, "टोकनमध्ये डेटा सापडला नाही (Form Data Empty in Token)!"

        return form_data, None

    except jwt.ExpiredSignatureError:
        return None, "नोंदणी टोकनची मुदत (३० मिनिटे) संपली आहे. कृपया फॉर्म पुन्हा सबमिट करा (Token Expired)!"
    except jwt.InvalidTokenError:
        return None, "टोकन अवैध किंवा छेडछाड केलेले आहे (Invalid / Tampered Token)!"
    except Exception as e:
        return None, f"टोकन डिकोड करताना त्रुटी आली: {str(e)}"


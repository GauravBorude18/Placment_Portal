import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'placement_core.settings')
django.setup()
from django.test import Client
from django.contrib.auth.models import User
from students.models import StudentProfile

c = Client()

# Find an existing student email
existing_student = StudentProfile.objects.first()
existing_email = existing_student.user.email
print(f"Testing with registered student email: {existing_email}")

# 1. Test check-email API for existing email
resp_chk = c.get(f'/api/check-email/?email={existing_email}')
print("Check email for existing:", resp_chk.status_code, resp_chk.json())
assert resp_chk.json()['available'] == False
assert 'already registered' in resp_chk.json()['error']

# 2. Test send-otp for existing email (POST & GET)
resp_send_get = c.get(f'/api/send-otp/?email={existing_email}')
print("Send OTP (GET) for existing email:", resp_send_get.status_code, resp_send_get.json())
assert resp_send_get.status_code == 400
assert resp_send_get.json()['already_registered'] == True
assert 'already registered' in resp_send_get.json()['error']

resp_send_post = c.post('/api/send-otp/', {'email': existing_email})
print("Send OTP (POST) for existing email:", resp_send_post.status_code, resp_send_post.json())
assert resp_send_post.status_code == 400
assert resp_send_post.json()['already_registered'] == True

# 3. Test verify-otp for existing email
resp_verify_exist = c.post('/api/verify-otp/', {'email': existing_email, 'otp': '123456'})
print("Verify OTP for existing email:", resp_verify_exist.status_code, resp_verify_exist.json())
assert resp_verify_exist.status_code == 400
assert resp_verify_exist.json()['already_registered'] == True

# 4. Test check-email for brand new email
new_email = "brand_new_student_2026@a2z.edu.in"
resp_chk_new = c.get(f'/api/check-email/?email={new_email}')
print("Check email for new:", resp_chk_new.status_code, resp_chk_new.json())
assert resp_chk_new.json()['available'] == True

# 5. Test send-otp for brand new email
resp_send_new = c.post('/api/send-otp/', {'email': new_email})
print("Send OTP for new email:", resp_send_new.status_code, resp_send_new.json())
assert resp_send_new.status_code == 200
assert resp_send_new.json()['success'] == True

print("ALL TESTS PASSED: Registered email is immediately flagged, OTP generation is strictly blocked, and OTP verification is completely denied!")

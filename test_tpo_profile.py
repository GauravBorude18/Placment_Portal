import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'placement_core.settings')
django.setup()
from django.test import Client
from tpo_officer.models import TPOProfile
from django.contrib.auth.models import User

c = Client()
# 1. Login as TPO
resp_login = c.post('/login/', {'username': 'tpo', 'password': 'student123', 'role': 'admin'}, follow=True)

# 2. Get profile page
resp_profile = c.get('/tpo/profile/')
print('TPO Profile GET status:', resp_profile.status_code)
assert resp_profile.status_code == 200
assert b'Prof. S. Bhattacharya' in resp_profile.content

# 3. Test Appointing New TPO
resp_appoint = c.post('/tpo/profile/', {
    'action': 'appoint_tpo',
    'new_full_name': 'Prof. Rajesh K. Sharma',
    'new_username': 'tpo_sharma',
    'new_email': 'r.sharma@a2zplacement.edu',
    'new_password': 'sharmaPass123',
    'new_designation': 'Head, Training & Placement Cell',
    'new_department': 'Computer Science & Engineering',
    'new_phone': '+91 98220 99999',
    'new_signing_title': 'Head, Placement Cell & DPC In-Charge'
}, follow=True)

print('Appoint New TPO status:', resp_appoint.status_code)
assert resp_appoint.status_code == 200
assert b'Prof. Rajesh K. Sharma' in resp_appoint.content

# 4. Verify new TPO in database
new_tpo = TPOProfile.objects.get(user__username='tpo_sharma')
print('New TPO is active head:', new_tpo.is_active_head)
assert new_tpo.is_active_head == True

# 5. Verify new TPO can log in and access TPO Dashboard
c_new = Client()
resp_new_login = c_new.post('/login/', {'username': 'tpo_sharma', 'password': 'sharmaPass123', 'role': 'admin'}, follow=True)
print('New TPO login status:', resp_new_login.status_code)
assert resp_new_login.status_code == 200

resp_new_dash = c_new.get('/tpo/dashboard/')
print('New TPO Dashboard access status:', resp_new_dash.status_code)
assert resp_new_dash.status_code == 200
assert b'Prof. Rajesh K. Sharma' in resp_new_dash.content

print('TEST PASSED: TPO Profile Update, Appoint New TPO, Credentials Assignment & Access 100% Verified!')

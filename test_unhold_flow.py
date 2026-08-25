import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'placement_core.settings')
django.setup()
from django.test import Client
from students.models import StudentProfile

# 1. Unhold student 223344556
st = StudentProfile.objects.filter(roll_number='223344556').first()
c = Client()
# Log in as TPO
c.post('/login/', {'username': 'tpo', 'password': 'student123', 'role': 'admin'})
resp_unhold = c.get(f'/tpo/students/unhold/{st.id}/', follow=True)
print('Unhold action status:', resp_unhold.status_code)

st.refresh_from_db()
print('After Unhold in DB:')
print('verification_status:', st.verification_status)
print('is_dpc_verified:', st.is_dpc_verified)
print('hold_until:', st.hold_until)

# 2. Check Student Dashboard for 223344556
c_student = Client()
c_student.force_login(st.user)
resp_dash = c_student.get('/dashboard/')
print('Dashboard status:', resp_dash.status_code)
assert resp_dash.status_code == 200

# Verify yellow banner is GONE and verified pill is PRESENT
if b'TEMPORARY VERIFICATION HOLD IN EFFECT' in resp_dash.content:
    print('WARNING: Hold banner is still in HTML!')
else:
    print('SUCCESS: Hold banner is completely GONE from HTML!')

if b'Verified by Placement Head & DPC' in resp_dash.content:
    print('SUCCESS: Green Verified Badge is displayed on Dashboard!')
else:
    print('WARNING: Verified badge not found!')

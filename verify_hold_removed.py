import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'placement_core.settings')
django.setup()
from django.test import Client
from students.models import StudentProfile

st = StudentProfile.objects.get(roll_number='223344556')
c = Client()
c.force_login(st.user)
resp = c.get('/dashboard/')
print('Current Dashboard status code:', resp.status_code)
print('Is Hold Banner present in HTML?', b'TEMPORARY VERIFICATION HOLD IN EFFECT' in resp.content)
print('Is Verified Badge present in HTML?', b'Verified by Placement Head & DPC' in resp.content)
assert not (b'TEMPORARY VERIFICATION HOLD IN EFFECT' in resp.content)
assert b'Verified by Placement Head & DPC' in resp.content
print('All checks confirmed!')

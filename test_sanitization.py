import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'placement_core.settings')
django.setup()
from django.test import Client
from students.models import StudentProfile
from django.contrib.auth.models import User

st = StudentProfile.objects.first()
print('Student user:', st.user.username)
c = Client()
c.force_login(st.user)
resp_edit = c.get('/profile/edit/')
print('Profile Edit status:', resp_edit.status_code)
assert resp_edit.status_code == 200
assert b'Primary Mobile Number (10 digits)' in resp_edit.content
print('100% Passed!')

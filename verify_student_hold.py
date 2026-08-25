import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'placement_core.settings')
django.setup()
from django.test import Client
from students.models import StudentProfile

c = Client()
c.post('/login/', {'username': '223344556', 'password': 'student123', 'role': 'student'})

resp_dash = c.get('/student_dashboard/')
assert resp_dash.status_code == 200
assert b'TEMPORARY VERIFICATION HOLD IN EFFECT' in resp_dash.content
print('Dashboard Hold banner verified!')

resp_notif = c.get('/notifications/')
assert resp_notif.status_code == 200
assert b'Temporary Verification Hold Active' in resp_notif.content or b'Placed on Hold' in resp_notif.content
print('Notification Center Hold alert verified!')

print('Student 223344556 Hold notifications verified 100% OK!')

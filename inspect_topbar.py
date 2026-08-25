import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'placement_core.settings')
django.setup()
from django.test import Client

c = Client()
c.post('/login/', {'username': '223344556', 'password': 'student123', 'role': 'student'})

resp_dash = c.get('/student_dashboard/')
print('Status:', resp_dash.status_code)
content = resp_dash.content.decode('utf-8')

print('Has topbar-icon-btn:', 'topbar-icon-btn' in content)
print('Has View Details or View in mailbox modal:', 'View' in content)
for line in content.split('\n'):
    if 'topbar-icon-btn' in line or 'student-email-tray-modal' in line or 'openStudentEmailTray' in line:
        print('  >', line.strip()[:100])

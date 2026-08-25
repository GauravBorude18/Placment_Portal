import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'placement_core.settings')
django.setup()
from django.test import Client
from students.models import StudentProfile, StudentEmailNotification

c = Client()
st = StudentProfile.objects.get(roll_number='223344556')

# 1. TPO puts student 223344556 on Hold for 3 days
resp_hold = c.get(f'/tpo/students/hold/{st.id}/?days=3&reason=Pending+12th+HSC+Marksheet+Original+Verification')
print('TPO Hold action status:', resp_hold.status_code)

st.refresh_from_db()
print('Student status after Hold:', st.verification_status, 'Hold days:', st.hold_days)
assert st.verification_status == 'ON_HOLD'

# Check notification created
notif = StudentEmailNotification.objects.filter(student=st, subject__icontains='Hold').first()
assert notif is not None
print('Notification created successfully:')
print('  Subject:', notif.subject.encode('ascii', 'ignore').decode('ascii'))
print('  Headline:', notif.headline.encode('ascii', 'ignore').decode('ascii'))
print('  Body:', notif.body_content.encode('ascii', 'ignore').decode('ascii'))

# 2. Student 223344556 logs in and opens notification center
c_student = Client()
c_student.post('/login/', {'username': '223344556', 'password': 'student123', 'role': 'student'})
resp_notif = c_student.get('/notifications/')
assert resp_notif.status_code == 200
assert b'Temporary Verification Hold Active' in resp_notif.content or b'Placed on Hold' in resp_notif.content

print('TEST PASSED: Hold notification appears immediately on student profile & notification center!')

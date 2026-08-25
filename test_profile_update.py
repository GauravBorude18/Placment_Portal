import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'placement_core.settings')
django.setup()
from django.test import Client
from students.models import StudentProfile
from django.contrib.auth.models import User

# 1. Get Gaurav Borude
st = StudentProfile.objects.filter(roll_number='223344556').first()
assert st is not None, "Student 223344556 should exist"

c = Client()
c.force_login(st.user)

# 2. Get /profile/edit/
resp = c.get('/profile/edit/')
print('GET /profile/edit/ status:', resp.status_code)
assert resp.status_code == 200
html = resp.content.decode('utf-8')
assert 'Gaurav Borude' in html
assert '223344556' in html
assert '1. Student Identity & Login' in html
assert '2. Contact & Permanent Address' in html
assert '3. 10th & 12th High School Credentials' in html
assert '4. Degree Program & CPI' in html
assert '5. Master Resumes (PDF Format)' in html
print('All 5 Registration Record Sections are visible in Edit Profile!')

# 3. Post Update to profile
update_data = {
    'full_name': 'Gaurav S. Borude',
    'email': 'gaurav.borude.2026@a2z.edu.in',
    'phone_number': '9820198201',
    'alternate_phone': '9820198202',
    'permanent_address': 'Flat 402, Greenfield Residency, FC Road',
    'pincode': '411005',
    'city': 'Pune',
    'state': 'Maharashtra',
    'tenth_board': 'CBSE',
    'tenth_percentage': '94.50',
    'tenth_year': '2020',
    'tenth_school': 'Delhi Public School Pune',
    'twelfth_board': 'HSC Maharashtra',
    'twelfth_percentage': '95.20',
    'twelfth_year': '2022',
    'twelfth_school': 'Fergusson Junior College Pune',
    'degree': 'B.Tech in Computer Science & Engineering',
    'department': 'Computer Science & Engineering',
    'cgpa': '8.15',
    'specialization': 'Cyber Security & AI',
    'new_password': 'newpassword123',
    'confirm_password': 'newpassword123'
}

resp_post = c.post('/profile/edit/', update_data, follow=True)
print('POST /profile/edit/ status:', resp_post.status_code)
assert resp_post.status_code == 200
assert 'updated successfully' in resp_post.content.decode('utf-8')

# 4. Check DB
st.refresh_from_db()
print('Updated full_name:', st.full_name)
print('Updated phone:', st.phone_number)
print('Updated address:', st.permanent_address)
print('Updated pincode:', st.pincode)
print('Updated city/state:', st.city, st.state)
print('Updated 10th %:', st.tenth_percentage)
print('Updated 12th %:', st.twelfth_percentage)
print('Updated CGPA:', st.cgpa)
print('Updated Specialization:', st.specialization)

assert st.full_name == 'Gaurav S. Borude'
assert st.phone_number == '9820198201'
assert st.pincode == '411005'
assert float(st.tenth_percentage) == 94.50
assert float(st.twelfth_percentage) == 95.20
assert float(st.cgpa) == 8.15

# 5. Verify login with new password
c_new = Client()
login_ok = c_new.login(username=st.user.username, password='newpassword123')
print('Login with new password succeeded:', login_ok)
assert login_ok == True

print('ALL TESTS PASSED: Full student registration details are completely viewable and editable!')

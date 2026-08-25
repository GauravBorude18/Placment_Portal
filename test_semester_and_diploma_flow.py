import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'placement_core.settings')
django.setup()
from django.test import Client
from students.models import StudentProfile
from decimal import Decimal

st = StudentProfile.objects.filter(roll_number='223344556').first()
assert st is not None, "Student 223344556 must exist"

c = Client()
c.force_login(st.user)

# 1. Test update to Diploma DSE
diploma_data = {
    'full_name': 'Gaurav S. Borude',
    'email': 'gaurav.borude.2026@a2z.edu.in',
    'phone_number': '9820198201',
    'alternate_phone': '9820198202',
    'permanent_address': 'Flat 402, Greenfield Residency, FC Road',
    'pincode': '411005',
    'city': 'Pune',
    'state': 'Maharashtra',
    'entry_route': 'DIPLOMA_DSE',
    'tenth_board': 'CBSE',
    'tenth_percentage': '94.50',
    'tenth_year': '2020',
    'tenth_school': 'Delhi Public School Pune',
    'diploma_board': 'MSBTE',
    'diploma_percentage': '89.40',
    'diploma_college': 'Government Polytechnic Pune',
    'degree': 'B.Tech in Computer Science & Engineering',
    'department': 'Computer Science & Engineering',
    'cgpa': '8.85',
    'active_backlogs': '0',
    'specialization': 'Cyber Security & AI',
    'sem3_sgpa': '8.80',
    'sem4_sgpa': '9.10',
    'sem5_sgpa': '9.30',
    'sem6_sgpa': '9.00',
    'sem7_sgpa': '9.20',
    'sem8_sgpa': '9.40',
    'sem3_backlogs': '0',
    'sem4_backlogs': '0',
    'sem5_backlogs': '0',
    'sem6_backlogs': '0',
    'sem7_backlogs': '0',
    'sem8_backlogs': '0',
}

resp = c.post('/profile/edit/', diploma_data, follow=True)
assert resp.status_code == 200
st.refresh_from_db()

print("--- Diploma DSE Verification ---")
print("Entry route:", st.entry_route)
print("Diploma Board:", st.diploma_board)
print("Diploma %:", st.diploma_percentage)
print("Diploma College:", st.diploma_college)
print("Sem 3 SGPA:", st.sem3_sgpa)
print("Semester pointers count:", len(st.semester_pointers))
assert st.entry_route == 'DIPLOMA_DSE'
assert float(st.diploma_percentage) == 89.40
assert len(st.semester_pointers) == 6
assert st.semester_pointers[0]['sem'] == 'Sem 3'

# 2. Test update to 12th HSC Regular
hsc_data = {
    'full_name': 'Gaurav S. Borude',
    'email': 'gaurav.borude.2026@a2z.edu.in',
    'phone_number': '9820198201',
    'alternate_phone': '9820198202',
    'permanent_address': 'Flat 402, Greenfield Residency, FC Road',
    'pincode': '411005',
    'city': 'Pune',
    'state': 'Maharashtra',
    'entry_route': '12TH_REGULAR',
    'tenth_board': 'CBSE',
    'tenth_percentage': '94.50',
    'tenth_year': '2020',
    'tenth_school': 'Delhi Public School Pune',
    'twelfth_board': 'HSC Maharashtra',
    'twelfth_percentage': '95.80',
    'twelfth_year': '2022',
    'twelfth_school': 'Fergusson Junior College Pune',
    'degree': 'B.Tech in Computer Science & Engineering',
    'department': 'Computer Science & Engineering',
    'cgpa': '8.95',
    'active_backlogs': '0',
    'specialization': 'Cyber Security & AI',
    'sem1_sgpa': '9.10',
    'sem2_sgpa': '9.20',
    'sem3_sgpa': '8.90',
    'sem4_sgpa': '9.10',
    'sem5_sgpa': '9.30',
    'sem6_sgpa': '9.00',
    'sem7_sgpa': '9.20',
    'sem8_sgpa': '9.40',
}

resp_hsc = c.post('/profile/edit/', hsc_data, follow=True)
assert resp_hsc.status_code == 200
st.refresh_from_db()

print("\n--- 12th HSC Regular Verification ---")
print("Entry route:", st.entry_route)
print("12th Board:", st.twelfth_board)
print("12th %:", st.twelfth_percentage)
print("Sem 1 SGPA:", st.sem1_sgpa)
print("Semester pointers count:", len(st.semester_pointers))
assert st.entry_route == '12TH_REGULAR'
assert float(st.twelfth_percentage) == 95.80
assert len(st.semester_pointers) == 8
assert st.semester_pointers[0]['sem'] == 'Sem 1'

print("\nALL SEMESTER MARKS AND 12TH/DIPLOMA TESTS PASSED!")

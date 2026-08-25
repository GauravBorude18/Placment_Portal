import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'placement_core.settings')
django.setup()
from students.models import StudentProfile

st = StudentProfile.objects.filter(roll_number='223344556').first()
if st:
    print('Student found:', st.full_name, st.roll_number)
    print('verification_status:', st.verification_status)
    print('is_dpc_verified:', st.is_dpc_verified)
    print('verification_remarks:', st.verification_remarks)
    print('hold_until:', st.hold_until)
    print('hold_days:', st.hold_days)
else:
    print('Student 223344556 not found!')
    all_s = StudentProfile.objects.all()
    for s in all_s:
        print(s.roll_number, s.full_name, s.verification_status, s.is_dpc_verified)

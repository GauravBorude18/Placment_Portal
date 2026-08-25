import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'placement_core.settings')
django.setup()
from students.models import StudentProfile
from django.contrib.auth.models import User

st = StudentProfile.objects.filter(roll_number='223344556').first()
if st:
    user = st.user
    print("Roll Number:", st.roll_number)
    print("Full Name:", st.full_name)
    print("Username:", user.username)
    print("Email:", user.email)
    print("Password is 'student123'?", user.check_password('student123'))
    print("Password is 'newpassword123'?", user.check_password('newpassword123'))
    
    # Let's set the password cleanly to 'student123' so the user can easily log in
    user.set_password('student123')
    user.save()
    print("Reset password to 'student123' successfully!")
else:
    print("Student not found!")

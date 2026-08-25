from django.test import TestCase, Client
from django.contrib.auth.models import User
from decimal import Decimal
from django.utils import timezone
from .models import StudentProfile, Company, JobAnnouncementForm, Application, InterviewSlot, PlacementAnnouncement

class StudentPortalTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='test_aarav', password='password123')
        self.student = StudentProfile.objects.create(
            user=self.user,
            roll_number='220050042',
            full_name='Aarav Sharma',
            cgpa=Decimal('9.48')
        )
        self.company = Company.objects.create(
            name='Google',
            sector='Software & AI',
            location='Bengaluru'
        )
        self.jaf = JobAnnouncementForm.objects.create(
            company=self.company,
            role_title='Software Engineer',
            sector='Software & AI',
            location='Bengaluru',
            ctc_display='₹48.5 LPA',
            ctc_breakdown='Base: ₹24 LPA',
            cgpa_cutoff=Decimal('8.50'),
            deadline=timezone.now(),
            description='Test description'
        )

    def test_landing_view(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'A2Z Placement Cell')
        self.assertContains(response, 'Role-Based Portals & Access')
        self.assertContains(response, 'Google')

    def test_student_dashboard_protected(self):
        # Unauthenticated access redirects to login
        response = self.client.get('/student_dashboard/')
        self.assertEqual(response.status_code, 302)
        self.assertTrue('/login/' in response.url)

        # Authenticated student access succeeds
        self.client.login(username='test_aarav', password='password123')
        auth_response = self.client.get('/student_dashboard/')
        self.assertEqual(auth_response.status_code, 200)
        self.assertContains(auth_response, 'Aarav Sharma')
        self.assertContains(auth_response, 'Google')

    def test_apply_api(self):
        self.client.login(username='test_aarav', password='password123')
        response = self.client.post(f'/api/apply/{self.jaf.id}/')
        self.assertEqual(response.status_code, 200)
        json_data = response.json()
        self.assertTrue(json_data['success'])
        self.assertEqual(Application.objects.filter(student=self.student, jaf=self.jaf).count(), 1)

    def test_unapproved_student_cannot_apply_or_view_details(self):
        self.client.login(username='test_aarav', password='password123')
        
        # 1. Set student status to unapproved
        self.student.is_dpc_verified = False
        self.student.verification_status = 'PENDING'
        self.student.save()

        # 2. Viewing JAF details is restricted (HTTP 403)
        detail_res = self.client.get(f'/api/jaf/{self.jaf.id}/')
        self.assertEqual(detail_res.status_code, 403)
        self.assertFalse(detail_res.json()['success'])

        # 3. Applying to JAF is locked (HTTP 403)
        apply_res = self.client.post(f'/api/apply/{self.jaf.id}/')
        self.assertEqual(apply_res.status_code, 403)
        self.assertFalse(apply_res.json()['success'])

        # 4. Once Placement Head approves, details and apply unlock (HTTP 200)
        self.student.is_dpc_verified = True
        self.student.verification_status = 'APPROVED'
        self.student.save()

        unlocked_detail = self.client.get(f'/api/jaf/{self.jaf.id}/')
        self.assertEqual(unlocked_detail.status_code, 200)
        self.assertTrue(unlocked_detail.json()['success'])

    def test_applications_view(self):
        self.client.login(username='test_aarav', password='password123')
        Application.objects.create(student=self.student, jaf=self.jaf, status='APPLIED')
        response = self.client.get('/applications/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Google')
        self.assertContains(response, 'Software Engineer')

    def test_schedule_view(self):
        self.client.login(username='test_aarav', password='password123')
        InterviewSlot.objects.create(
            student=self.student,
            jaf=self.jaf,
            round_name='Round 1 Algorithms'
        )
        response = self.client.get('/schedule/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Round 1 Algorithms')

    def test_login_view(self):
        # Test GET login page
        response = self.client.get('/login/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'A2Z Placement Cell')
        self.assertContains(response, 'Single Sign-On (SSO)')

        # Test POST login with student credentials
        login_response = self.client.post('/login/', {
            'username': 'test_aarav',
            'password': 'password123',
            'role': 'student'
        })
        self.assertEqual(login_response.status_code, 302)

        # Test POST login with student roll number
        login_by_roll = self.client.post('/login/', {
            'username': '220050042',
            'password': 'password123',
            'role': 'student'
        })
        self.assertEqual(login_by_roll.status_code, 302)

    def test_api_send_and_verify_otp(self):
        # 1. Send OTP to valid new email
        send_res = self.client.get('/api/send-otp/?email=student.test@a2z.edu.in')
        self.assertEqual(send_res.status_code, 200)
        data = send_res.json()
        self.assertTrue(data['success'])
        otp = data['otp']

        # 2. Verify with correct OTP
        verify_res = self.client.get(f'/api/verify-otp/?email=student.test@a2z.edu.in&otp={otp}')
        self.assertEqual(verify_res.status_code, 200)
        self.assertTrue(verify_res.json()['success'])

        # 3. Verify with invalid OTP fails
        bad_verify = self.client.get('/api/verify-otp/?email=student.test@a2z.edu.in&otp=999000')
        self.assertEqual(bad_verify.status_code, 400)
        self.assertFalse(bad_verify.json()['success'])

    def test_duplicate_email_rejected(self):
        User.objects.create_user(username='existing_user', email='duplicate@a2z.edu.in', password='pass')
        res = self.client.get('/api/send-otp/?email=duplicate@a2z.edu.in')
        self.assertEqual(res.status_code, 400)
        self.assertFalse(res.json()['success'])

    def test_register_view(self):
        # Test GET register page
        response = self.client.get('/register/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Student Placement Registration')
        self.assertContains(response, '10th / 12th')

        # Test POST register new student with all parts
        reg_response = self.client.post('/register/', {
            'username': 'priya.patel',
            'roll_number': '220070099',
            'full_name': 'Priya Patel',
            'email': 'priya.patel@a2z.edu.in',
            'password': 'password123',
            'confirm_password': 'password123',
            'phone_number': '+91 98201 54321',
            'alternate_phone': '+91 98201 12345',
            'permanent_address': 'A-402, Nilgiri Heights, Central Avenue Road',
            'city': 'Mumbai',
            'state': 'Maharashtra',
            'pincode': '400076',
            'tenth_board': 'CBSE',
            'tenth_percentage': '95.60',
            'tenth_year': '2020',
            'tenth_school': 'Delhi Public School',
            'twelfth_board': 'CBSE',
            'twelfth_percentage': '96.80',
            'twelfth_year': '2022',
            'twelfth_school': 'National Junior College',
            'degree': 'B.Tech in Electrical Engineering',
            'department': 'Electrical Engineering',
            'cgpa': '9.15',
            'specialization': 'Honours in Signal Processing',
        })
        self.assertEqual(reg_response.status_code, 302)
        self.assertTrue('/login/' in reg_response.url)
        
        # Verify student created in database with all detailed fields
        new_student = StudentProfile.objects.filter(roll_number='220070099').first()
        self.assertIsNotNone(new_student)
        self.assertEqual(new_student.full_name, 'Priya Patel')
        self.assertEqual(new_student.city, 'Mumbai')
        self.assertEqual(new_student.tenth_board, 'CBSE')
        self.assertEqual(new_student.tenth_percentage, Decimal('95.60'))
        self.assertEqual(new_student.twelfth_percentage, Decimal('96.80'))
        self.assertEqual(new_student.cgpa, Decimal('9.15'))
        self.assertFalse(new_student.is_dpc_verified)
        self.assertEqual(new_student.verification_status, 'PENDING')

    def test_edit_profile_view(self):
        # Login test student
        self.client.login(username='test_aarav', password='password123')
        
        # Test GET edit profile
        response = self.client.get('/profile/edit/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Update Official Profile')
        self.assertContains(response, '10th & 12th')

        # Test POST edit profile with complete details
        post_response = self.client.post('/profile/edit/', {
            'full_name': 'Aarav Sharma Updated',
            'email': 'aarav.updated@a2z.edu.in',
            'phone_number': '+91 99999 88888',
            'alternate_phone': '+91 99999 77777',
            'permanent_address': 'Flat 501, Green Heights',
            'city': 'Pune',
            'state': 'Maharashtra',
            'pincode': '411001',
            'tenth_board': 'ICSE',
            'tenth_percentage': '97.20',
            'tenth_year': '2019',
            'tenth_school': 'St. Mary High School',
            'twelfth_board': 'State Board',
            'twelfth_percentage': '98.10',
            'twelfth_year': '2021',
            'twelfth_school': 'Fergusson Junior College',
            'degree': 'B.Tech in Computer Science & Engineering',
            'department': 'Computer Science & Engineering',
            'cgpa': '9.65',
            'specialization': 'Honours in AI & Distributed Systems',
        })
        self.assertEqual(post_response.status_code, 200)
        self.assertContains(post_response, 'updated successfully')

        # Verify profile updated in DB
        self.student.refresh_from_db()
        self.assertEqual(self.student.full_name, 'Aarav Sharma Updated')
        self.assertEqual(self.student.city, 'Pune')
        self.assertEqual(self.student.tenth_board, 'ICSE')
        self.assertEqual(self.student.tenth_percentage, Decimal('97.20'))
        self.assertEqual(self.student.twelfth_percentage, Decimal('98.10'))
        self.assertEqual(self.student.cgpa, Decimal('9.65'))

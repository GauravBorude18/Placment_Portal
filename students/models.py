import re
from django.db import models
from django.contrib.auth.models import User

class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile')
    roll_number = models.CharField(max_length=20, unique=True)
    full_name = models.CharField(max_length=120)
    degree = models.CharField(max_length=150, default="B.Tech in Computer Science & Engineering")
    department = models.CharField(max_length=120, default="Computer Science & Engineering")
    specialization = models.CharField(max_length=200, default="General / Standard Coursework", blank=True)
    cgpa = models.DecimalField(max_digits=4, decimal_places=2, default=9.48)
    batch = models.CharField(max_length=50, default="Class of 2026")
    department_rank = models.IntegerField(default=4)
    is_dpc_verified = models.BooleanField(default=False, help_text="True only when TPO / Placement Head approves candidate")
    resume_sde_name = models.CharField(max_length=150, default="Aarav_Sharma_SDE_Master.pdf")
    resume_quant_name = models.CharField(max_length=150, default="Aarav_Sharma_Quant_Finance.pdf")
    resume_sde_file = models.FileField(upload_to='resumes/', blank=True, null=True)
    resume_quant_file = models.FileField(upload_to='resumes/', blank=True, null=True)
    profile_picture = models.FileField(upload_to='profiles/students/', blank=True, null=True, help_text="Official student passport photo")
    dpc_verifier = models.CharField(max_length=120, default="Prof. S. Bhattacharya (DPC)")

    @property
    def is_profile_completed(self):
        """
        Check whether the student has completed adding their profile information.
        Returns True if full_name, roll_number, and contact/academic details are filled out.
        """
        if not self.full_name or self.full_name.strip() in ['', 'New Student', 'Draft', 'Unregistered']:
            return False
        if not self.roll_number or self.roll_number.strip() in ['', '0', '000']:
            return False
        if not self.phone_number and not self.current_address and not self.is_fee_paid:
            return False
        return True

    @property
    def profile_picture_url(self):
        if self.profile_picture:
            try:
                return self.profile_picture.url
            except Exception:
                pass
        return None
    verification_status = models.CharField(
        max_length=30,
        choices=[
            ('PENDING', 'Pending Review'),
            ('APPROVED', 'Approved by Placement Head'),
            ('DECLINED', 'Declined / Rejected'),
            ('ON_HOLD', 'Temporarily On Hold')
        ],
        default='PENDING'
    )
    verification_remarks = models.TextField(blank=True, default="", help_text="Remarks/Reason for decline or temporary hold")
    hold_days = models.IntegerField(default=0, help_text="Days candidate is kept on hold")
    hold_until = models.DateTimeField(null=True, blank=True, help_text="Automatic hold release timestamp")
    approved_by = models.CharField(max_length=150, blank=True, default="")

    def check_and_release_hold(self):
        """If hold period has expired, automatically release hold and re-approve."""
        from django.utils import timezone
        if self.verification_status == 'ON_HOLD' and self.hold_until:
            if timezone.now() >= self.hold_until:
                self.verification_status = 'APPROVED'
                self.is_dpc_verified = True
                self.verification_remarks = f"Auto-released from hold on {timezone.now().strftime('%b %d, %Y')}"
                self.hold_until = None
                self.save()
                return True
        return False

    # Contact & Address (Current & Permanent)
    phone_number = models.CharField(max_length=20, blank=True, default="")
    alternate_phone = models.CharField(max_length=20, blank=True, default="")
    
    # Current / Communication Address
    current_address = models.TextField(blank=True, default="")
    current_city = models.CharField(max_length=100, blank=True, default="")
    current_state = models.CharField(max_length=100, blank=True, default="")
    current_pincode = models.CharField(max_length=20, blank=True, default="")
    same_as_current_address = models.BooleanField(default=True)

    # Permanent Residential Address
    permanent_address = models.TextField(blank=True, default="")
    city = models.CharField(max_length=100, blank=True, default="")
    state = models.CharField(max_length=100, blank=True, default="")
    pincode = models.CharField(max_length=20, blank=True, default="")
    is_email_verified = models.BooleanField(default=False)
    
    # Placement Enrollment Fee Payment Tracking (₹99)
    is_fee_paid = models.BooleanField(default=False, help_text="True when student pays ₹99 enrollment fee")
    fee_amount_paid = models.DecimalField(max_digits=10, decimal_places=2, default=99.00)
    fee_order_id = models.CharField(max_length=100, blank=True, default="")
    fee_payment_id = models.CharField(max_length=100, blank=True, default="")
    fee_paid_at = models.DateTimeField(null=True, blank=True)

    # 10th, 12th & Diploma Academic Records
    entry_route = models.CharField(
        max_length=50,
        choices=[
            ('12TH_REGULAR', '12th Standard Route (8 Semesters)'),
            ('DIPLOMA_DSE', 'Diploma / Direct Second Year Route (6 Semesters)')
        ],
        default='12TH_REGULAR'
    )
    tenth_board = models.CharField(max_length=100, blank=True, default="CBSE")
    tenth_percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, default=95.00)
    tenth_year = models.CharField(max_length=10, blank=True, default="2020")
    tenth_school = models.CharField(max_length=200, blank=True, default="")
    twelfth_board = models.CharField(max_length=100, blank=True, default="CBSE")
    twelfth_percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, default=96.50)
    twelfth_year = models.CharField(max_length=10, blank=True, default="2022")
    twelfth_school = models.CharField(max_length=200, blank=True, default="")
    
    # 12th Subject-Specific Marks
    twelfth_maths = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, default=95.00)
    twelfth_physics = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, default=94.00)
    twelfth_chemistry = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, default=92.00)
    twelfth_english = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, default=90.00)
    twelfth_computer_science = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, default=98.00)
    custom_subject_marks = models.JSONField(default=dict, blank=True, help_text="Dynamic custom 12th subject marks e.g. {'Statistics': 92.0, 'Electronics': 90.0}")

    # Diploma Records
    diploma_board = models.CharField(max_length=100, blank=True, default="MSBTE")
    diploma_percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, default=85.00)
    diploma_college = models.CharField(max_length=200, blank=True, default="")
    diploma_sem1_percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, default=85.00)
    diploma_sem2_percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, default=86.00)
    diploma_sem3_percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, default=88.00)
    diploma_sem4_percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, default=87.50)
    diploma_sem5_percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, default=89.00)
    diploma_sem6_percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, default=90.50)
    
    # Degree Semester-Wise SGPA Pointers (Sem 1 to Sem 8)
    sem1_sgpa = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True, default=9.20)
    sem2_sgpa = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True, default=9.40)
    sem3_sgpa = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True, default=9.10)
    sem4_sgpa = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True, default=9.50)
    sem5_sgpa = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True, default=9.60)
    sem6_sgpa = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True, default=9.40)
    sem7_sgpa = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True, default=9.50)
    sem8_sgpa = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True, default=9.60)

    # Degree Semester-Wise Backlogs Count
    sem1_backlogs = models.IntegerField(default=0, help_text="Backlogs in Sem 1")
    sem2_backlogs = models.IntegerField(default=0, help_text="Backlogs in Sem 2")
    sem3_backlogs = models.IntegerField(default=0, help_text="Backlogs in Sem 3")
    sem4_backlogs = models.IntegerField(default=0, help_text="Backlogs in Sem 4")
    sem5_backlogs = models.IntegerField(default=0, help_text="Backlogs in Sem 5")
    sem6_backlogs = models.IntegerField(default=0, help_text="Backlogs in Sem 6")
    sem7_backlogs = models.IntegerField(default=0, help_text="Backlogs in Sem 7")
    sem8_backlogs = models.IntegerField(default=0, help_text="Backlogs in Sem 8")

    # Backlog Tracker
    active_backlogs = models.IntegerField(default=0, help_text="Live/Active backlogs in current semester (0 = No Backlog)")
    total_backlogs_history = models.IntegerField(default=0, help_text="Past dead backlogs history (0 = Never Backlog)")

    # Core Technical Skills & Projects
    technical_skills = models.TextField(blank=True, default="Data Structures & Algorithms, Python / Django, C++ Systems Programming, PostgreSQL & Distributed DBs, REST APIs & Microservices", help_text="Comma-separated or bulleted technical skills & specializations")
    key_projects_experience = models.TextField(blank=True, default="Enterprise High-Throughput Matching Engine: Designed distributed order matching pipeline handling 10,000+ requests/sec with Redis & Celery.\nAutonomous AI Analytics Platform: Built end-to-end ML pipeline with transformer models for predictive classification.\nAcademic Honours: Dean's List for academic excellence; Top 1% in National Engineering Olympiad.", help_text="Key engineering projects, industry experience & academic honours")

    def __str__(self):
        return f"{self.full_name} ({self.roll_number}) - CGPA: {self.cgpa}"

    @property
    def skills_list(self):
        """Returns clean list of individual technical skills."""
        if not self.technical_skills:
            return []
        items = re.split(r'[,;\n]+', self.technical_skills)
        return [i.strip() for i in items if i.strip()]

    @property
    def projects_list(self):
        """Returns clean list of project lines."""
        if not self.key_projects_experience:
            return []
        lines = self.key_projects_experience.splitlines()
        return [l.strip() for l in lines if l.strip()]

    @property
    def semester_pointers(self):
        """Returns list of semester numbers, pointers and backlogs based on entry route."""
        if self.entry_route == 'DIPLOMA_DSE':
            return [
                {'sem': 'Sem 3', 'sgpa': self.sem3_sgpa, 'backlogs': self.sem3_backlogs, 'is_exempted': False},
                {'sem': 'Sem 4', 'sgpa': self.sem4_sgpa, 'backlogs': self.sem4_backlogs, 'is_exempted': False},
                {'sem': 'Sem 5', 'sgpa': self.sem5_sgpa, 'backlogs': self.sem5_backlogs, 'is_exempted': False},
                {'sem': 'Sem 6', 'sgpa': self.sem6_sgpa, 'backlogs': self.sem6_backlogs, 'is_exempted': False},
                {'sem': 'Sem 7', 'sgpa': self.sem7_sgpa, 'backlogs': self.sem7_backlogs, 'is_exempted': False},
                {'sem': 'Sem 8', 'sgpa': self.sem8_sgpa, 'backlogs': self.sem8_backlogs, 'is_exempted': False},
            ]
        else:
            return [
                {'sem': 'Sem 1', 'sgpa': self.sem1_sgpa, 'backlogs': self.sem1_backlogs, 'is_exempted': False},
                {'sem': 'Sem 2', 'sgpa': self.sem2_sgpa, 'backlogs': self.sem2_backlogs, 'is_exempted': False},
                {'sem': 'Sem 3', 'sgpa': self.sem3_sgpa, 'backlogs': self.sem3_backlogs, 'is_exempted': False},
                {'sem': 'Sem 4', 'sgpa': self.sem4_sgpa, 'backlogs': self.sem4_backlogs, 'is_exempted': False},
                {'sem': 'Sem 5', 'sgpa': self.sem5_sgpa, 'backlogs': self.sem5_backlogs, 'is_exempted': False},
                {'sem': 'Sem 6', 'sgpa': self.sem6_sgpa, 'backlogs': self.sem6_backlogs, 'is_exempted': False},
                {'sem': 'Sem 7', 'sgpa': self.sem7_sgpa, 'backlogs': self.sem7_backlogs, 'is_exempted': False},
                {'sem': 'Sem 8', 'sgpa': self.sem8_sgpa, 'backlogs': self.sem8_backlogs, 'is_exempted': False},
            ]

    @property
    def diploma_semesters(self):
        """Returns list of all 6 diploma semester marks."""
        return [
            {'sem': 'Sem 1', 'percentage': self.diploma_sem1_percentage},
            {'sem': 'Sem 2', 'percentage': self.diploma_sem2_percentage},
            {'sem': 'Sem 3', 'percentage': self.diploma_sem3_percentage},
            {'sem': 'Sem 4', 'percentage': self.diploma_sem4_percentage},
            {'sem': 'Sem 5', 'percentage': self.diploma_sem5_percentage},
            {'sem': 'Sem 6', 'percentage': self.diploma_sem6_percentage},
        ]

    @property
    def all_twelfth_subjects(self):
        """Returns list of standard and custom 12th subjects with scores."""
        subs = []
        if self.twelfth_maths is not None: subs.append({'name': 'Mathematics', 'marks': self.twelfth_maths, 'icon': '📐'})
        if self.twelfth_physics is not None: subs.append({'name': 'Physics', 'marks': self.twelfth_physics, 'icon': '⚡'})
        if self.twelfth_chemistry is not None: subs.append({'name': 'Chemistry', 'marks': self.twelfth_chemistry, 'icon': '🧪'})
        if self.twelfth_english is not None: subs.append({'name': 'English', 'marks': self.twelfth_english, 'icon': '🗣️'})
        if self.twelfth_computer_science is not None: subs.append({'name': 'Computer Science', 'marks': self.twelfth_computer_science, 'icon': '💻'})
        if isinstance(self.custom_subject_marks, dict):
            for name, marks in self.custom_subject_marks.items():
                subs.append({'name': name, 'marks': marks, 'icon': '📚'})
        return subs

    @property
    def applied_count(self):
        return self.applications.count()

    @property
    def shortlisted_count(self):
        return self.applications.filter(status='SHORTLISTED').count()

    @property
    def interviews_count(self):
        return self.applications.filter(status='INTERVIEW').count()

    @property
    def offers_count(self):
        return self.applications.filter(status='OFFERED').count()


class Company(models.Model):
    name = models.CharField(max_length=150, unique=True)
    logo_url = models.URLField(max_length=500, blank=True)
    logo_file = models.FileField(upload_to='profiles/companies/', blank=True, null=True, help_text="Uploaded corporate logo")
    logo_fallback = models.CharField(max_length=10, default="🏢")
    sector = models.CharField(max_length=100)
    location = models.CharField(max_length=200)
    website = models.URLField(max_length=300, blank=True)

    @property
    def display_logo_url(self):
        if self.logo_file:
            try:
                return self.logo_file.url
            except Exception:
                pass
        return self.logo_url or ""

    class Meta:
        verbose_name_plural = "Companies"

    def __str__(self):
        return self.name


class JobAnnouncementForm(models.Model):
    SECTOR_CHOICES = [
        ('Software & AI', 'Software & AI'),
        ('Quant & Finance', 'Quant & Finance'),
        ('Core Engineering', 'Core Engineering'),
        ('Management Consulting', 'Management Consulting'),
        ('Analytics & Data', 'Analytics & Data'),
    ]

    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='jafs')
    role_title = models.CharField(max_length=200)
    sector = models.CharField(max_length=100, choices=SECTOR_CHOICES, default='Software & AI')
    location = models.CharField(max_length=250, default="Bangalore / Mumbai / Remote")
    ctc_display = models.CharField(max_length=100, help_text="e.g. ₹48.5 LPA or ₹1.42 Cr")
    ctc_breakdown = models.TextField(blank=True, default="Base Salary + Performance Bonus + Relocation Assistance", help_text="Detailed compensation details")
    
    # 1. Standard 10th, 12th & Degree CPI Toggles
    require_tenth_cutoff = models.BooleanField(default=True, help_text="Check to enforce 10th cutoff")
    min_tenth_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=60.00, help_text="Minimum 10th percentage cutoff")
    
    require_twelfth_cutoff = models.BooleanField(default=True, help_text="Check to enforce 12th/Diploma cutoff")
    min_twelfth_diploma_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=60.00, help_text="Minimum 12th/Diploma percentage cutoff")
    
    # 2. 12th Subject-Wise Cutoff Toggles (Maths, Physics, Chemistry, English & Dynamic Subjects)
    require_twelfth_subjects = models.BooleanField(default=False, help_text="Check to enforce 12th subject-wise cutoffs")
    min_twelfth_maths = models.DecimalField(max_digits=5, decimal_places=2, default=60.00, help_text="Minimum 12th Mathematics %")
    min_twelfth_physics = models.DecimalField(max_digits=5, decimal_places=2, default=60.00, help_text="Minimum 12th Physics %")
    min_twelfth_chemistry = models.DecimalField(max_digits=5, decimal_places=2, default=60.00, help_text="Minimum 12th Chemistry %")
    min_twelfth_english = models.DecimalField(max_digits=5, decimal_places=2, default=60.00, help_text="Minimum 12th English %")
    custom_subject_cutoffs = models.JSONField(default=dict, blank=True, help_text="Additional custom 12th subjects e.g. {'Computer Science': 75.0, 'Electronics': 70.0}")

    # 3. Degree Cumulative CPI & Semester-wise SGPA Pointer Toggles
    require_cgpa_cutoff = models.BooleanField(default=True, help_text="Check to enforce Degree CPI cutoff")
    cgpa_cutoff = models.DecimalField(max_digits=4, decimal_places=2, default=7.50, help_text="Minimum Degree CPI cutoff")
    
    require_min_sem_sgpa = models.BooleanField(default=False, help_text="Check to enforce minimum pointer in every semester")
    min_sem_sgpa = models.DecimalField(max_digits=4, decimal_places=2, default=6.00, help_text="Minimum SGPA pointer per semester")
    
    # 4. Backlogs Policy (Independent Toggles for Active Live vs Past Dead Backlogs)
    require_no_backlogs = models.BooleanField(default=True, help_text="Legacy flag for backlogs")
    require_active_backlogs_cutoff = models.BooleanField(default=True, help_text="Check to enforce Active/Live Backlogs limit")
    max_active_backlogs = models.IntegerField(default=0, help_text="Maximum live backlogs allowed (0 = Strictly No Backlogs)")
    
    require_history_backlogs_cutoff = models.BooleanField(default=True, help_text="Check to enforce Past Dead Backlogs history limit")
    max_history_backlogs = models.IntegerField(default=0, help_text="Maximum past backlogs allowed (0 = Clear record)")

    allowed_entry_routes = models.CharField(
        max_length=50,
        choices=[
            ('BOTH', 'Both 12th Regular (8 Sems) & Diploma DSE (6 Sems)'),
            ('12TH_ONLY', '12th Regular Route Only (8 Semesters)'),
            ('DIPLOMA_ONLY', 'Diploma DSE Route Only (6 Semesters)')
        ],
        default='BOTH'
    )

    eligible_branches = models.JSONField(default=list, help_text="List of eligible branches")
    eligible_degrees = models.JSONField(default=list, help_text="List of degrees e.g. B.Tech, Dual Degree")
    deadline = models.DateTimeField(null=True, blank=True)
    deadline_display = models.CharField(max_length=100, default="In 5 days, 11:59 PM IST")
    hiring_slot = models.CharField(max_length=100, default="Day 1 • Slot 1 (Dec 1)")
    description = models.TextField()
    requirements = models.JSONField(default=list)
    selection_process = models.JSONField(default=list)
    bond_details = models.CharField(max_length=100, default="None")
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)
    approval_status = models.CharField(
        max_length=30,
        choices=[
            ('APPROVED', 'Approved & Published'),
            ('PENDING', 'Pending TPO Approval'),
            ('REJECTED', 'Rejected')
        ],
        default='APPROVED'
    )
    is_workflow_configured = models.BooleanField(default=False, help_text="True when HR configures/updates hiring roadmap stages")
    created_at = models.DateTimeField(auto_now_add=True)

    def check_student_eligibility(self, student):
        """
        Evaluates active criteria based on which checkboxes were toggled ON:
        1. 10th Standard (if require_tenth_cutoff is True)
        2. 12th/Diploma (if require_twelfth_cutoff is True)
        3. 12th Subject Marks (Maths, Physics, Chem, English & Custom Subjects) (if require_twelfth_subjects is True)
        4. Degree Overall CPI (if require_cgpa_cutoff is True)
        5. Degree Semester Pointers (if require_min_sem_sgpa is True)
        6. Live Active Backlogs (if require_active_backlogs_cutoff is True)
        7. Past Dead Backlogs History (if require_history_backlogs_cutoff is True)
        """
        reasons = []

        # 1. 10th Standard Marks Check
        if self.require_tenth_cutoff:
            if student.tenth_percentage is not None and student.tenth_percentage < self.min_tenth_percentage:
                reasons.append(f"10th Marks ({student.tenth_percentage}%) below required cutoff ({self.min_tenth_percentage}%)")

        # 2. 12th / Diploma Overall Marks Check
        if self.require_twelfth_cutoff:
            if student.entry_route == 'DIPLOMA_DSE':
                qualifying_score = student.diploma_percentage
                score_type = "Diploma"
            else:
                qualifying_score = student.twelfth_percentage
                score_type = "12th Standard"

            if qualifying_score is not None and qualifying_score < self.min_twelfth_diploma_percentage:
                reasons.append(f"{score_type} Marks ({qualifying_score}%) below required cutoff ({self.min_twelfth_diploma_percentage}%)")

        # 3. 12th Subject-Wise Cutoff Check (Only for 12th students)
        if self.require_twelfth_subjects and student.entry_route != 'DIPLOMA_DSE':
            if student.twelfth_maths is not None and student.twelfth_maths < self.min_twelfth_maths:
                reasons.append(f"12th Maths ({student.twelfth_maths}%) below subject cutoff ({self.min_twelfth_maths}%)")
            if student.twelfth_physics is not None and student.twelfth_physics < self.min_twelfth_physics:
                reasons.append(f"12th Physics ({student.twelfth_physics}%) below subject cutoff ({self.min_twelfth_physics}%)")
            if student.twelfth_chemistry is not None and student.twelfth_chemistry < self.min_twelfth_chemistry:
                reasons.append(f"12th Chemistry ({student.twelfth_chemistry}%) below subject cutoff ({self.min_twelfth_chemistry}%)")
            if student.twelfth_english is not None and student.twelfth_english < self.min_twelfth_english:
                reasons.append(f"12th English ({student.twelfth_english}%) below subject cutoff ({self.min_twelfth_english}%)")

            # Dynamic Custom 12th Subjects Check
            if self.custom_subject_cutoffs:
                for subj_name, min_score in self.custom_subject_cutoffs.items():
                    try:
                        req_min = float(min_score)
                        if subj_name.lower() in ['computer science', 'cs', 'informatics']:
                            st_score = float(student.twelfth_computer_science or 98.0)
                        else:
                            st_score = float(student.custom_subject_marks.get(subj_name, 90.0))
                        if st_score < req_min:
                            reasons.append(f"12th {subj_name} ({st_score}%) below required cutoff ({req_min}%)")
                    except (ValueError, TypeError):
                        pass

        # 4. Degree CPI Cutoff Check
        if self.require_cgpa_cutoff:
            if student.cgpa is not None and student.cgpa < self.cgpa_cutoff:
                reasons.append(f"Degree CPI ({student.cgpa}) below cutoff ({self.cgpa_cutoff})")

        # 5. Degree Semester-Wise Pointer Check (SGPA in every semester >= min_sem_sgpa)
        if self.require_min_sem_sgpa:
            for sem_info in student.semester_pointers:
                sgpa = sem_info['sgpa']
                if sgpa is not None and sgpa < self.min_sem_sgpa:
                    reasons.append(f"{sem_info['sem']} SGPA ({sgpa}) is below minimum required pointer ({self.min_sem_sgpa})")

        # 6. Live / Active Backlogs Check (Independent Checkbox)
        if self.require_active_backlogs_cutoff:
            if 0 <= self.max_active_backlogs < 99:
                if student.active_backlogs > self.max_active_backlogs:
                    reasons.append(f"Active Live Backlogs ({student.active_backlogs}) exceeds allowed limit ({self.max_active_backlogs})")

        # 7. Past Dead Backlogs History Check (Independent Checkbox)
        if self.require_history_backlogs_cutoff:
            if 0 <= self.max_history_backlogs < 99:
                if student.total_backlogs_history > self.max_history_backlogs:
                    reasons.append(f"Past Backlogs History ({student.total_backlogs_history}) exceeds allowed limit ({self.max_history_backlogs})")

        # 8. Department / Branch Eligibility Check
        if self.eligible_branches:
            branches_str_list = [str(b).lower().strip() for b in self.eligible_branches]
            is_all_branches = any('all' in b for b in branches_str_list)
            if not is_all_branches:
                dept_lower = (student.department or '').lower().strip()
                dept_keywords = [dept_lower]

                if any(k in dept_lower for k in ['computer', 'cse', 'cs', 'it', 'comp']):
                    dept_keywords.extend(['cs', 'cse', 'computer science', 'computer', 'computer engineering', 'it', 'information technology'])
                
                if any(k in dept_lower for k in ['electrical', 'ee', 'eee', 'ece', 'electronics', 'telecom', 'e&tc', 'entc']):
                    dept_keywords.extend(['ee', 'eee', 'ece', 'electrical', 'electrical engineering', 'electronics', 'e&tc', 'entc', 'telecommunication'])
                
                if any(k in dept_lower for k in ['mechanical', 'me', 'mech']):
                    dept_keywords.extend(['me', 'mech', 'mechanical', 'mechanical engineering'])
                
                if any(k in dept_lower for k in ['civil', 'ce']):
                    dept_keywords.extend(['ce', 'civil', 'civil engineering'])
                
                if any(k in dept_lower for k in ['data science', 'ai', 'ds']):
                    dept_keywords.extend(['ds', 'ai', 'data science', 'artificial intelligence'])
                
                if any(k in dept_lower for k in ['mathematics', 'math', 'mnc']):
                    dept_keywords.extend(['math', 'mnc', 'mathematics', 'computing'])

                branch_matched = False
                for branch in branches_str_list:
                    for kw in dept_keywords:
                        if not kw:
                            continue
                        if re.search(r'\b' + re.escape(kw) + r'\b', branch) or kw == branch or kw in branch or branch in kw:
                            branch_matched = True
                            break
                    if branch_matched:
                        break

                if not branch_matched:
                    eligible_branches_formatted = ", ".join(self.eligible_branches)
                    reasons.append(f"Branch Ineligible: Your department ({student.department}) is not listed under eligible disciplines ({eligible_branches_formatted})")

        is_eligible = (len(reasons) == 0)
        return is_eligible, reasons

    class Meta:
        verbose_name = "Job Announcement Form (JAF)"
        verbose_name_plural = "Job Announcement Forms (JAFs)"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.company.name} - {self.role_title} ({self.ctc_display})"


class Application(models.Model):
    STATUS_CHOICES = [
        ('APPLIED', 'Application Submitted'),
        ('SHORTLISTED', 'Shortlisted for Day 1'),
        ('INTERVIEW', 'Interview Scheduled'),
        ('OFFERED', 'Offer Extended'),
        ('REJECTED', 'Not Selected'),
    ]

    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='applications')
    jaf = models.ForeignKey(JobAnnouncementForm, on_delete=models.CASCADE, related_name='applications')
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='APPLIED')
    current_round_title = models.CharField(max_length=200, default="Application Submitted", blank=True, null=True)
    applied_at = models.DateTimeField(auto_now_add=True)
    resume_used = models.CharField(max_length=150, default="Aarav_Sharma_SDE_Master.pdf")

    class Meta:
        unique_together = ('student', 'jaf')
        ordering = ['-applied_at']

    def __str__(self):
        return f"{self.student.roll_number} -> {self.jaf.company.name} [{self.status}]"


class HiringRound(models.Model):
    ROUND_TYPES = [
        ('REGISTRATION', '1. Registration & Criteria Filtering'),
        ('SHORTLISTING', '2. Resume & Profile Shortlisting Round'),
        ('ONLINE_TEST', '3. Technical Test / Coding Assessment'),
        ('GROUP_DISCUSSION', '4. Group Discussion (GD) / Communication'),
        ('TECH_INTERVIEW_1', '5. Technical Interview (Round 1)'),
        ('TECH_INTERVIEW_2', '6. Technical Interview (Round 2)'),
        ('HR_INTERVIEW', '7. HR & Leadership Fitment Round'),
        ('OFFER_ROLLOUT', '8. Final Job Offer Rollout'),
    ]

    STATUS_CHOICES = [
        ('UPCOMING', 'Upcoming / Scheduled'),
        ('ACTIVE', 'Active In Progress'),
        ('COMPLETED', 'Completed'),
    ]

    MODE_CHOICES = [
        ('ONLINE', '🌐 Online Mode (Video Meeting / Test Link)'),
        ('OFFLINE', '📍 Offline Mode (Campus Venue & Address)'),
        ('HYBRID', '🔀 Hybrid Mode (Both Online Link & Venue)'),
    ]

    jaf = models.ForeignKey(JobAnnouncementForm, on_delete=models.CASCADE, related_name='hiring_rounds')
    round_number = models.IntegerField(default=1)
    round_type = models.CharField(max_length=50, choices=ROUND_TYPES, default='ONLINE_TEST')
    mode = models.CharField(max_length=20, choices=MODE_CHOICES, default='ONLINE')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, default="")
    scheduled_date = models.CharField(max_length=100, default="Dec 1, 2026")
    scheduled_time = models.CharField(max_length=100, default="10:00 AM - 12:00 PM IST")
    deadline = models.CharField(max_length=150, blank=True, default="")
    location_or_platform = models.CharField(max_length=250, default="Online HackerRank Assessment / Room 204")
    meeting_link = models.CharField(max_length=500, blank=True, default="")
    venue_address = models.TextField(blank=True, default="")
    passing_criteria = models.CharField(max_length=200, default="Min 70% Cutoff Score")
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='UPCOMING')
    total_shortlisted = models.IntegerField(default=0)
    total_cleared = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['round_number']

    def __str__(self):
        return f"{self.jaf.company.name} - Round {self.round_number}: {self.title} [{self.status}]"


class InterviewSlot(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='interviews')
    jaf = models.ForeignKey(JobAnnouncementForm, on_delete=models.CASCADE, related_name='interviews')
    round_name = models.CharField(max_length=200)
    interview_date = models.CharField(max_length=100, default="Dec 1, 2026")
    interview_time = models.CharField(max_length=100, default="08:30 AM - 09:30 AM IST")
    slot_display = models.CharField(max_length=100, default="Day 1 • Slot 1")
    location = models.CharField(max_length=250, default="Room MB-204 (Gulmohar Building)")
    meeting_link = models.URLField(max_length=500, blank=True)
    interview_type = models.CharField(max_length=100, default="Technical")
    status = models.CharField(max_length=50, default="Confirmed")

    def __str__(self):
        return f"{self.student.roll_number} - {self.jaf.company.name} ({self.round_name})"


class PlacementAnnouncement(models.Model):
    TAG_TYPES = [
        ('danger', 'Urgent / Alert'),
        ('success', 'Shortlist / Offer'),
        ('warning', 'Notice / Deadline'),
        ('info', 'PPT / General'),
    ]

    title = models.CharField(max_length=250)
    content = models.TextField()
    tag = models.CharField(max_length=50, default="NOTICE")
    tag_type = models.CharField(max_length=20, choices=TAG_TYPES, default='info')
    author = models.CharField(max_length=150, default="Placement Office (TPO)")
    time_display = models.CharField(max_length=100, default="Just now")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"[{self.tag}] {self.title}"


class StudentEmailNotification(models.Model):
    """Audit log & In-app mailbox for all automated emails dispatched to students."""
    NOTIFICATION_TYPES = [
        ('OTP', 'Email Verification OTP'),
        ('SHORTLIST', 'Shortlisted for Online Test / Assessment'),
        ('INTERVIEW', 'Interview Slot & Invitation Call'),
        ('OFFER', 'Campus Placement Job Offer Letter'),
        ('REJECTED', 'Application Status Update'),
    ]

    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='email_notifications')
    company = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True, blank=True, related_name='sent_notifications')
    jaf = models.ForeignKey(JobAnnouncementForm, on_delete=models.SET_NULL, null=True, blank=True, related_name='notifications')
    notification_type = models.CharField(max_length=30, choices=NOTIFICATION_TYPES, default='SHORTLIST')
    subject = models.CharField(max_length=300)
    recipient_email = models.EmailField()
    headline = models.CharField(max_length=250, default="")
    body_content = models.TextField()
    action_url = models.CharField(max_length=500, blank=True, default="")
    action_label = models.CharField(max_length=100, blank=True, default="")
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.student.roll_number} - [{self.notification_type}] {self.subject}"


class StudentPaymentTransaction(models.Model):
    """
    विद्यार्थ्याच्या ₹99 प्लेसमेंट एनरोलमेंट फी ट्रान्झॅक्शनची अधिकृत पावती नोंद.
    Official payment receipt record for ₹99 placement enrollment fee.
    """
    STATUS_CHOICES = [
        ('SUCCESS', 'Payment Successful & Verified'),
        ('PENDING', 'Payment Pending'),
        ('FAILED', 'Payment Failed / Rejected'),
        ('REFUNDED', 'Payment Refunded')
    ]

    PAYMENT_METHOD_CHOICES = [
        ('UPI_QR', 'UPI QR Code (GPay / PhonePe / Paytm / BHIM)'),
        ('UPI_ID', 'UPI ID / VPA Intent'),
        ('CARD', 'Debit / Credit Card'),
        ('NETBANKING', 'NetBanking'),
        ('WALLET', 'Digital Wallet'),
        ('RAZORPAY_DIRECT', 'Razorpay Gateway Direct')
    ]

    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='payment_receipts')
    receipt_number = models.CharField(max_length=60, unique=True, help_text="e.g. A2Z-2026-FEE-49102")
    order_id = models.CharField(max_length=100, help_text="Razorpay or System Order ID")
    payment_id = models.CharField(max_length=100, blank=True, default="", help_text="Razorpay Payment ID / Txn Ref")
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=99.00, help_text="Fee amount in INR")
    currency = models.CharField(max_length=10, default="INR")
    payment_method = models.CharField(max_length=40, choices=PAYMENT_METHOD_CHOICES, default='UPI_QR')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='SUCCESS')
    paid_at = models.DateTimeField(auto_now_add=True)
    gateway_signature = models.CharField(max_length=255, blank=True, default="")
    notes = models.TextField(blank=True, default="A2Z Placement Cell Phase 1 Student Enrollment Fee")

    class Meta:
        ordering = ['-paid_at']

    def __str__(self):
        return f"{self.receipt_number} - {self.student.full_name} (₹{self.amount}) - {self.status}"


